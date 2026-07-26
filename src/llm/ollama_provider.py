"""
Ollama LLM Provider Module

This module implements the Ollama provider for local LLM inference.
Ollama allows running LLMs locally without API keys.

Author: TechFlow AI Project
License: MIT
"""

import requests
from typing import Optional, Iterator

from src.llm.base_provider import BaseProvider
from src.utils import (
    get_logger,
    LLMAPIError,
    LLMTimeoutError,
    LLMInvalidResponseError
)


logger = get_logger()


class OllamaProvider(BaseProvider):
    """
    Ollama LLM provider for local inference.
    
    Features:
    - Local LLM inference (no API key required)
    - Streaming support
    - Multiple models support (llama3.2, mistral, etc.)
    - Free to use
    
    Requirements:
    - Ollama must be installed and running locally
    - Default URL: http://localhost:11434
    """
    
    def __init__(
        self,
        model: str = 'llama3.2',
        base_url: str = 'http://localhost:11434',
        timeout: int = 60,
        **kwargs
    ):
        """
        Initialize Ollama provider.
        
        Args:
            model: Ollama model name (e.g., 'llama3.2', 'mistral')
            base_url: Ollama API base URL
            timeout: Request timeout in seconds
            **kwargs: Additional parameters
        
        Example:
            >>> provider = OllamaProvider(model='llama3.2')
            >>> response = provider.chat_completion([
            ...     {'role': 'user', 'content': 'Hello!'}
            ... ])
        """
        super().__init__(model=model, base_url=base_url, **kwargs)
        self.timeout = timeout
        logger.info(f"OllamaProvider initialized", model=model, base_url=base_url)
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "Ollama"
    
    def is_available(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            bool: True if Ollama is available
        
        Example:
            >>> provider = OllamaProvider()
            >>> if provider.is_available():
            ...     print("Ollama is running")
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            return False
    
    def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Generate chat completion using Ollama.
        
        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens (ignored by Ollama)
            stream: Enable streaming
            **kwargs: Additional parameters
        
        Returns:
            str or Iterator[str]: Response text or stream
        
        Raises:
            LLMAPIError: If API call fails
            LLMTimeoutError: If request times out
            LLMInvalidResponseError: If response is invalid
        
        Example:
            >>> provider = OllamaProvider()
            >>> messages = [{'role': 'user', 'content': 'Hello!'}]
            >>> response = provider.chat_completion(messages)
            >>> print(response)
        """
        # Validate inputs
        self.validate_messages(messages)
        self.validate_temperature(temperature)
        
        # Build request payload
        payload = {
            'model': self.model,
            'messages': messages,
            'stream': stream,
            'options': {
                'temperature': temperature
            }
        }
        
        # Add max_tokens if specified (Ollama uses 'num_predict')
        if max_tokens:
            payload['options']['num_predict'] = max_tokens
        
        # Add any additional options
        payload['options'].update(kwargs)
        
        logger.debug(
            f"Ollama chat completion request",
            model=self.model,
            num_messages=len(messages),
            stream=stream
        )
        
        try:
            if stream:
                return self._chat_completion_stream(payload)
            else:
                return self._chat_completion_blocking(payload)
                
        except requests.Timeout:
            logger.error(f"Ollama request timeout", model=self.model)
            raise LLMTimeoutError("Ollama", self.timeout)
        
        except requests.RequestException as e:
            logger.error(f"Ollama API error", error=str(e), exc_info=True)
            raise LLMAPIError("Ollama", str(e))
        
        except Exception as e:
            logger.error(f"Unexpected Ollama error", error=str(e), exc_info=True)
            raise LLMAPIError("Ollama", f"Unexpected error: {e}")
    
    def _chat_completion_blocking(self, payload: dict) -> str:
        """
        Execute blocking (non-streaming) chat completion.
        
        Args:
            payload: Request payload
        
        Returns:
            str: Complete response text
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        
        try:
            data = response.json()
            
            if 'message' not in data or 'content' not in data['message']:
                raise LLMInvalidResponseError(
                    "Ollama",
                    "Response missing 'message.content' field"
                )
            
            response_text = data['message']['content']
            
            logger.info(
                f"Ollama completion successful",
                model=self.model,
                response_length=len(response_text)
            )
            
            return response_text
            
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to parse Ollama response", error=str(e))
            raise LLMInvalidResponseError("Ollama", f"Invalid JSON response: {e}")
    
    def _chat_completion_stream(self, payload: dict) -> Iterator[str]:
        """
        Execute streaming chat completion.
        
        Args:
            payload: Request payload
        
        Yields:
            str: Response chunks
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=self.timeout,
            stream=True
        )
        
        response.raise_for_status()
        
        logger.info(f"Ollama streaming started", model=self.model)
        
        try:
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        data = json.loads(line)
                        
                        if 'message' in data and 'content' in data['message']:
                            chunk = data['message']['content']
                            if chunk:
                                yield chunk
                        
                        # Check if this is the final message
                        if data.get('done', False):
                            logger.debug("Ollama streaming complete")
                            break
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse stream chunk", error=str(e))
                        continue
                        
        except Exception as e:
            logger.error(f"Ollama streaming error", error=str(e), exc_info=True)
            raise LLMAPIError("Ollama", f"Streaming error: {e}")
    
    def list_models(self) -> list[str]:
        """
        List available Ollama models.
        
        Returns:
            list[str]: List of model names
        
        Example:
            >>> provider = OllamaProvider()
            >>> models = provider.list_models()
            >>> print(models)
            ['llama3.2', 'mistral', 'codellama']
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            logger.debug(f"Listed {len(models)} Ollama models")
            return models
            
        except Exception as e:
            logger.error(f"Failed to list Ollama models", error=str(e))
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """
        Pull/download a model from Ollama library.
        
        Args:
            model_name: Name of model to pull (e.g., 'llama3.2')
        
        Returns:
            bool: True if successful
        
        Example:
            >>> provider = OllamaProvider()
            >>> provider.pull_model('llama3.2')
            True
        """
        try:
            logger.info(f"Pulling Ollama model", model=model_name)
            
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={'name': model_name},
                timeout=300  # 5 minutes for model download
            )
            response.raise_for_status()
            
            logger.info(f"Model pulled successfully", model=model_name)
            return True
            
        except Exception as e:
            logger.error(f"Failed to pull model", model=model_name, error=str(e))
            return False


# Convenience: Allow direct import
__all__ = [
    'OllamaProvider',
]
