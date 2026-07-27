"""
Google Gemini LLM Provider Module (NEW SDK)

This module implements the Google Gemini provider using the NEW official google-genai SDK.
The old google-generativeai SDK was deprecated in late 2024.

Uses Gemini 1.5 Flash (free tier) as the primary LLM provider.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional, Iterator
import time

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from src.llm.base_provider import BaseProvider
from src.utils import (
    get_logger,
    LLMAPIError,
    LLMTimeoutError,
    LLMInvalidResponseError,
    LLMRateLimitError
)


logger = get_logger()


class GeminiProvider(BaseProvider):
    """
    Google Gemini LLM provider (free tier) - NEW SDK.
    
    Features:
    - Gemini 1.5 Flash model (free tier)
    - Streaming support
    - High rate limits on free tier
    - Good multilingual support
    - 1M token context window
    
    Requirements:
    - Google GenAI SDK (google-genai) - NEW official SDK
    - Gemini API key (free tier available)
    
    Changes from old SDK:
    - Uses Client object instead of GenerativeModel
    - client.models.generate_content() instead of model.generate_content()
    - Unified streaming with stream parameter
    """
    
    def __init__(
        self,
        model: str = 'gemini-1.5-flash-latest',
        api_key: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        """
        Initialize Gemini provider with NEW SDK.
        
        Args:
            model: Gemini model name (default: gemini-1.5-flash-latest)
            api_key: Gemini API key
            timeout: Request timeout in seconds
            **kwargs: Additional parameters
        
        Example:
            >>> provider = GeminiProvider(api_key='AIza...')
            >>> response = provider.chat_completion([
            ...     {'role': 'user', 'content': 'Hello!'}
            ... ])
        """
        super().__init__(model=model, api_key=api_key, **kwargs)
        self.timeout = timeout
        self.client = None
        
        if GENAI_AVAILABLE and api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                logger.info(f"GeminiProvider initialized with NEW SDK", model=model)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client", error=str(e))
        else:
            if not GENAI_AVAILABLE:
                logger.warning("google-genai package not available (NEW SDK required)")
            else:
                logger.warning("Gemini API key not provided")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "Google Gemini"
    
    def is_available(self) -> bool:
        """
        Check if Gemini is available and configured correctly.
        
        Returns:
            bool: True if provider can be used
        
        Example:
            >>> provider = GeminiProvider(api_key='AIza...')
            >>> if provider.is_available():
            ...     print("Gemini is ready")
        """
        if not GENAI_AVAILABLE:
            logger.debug("Gemini not available - NEW SDK not installed")
            return False
        
        if not self.api_key or not self.client:
            logger.debug("Gemini not available - API key not configured")
            return False
        
        return True
    
    def _convert_messages_to_gemini_format(self, messages: list[dict]) -> tuple[str, list[dict]]:
        """
        Convert OpenAI-style messages to NEW Gemini SDK format.
        
        NEW SDK format:
        - System instruction (string) passed in config
        - Contents array with role ('user'/'model') and parts
        
        Args:
            messages: OpenAI-style messages
        
        Returns:
            tuple: (system_instruction, gemini_contents)
        """
        system_instruction = ""
        gemini_contents = []
        
        for msg in messages:
            role = msg['role']
            content = msg['content']
            
            if role == 'system':
                # System instruction separate in config
                system_instruction = content
            elif role == 'user':
                gemini_contents.append({
                    'role': 'user',
                    'parts': [{'text': content}]
                })
            elif role == 'assistant':
                gemini_contents.append({
                    'role': 'model',  # Gemini uses 'model' instead of 'assistant'
                    'parts': [{'text': content}]
                })
        
        return system_instruction, gemini_contents
    
    def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Generate chat completion using NEW Gemini SDK.
        
        Args:
            messages: List of message dicts (OpenAI format)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Enable streaming
            **kwargs: Additional parameters
        
        Returns:
            str or Iterator[str]: Response text or stream
        
        Raises:
            LLMAPIError: If API call fails
            LLMTimeoutError: If request times out
            LLMRateLimitError: If rate limit exceeded
            LLMInvalidResponseError: If response is invalid
        
        Example:
            >>> provider = GeminiProvider(api_key='AIza...')
            >>> messages = [{'role': 'user', 'content': 'Hello!'}]
            >>> response = provider.chat_completion(messages)
            >>> print(response)
        """
        # Validate inputs
        self.validate_messages(messages)
        self.validate_temperature(temperature)
        
        if not self.client:
            raise LLMAPIError("Gemini", "Provider not initialized - missing API key")
        
        # Convert to Gemini format
        system_instruction, gemini_contents = self._convert_messages_to_gemini_format(messages)
        
        # Build config using NEW SDK types
        config_dict = {
            'temperature': temperature,
        }
        
        if system_instruction:
            config_dict['system_instruction'] = system_instruction
        
        if max_tokens:
            config_dict['max_output_tokens'] = max_tokens
        
        config = types.GenerateContentConfig(**config_dict)
        
        logger.debug(
            f"Gemini chat completion request (NEW SDK)",
            model=self.model,
            num_messages=len(messages),
            stream=stream
        )
        
        try:
            start_time = time.time()
            
            if stream:
                return self._chat_completion_stream(gemini_contents, config, start_time)
            else:
                return self._chat_completion_blocking(gemini_contents, config, start_time)
                
        except Exception as e:
            error_str = str(e).lower()
            
            # Check for timeout
            if 'timeout' in error_str or (time.time() - start_time) > self.timeout:
                logger.error(f"Gemini request timeout", model=self.model)
                raise LLMTimeoutError("Gemini", self.timeout)
            
            # Check for rate limit
            if 'quota' in error_str or 'rate limit' in error_str or '429' in error_str:
                logger.warning(f"Gemini rate limit exceeded")
                raise LLMRateLimitError("Gemini")
            
            # General API error
            logger.error(f"Gemini API error (NEW SDK)", error=str(e), exc_info=True)
            raise LLMAPIError("Gemini", str(e))
    
    def _chat_completion_blocking(
        self,
        gemini_contents: list[dict],
        config: types.GenerateContentConfig,
        start_time: float
    ) -> str:
        """
        Execute blocking (non-streaming) chat completion with NEW SDK.
        
        Args:
            gemini_contents: Messages in Gemini format
            config: Generation configuration
            start_time: Request start time
        
        Returns:
            str: Complete response text
        """
        # NEW SDK: client.models.generate_content()
        response = self.client.models.generate_content(
            model=self.model,
            contents=gemini_contents,
            config=config
        )
        
        # Check if request took too long
        if time.time() - start_time > self.timeout:
            raise LLMTimeoutError("Gemini", self.timeout)
        
        if not response or not response.text:
            raise LLMInvalidResponseError("Gemini", "Empty response from API")
        
        response_text = response.text
        
        logger.info(
            f"Gemini completion successful (NEW SDK)",
            model=self.model,
            response_length=len(response_text)
        )
        
        return response_text
    
    def _chat_completion_stream(
        self,
        gemini_contents: list[dict],
        config: types.GenerateContentConfig,
        start_time: float
    ) -> Iterator[str]:
        """
        Execute streaming chat completion with NEW SDK.
        
        Args:
            gemini_contents: Messages in Gemini format
            config: Generation configuration
            start_time: Request start time
        
        Yields:
            str: Response chunks
        """
        logger.info(f"Gemini streaming started (NEW SDK)", model=self.model)
        
        try:
            # NEW SDK: client.models.generate_content_stream()
            response_stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=gemini_contents,
                config=config
            )
            
            for chunk in response_stream:
                # Check timeout
                if time.time() - start_time > self.timeout:
                    raise LLMTimeoutError("Gemini", self.timeout)
                
                if chunk.text:
                    yield chunk.text
            
            logger.debug("Gemini streaming complete (NEW SDK)")
            
        except LLMTimeoutError:
            raise
        except Exception as e:
            logger.error(f"Gemini streaming error (NEW SDK)", error=str(e), exc_info=True)
            raise LLMAPIError("Gemini", f"Streaming error: {e}")
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using NEW Gemini SDK.
        
        Args:
            text: Text to count tokens for
        
        Returns:
            int: Token count
        
        Example:
            >>> provider = GeminiProvider(api_key='AIza...')
            >>> count = provider.count_tokens("Hello, world!")
            >>> print(count)
            4
        """
        if not self.client:
            # Fallback to approximate count (4 chars per token)
            return len(text) // 4
        
        try:
            # NEW SDK: client.models.count_tokens()
            response = self.client.models.count_tokens(
                model=self.model,
                contents=text
            )
            return response.total_tokens
        except Exception as e:
            logger.warning(f"Failed to count tokens with Gemini (NEW SDK)", error=str(e))
            # Fallback
            return len(text) // 4


# Convenience: Allow direct import
__all__ = [
    'GeminiProvider',
]


# Singleton instance
_gemini_provider_instance: Optional[GeminiProvider] = None


def get_gemini_provider() -> GeminiProvider:
    """
    Get singleton GeminiProvider instance.
    
    Returns:
        GeminiProvider: Singleton Gemini provider instance
    
    Example:
        >>> provider = get_gemini_provider()
        >>> response = provider.chat_completion(messages)
    """
    global _gemini_provider_instance
    
    if _gemini_provider_instance is None:
        from src.config import get_settings
        settings = get_settings()
        
        _gemini_provider_instance = GeminiProvider(
            model=settings.GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY
        )
        logger.debug("GeminiProvider singleton created (NEW SDK)")
    
    return _gemini_provider_instance
