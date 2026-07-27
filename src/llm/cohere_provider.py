"""
Cohere LLM Provider Module

This module implements the Cohere provider for the TechFlow Solutions project.
Uses Cohere Command-R7B (FREE tier) as the fallback LLM provider.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional, Iterator
import time

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False

from src.llm.base_provider import BaseProvider
from src.utils import (
    get_logger,
    LLMAPIError,
    LLMTimeoutError,
    LLMInvalidResponseError,
    LLMRateLimitError
)


logger = get_logger()


class CohereProvider(BaseProvider):
    """
    Cohere LLM provider (free tier).
    
    Features:
    - Command-R7B model (FREE tier, Dec 2024)
    - Streaming support
    - Good context window (128K tokens)
    - Good multilingual support
    
    Requirements:
    - Cohere SDK (cohere)
    - Cohere API key (FREE tier available)
    """
    
    def __init__(
        self,
        model: str = 'command-r7b-12-2024',  # FREE tier model
        api_key: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        """
        Initialize Cohere provider.
        
        Args:
            model: Cohere model name (default: command-r7b-12-2024 - FREE tier)
            api_key: Cohere API key
            timeout: Request timeout in seconds
            **kwargs: Additional parameters
        
        Note:
            FREE tier models:
            - command-r7b-12-2024 (recommended, latest)
            - command-r (deprecated Sept 2025, DO NOT USE)
            
            PAID tier models:
            - command-r-plus (better quality, paid only)
        
        Example:
            >>> provider = CohereProvider(api_key='...')
            >>> response = provider.chat_completion([
            ...     {'role': 'user', 'content': 'Hello!'}
            ... ])
        """
        super().__init__(model=model, api_key=api_key, **kwargs)
        self.timeout = timeout
        self.client = None
        
        if COHERE_AVAILABLE and api_key:
            try:
                self.client = cohere.Client(api_key=api_key)
                logger.info(f"CohereProvider initialized", model=model)
            except Exception as e:
                logger.error(f"Failed to initialize Cohere client", error=str(e))
        else:
            if not COHERE_AVAILABLE:
                logger.warning("cohere package not available")
            else:
                logger.warning("Cohere API key not provided")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "Cohere"
    
    def is_available(self) -> bool:
        """
        Check if Cohere is available and configured correctly.
        
        Returns:
            bool: True if provider can be used
        
        Example:
            >>> provider = CohereProvider(api_key='...')
            >>> if provider.is_available():
            ...     print("Cohere is ready")
        """
        if not COHERE_AVAILABLE:
            logger.debug("Cohere not available - SDK not installed")
            return False
        
        if not self.api_key or not self.client:
            logger.debug("Cohere not available - API key not configured")
            return False
        
        return True
    
    def _convert_messages_to_cohere_format(self, messages: list[dict]) -> tuple[str, str, list[dict]]:
        """
        Convert OpenAI-style messages to Cohere format.
        
        Cohere uses:
        - preamble (system message)
        - message (current user message)
        - chat_history (previous messages)
        
        Args:
            messages: OpenAI-style messages
        
        Returns:
            tuple: (preamble, current_message, chat_history)
        """
        preamble = ""
        chat_history = []
        current_message = ""
        
        for i, msg in enumerate(messages):
            role = msg['role']
            content = msg['content']
            
            if role == 'system':
                preamble = content
            elif i == len(messages) - 1 and role == 'user':
                # Last user message is the current query
                current_message = content
            elif role == 'user':
                chat_history.append({
                    'role': 'USER',
                    'message': content
                })
            elif role == 'assistant':
                chat_history.append({
                    'role': 'CHATBOT',
                    'message': content
                })
        
        return preamble, current_message, chat_history
    
    def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Generate chat completion using Cohere.
        
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
            >>> provider = CohereProvider(api_key='...')
            >>> messages = [{'role': 'user', 'content': 'Hello!'}]
            >>> response = provider.chat_completion(messages)
            >>> print(response)
        """
        # Validate inputs
        self.validate_messages(messages)
        self.validate_temperature(temperature)
        
        if not self.client:
            raise LLMAPIError("Cohere", "Provider not initialized - missing API key")
        
        # Convert to Cohere format
        preamble, current_message, chat_history = self._convert_messages_to_cohere_format(messages)
        
        if not current_message:
            raise LLMInvalidResponseError("Cohere", "No user message found")
        
        # Build request parameters
        params = {
            'model': self.model,
            'message': current_message,
            'temperature': temperature,
        }
        
        if preamble:
            params['preamble'] = preamble
        
        if chat_history:
            params['chat_history'] = chat_history
        
        if max_tokens:
            params['max_tokens'] = max_tokens
        
        logger.debug(
            f"Cohere chat completion request",
            model=self.model,
            num_messages=len(messages),
            stream=stream
        )
        
        try:
            start_time = time.time()
            
            if stream:
                return self._chat_completion_stream(params, start_time)
            else:
                return self._chat_completion_blocking(params, start_time)
                
        except Exception as e:
            error_str = str(e).lower()
            
            # Check for timeout
            if 'timeout' in error_str or (time.time() - start_time) > self.timeout:
                logger.error(f"Cohere request timeout", model=self.model)
                raise LLMTimeoutError("Cohere", self.timeout)
            
            # Check for rate limit
            if 'rate limit' in error_str or '429' in error_str or 'too many requests' in error_str:
                logger.warning(f"Cohere rate limit exceeded")
                raise LLMRateLimitError("Cohere")
            
            # General API error
            logger.error(f"Cohere API error", error=str(e), exc_info=True)
            raise LLMAPIError("Cohere", str(e))
    
    def _chat_completion_blocking(
        self,
        params: dict,
        start_time: float
    ) -> str:
        """
        Execute blocking (non-streaming) chat completion.
        
        Args:
            params: Request parameters
            start_time: Request start time
        
        Returns:
            str: Complete response text
        """
        response = self.client.chat(**params)
        
        # Check if request took too long
        if time.time() - start_time > self.timeout:
            raise LLMTimeoutError("Cohere", self.timeout)
        
        if not response or not response.text:
            raise LLMInvalidResponseError("Cohere", "Empty response from API")
        
        response_text = response.text
        
        logger.info(
            f"Cohere completion successful",
            model=self.model,
            response_length=len(response_text)
        )
        
        return response_text
    
    def _chat_completion_stream(
        self,
        params: dict,
        start_time: float
    ) -> Iterator[str]:
        """
        Execute streaming chat completion.
        
        Args:
            params: Request parameters
            start_time: Request start time
        
        Yields:
            str: Response chunks
        """
        logger.info(f"Cohere streaming started", model=self.model)
        
        try:
            response_stream = self.client.chat_stream(**params)
            
            for event in response_stream:
                # Check timeout
                if time.time() - start_time > self.timeout:
                    raise LLMTimeoutError("Cohere", self.timeout)
                
                if hasattr(event, 'event_type'):
                    if event.event_type == 'text-generation':
                        if hasattr(event, 'text') and event.text:
                            yield event.text
                    elif event.event_type == 'stream-end':
                        logger.debug("Cohere streaming complete")
                        break
            
        except LLMTimeoutError:
            raise
        except Exception as e:
            logger.error(f"Cohere streaming error", error=str(e), exc_info=True)
            raise LLMAPIError("Cohere", f"Streaming error: {e}")
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using Cohere's tokenizer.
        
        Args:
            text: Text to count tokens for
        
        Returns:
            int: Token count
        
        Example:
            >>> provider = CohereProvider(api_key='...')
            >>> count = provider.count_tokens("Hello, world!")
            >>> print(count)
            4
        """
        if not self.client:
            # Fallback to approximate count (4 chars per token)
            return len(text) // 4
        
        try:
            result = self.client.tokenize(text=text, model=self.model)
            return len(result.tokens)
        except Exception as e:
            logger.warning(f"Failed to count tokens with Cohere", error=str(e))
            # Fallback
            return len(text) // 4


# Convenience: Allow direct import
__all__ = [
    'CohereProvider',
]


# Singleton instance
_cohere_provider_instance: Optional[CohereProvider] = None


def get_cohere_provider() -> CohereProvider:
    """
    Get singleton CohereProvider instance.
    
    Returns:
        CohereProvider: Singleton Cohere provider instance
    
    Example:
        >>> provider = get_cohere_provider()
        >>> response = provider.chat_completion(messages)
    """
    global _cohere_provider_instance
    
    if _cohere_provider_instance is None:
        from src.config import get_settings
        settings = get_settings()
        
        _cohere_provider_instance = CohereProvider(
            model=settings.COHERE_MODEL,
            api_key=settings.COHERE_API_KEY
        )
        logger.debug("CohereProvider singleton created")
    
    return _cohere_provider_instance
