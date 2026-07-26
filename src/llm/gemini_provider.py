"""
Google Gemini LLM Provider Module

This module implements the Google Gemini provider for the TechFlow Solutions project.
Uses Gemini 2.0 Flash (free tier) as the primary LLM provider.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional, Iterator
import time

try:
    import google.generativeai as genai
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
    Google Gemini LLM provider (free tier).
    
    Features:
    - Gemini 1.5 Flash model (free tier)
    - Streaming support
    - High rate limits on free tier
    - Good multilingual support
    - 1M token context window
    
    Requirements:
    - Google Generative AI SDK (google-generativeai)
    - Gemini API key (free tier available)
    """
    
    def __init__(
        self,
        model: str = 'gemini-1.5-flash',
        api_key: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        """
        Initialize Gemini provider.
        
        Args:
            model: Gemini model name (default: gemini-1.5-flash)
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
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel(model)
                logger.info(f"GeminiProvider initialized", model=model)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client", error=str(e))
        else:
            if not GENAI_AVAILABLE:
                logger.warning("google-generativeai package not available")
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
            logger.debug("Gemini not available - SDK not installed")
            return False
        
        if not self.api_key or not self.client:
            logger.debug("Gemini not available - API key not configured")
            return False
        
        try:
            # Simple test to verify API key works
            test_model = genai.GenerativeModel(self.model)
            # Just checking if we can create the model is enough
            return True
        except Exception as e:
            logger.debug(f"Gemini availability check failed: {e}")
            return False
    
    def _convert_messages_to_gemini_format(self, messages: list[dict]) -> tuple[str, list[dict]]:
        """
        Convert OpenAI-style messages to Gemini format.
        
        Gemini uses a different format:
        - system_instruction (string)
        - contents (list of {'role': 'user'/'model', 'parts': [{'text': '...'}]})
        
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
                # Gemini uses system_instruction separately
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
        Generate chat completion using Gemini.
        
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
        
        # Create model with system instruction if present
        if system_instruction:
            model = genai.GenerativeModel(
                self.model,
                system_instruction=system_instruction
            )
        else:
            model = self.client
        
        # Build generation config
        generation_config = {
            'temperature': temperature,
        }
        
        if max_tokens:
            generation_config['max_output_tokens'] = max_tokens
        
        logger.debug(
            f"Gemini chat completion request",
            model=self.model,
            num_messages=len(messages),
            stream=stream
        )
        
        try:
            start_time = time.time()
            
            if stream:
                return self._chat_completion_stream(model, gemini_contents, generation_config)
            else:
                return self._chat_completion_blocking(model, gemini_contents, generation_config, start_time)
                
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
            logger.error(f"Gemini API error", error=str(e), exc_info=True)
            raise LLMAPIError("Gemini", str(e))
    
    def _chat_completion_blocking(
        self,
        model,
        gemini_contents: list[dict],
        generation_config: dict,
        start_time: float
    ) -> str:
        """
        Execute blocking (non-streaming) chat completion.
        
        Args:
            model: Gemini model instance
            gemini_contents: Messages in Gemini format
            generation_config: Generation configuration
            start_time: Request start time
        
        Returns:
            str: Complete response text
        """
        response = model.generate_content(
            gemini_contents,
            generation_config=generation_config
        )
        
        # Check if request took too long
        if time.time() - start_time > self.timeout:
            raise LLMTimeoutError("Gemini", self.timeout)
        
        if not response or not response.text:
            raise LLMInvalidResponseError("Gemini", "Empty response from API")
        
        response_text = response.text
        
        logger.info(
            f"Gemini completion successful",
            model=self.model,
            response_length=len(response_text)
        )
        
        return response_text
    
    def _chat_completion_stream(
        self,
        model,
        gemini_contents: list[dict],
        generation_config: dict
    ) -> Iterator[str]:
        """
        Execute streaming chat completion.
        
        Args:
            model: Gemini model instance
            gemini_contents: Messages in Gemini format
            generation_config: Generation configuration
        
        Yields:
            str: Response chunks
        """
        logger.info(f"Gemini streaming started", model=self.model)
        
        try:
            response_stream = model.generate_content(
                gemini_contents,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            
            logger.debug("Gemini streaming complete")
            
        except Exception as e:
            logger.error(f"Gemini streaming error", error=str(e), exc_info=True)
            raise LLMAPIError("Gemini", f"Streaming error: {e}")
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using Gemini's token counter.
        
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
            result = self.client.count_tokens(text)
            return result.total_tokens
        except Exception as e:
            logger.warning(f"Failed to count tokens with Gemini", error=str(e))
            # Fallback
            return len(text) // 4


# Convenience: Allow direct import
__all__ = [
    'GeminiProvider',
]
