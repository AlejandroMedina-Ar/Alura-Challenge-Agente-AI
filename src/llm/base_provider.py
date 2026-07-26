"""
Base LLM Provider Module

This module defines the abstract base class for all LLM providers.
All provider implementations must inherit from BaseProvider.

Author: TechFlow Solutions Project
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Optional, Iterator

from src.utils import get_logger


logger = get_logger()


class BaseProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    All LLM provider implementations (Ollama, OpenRouter, etc.) must inherit
    from this class and implement all abstract methods.
    
    Features:
    - Standardized interface for all providers
    - Chat completion with streaming support
    - Configuration management
    - Error handling
    """
    
    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize LLM provider.
        
        Args:
            model: Model identifier (e.g., 'llama3.2', 'gpt-4')
            base_url: API base URL (optional)
            api_key: API key for authentication (optional)
            **kwargs: Additional provider-specific parameters
        """
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.config = kwargs
        
        logger.debug(
            f"BaseProvider initialized",
            provider=self.__class__.__name__,
            model=model
        )
    
    @abstractmethod
    def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Generate chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate (optional)
            stream: If True, return generator for streaming
            **kwargs: Additional provider-specific parameters
        
        Returns:
            str: Complete response text (if stream=False)
            Iterator[str]: Response chunks generator (if stream=True)
        
        Raises:
            LLMAPIError: If API call fails
            LLMTimeoutError: If request times out
            LLMInvalidResponseError: If response is invalid
        
        Example:
            >>> provider = SomeProvider(model='model-name')
            >>> messages = [
            ...     {'role': 'system', 'content': 'You are a helpful assistant'},
            ...     {'role': 'user', 'content': 'Hello!'}
            ... ]
            >>> response = provider.chat_completion(messages)
            >>> print(response)
            'Hello! How can I help you today?'
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and configured correctly.
        
        Returns:
            bool: True if provider can be used
        
        Example:
            >>> provider = SomeProvider(model='model-name')
            >>> if provider.is_available():
            ...     response = provider.chat_completion(messages)
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get human-readable provider name.
        
        Returns:
            str: Provider name (e.g., 'Ollama', 'OpenRouter')
        
        Example:
            >>> provider = SomeProvider(model='model-name')
            >>> print(provider.get_provider_name())
            'Ollama'
        """
        pass
    
    def validate_messages(self, messages: list[dict]) -> None:
        """
        Validate message format.
        
        Args:
            messages: List of message dicts
        
        Raises:
            ValueError: If messages format is invalid
        
        Example:
            >>> provider = SomeProvider(model='model-name')
            >>> messages = [{'role': 'user', 'content': 'Hello'}]
            >>> provider.validate_messages(messages)  # OK
        """
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        
        if len(messages) == 0:
            raise ValueError("Messages list cannot be empty")
        
        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"Message {i} must be a dict")
            
            if 'role' not in msg:
                raise ValueError(f"Message {i} missing 'role' field")
            
            if 'content' not in msg:
                raise ValueError(f"Message {i} missing 'content' field")
            
            if msg['role'] not in ['system', 'user', 'assistant']:
                raise ValueError(
                    f"Message {i} has invalid role: {msg['role']}. "
                    "Must be 'system', 'user', or 'assistant'"
                )
    
    def validate_temperature(self, temperature: float) -> None:
        """
        Validate temperature parameter.
        
        Args:
            temperature: Temperature value
        
        Raises:
            ValueError: If temperature is out of range
        
        Example:
            >>> provider = SomeProvider(model='model-name')
            >>> provider.validate_temperature(0.7)  # OK
            >>> provider.validate_temperature(3.0)  # ValueError
        """
        if not 0.0 <= temperature <= 2.0:
            raise ValueError(
                f"Temperature must be between 0.0 and 2.0, got {temperature}"
            )
    
    def format_error_message(self, error: Exception) -> str:
        """
        Format error message for logging/display.
        
        Args:
            error: Exception that occurred
        
        Returns:
            str: Formatted error message
        
        Example:
            >>> provider = SomeProvider(model='model-name')
            >>> try:
            ...     # Some operation
            ...     pass
            ... except Exception as e:
            ...     msg = provider.format_error_message(e)
            ...     print(msg)
        """
        provider_name = self.get_provider_name()
        return f"{provider_name} error: {str(error)}"
    
    def __repr__(self) -> str:
        """
        String representation of provider.
        
        Returns:
            str: Provider representation
        
        Example:
            >>> provider = SomeProvider(model='llama3.2')
            >>> print(provider)
            SomeProvider(model='llama3.2')
        """
        return f"{self.__class__.__name__}(model='{self.model}')"


# Convenience: Allow direct import
__all__ = [
    'BaseProvider',
]
