"""
OpenRouter LLM Provider Module

This module implements the OpenRouter provider for accessing multiple LLMs.
OpenRouter provides access to free-tier models like Google Gemini 2.0 Flash.

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
    LLMInvalidResponseError,
    LLMRateLimitError
)


logger = get_logger()


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter LLM provider.
    
    Features:
    - Access to multiple LLM models
    - Free-tier models available (e.g., google/gemini-2.0-flash-exp:free)
    - Streaming support
    - Rate limit handling
    
    Requirements:
    - OpenRouter API key (free tier available)
    - Model must include ':free' suffix for free models
    """
    
    def __init__(
        self,
        model: str = 'google/gemini-2.0-flash-exp:free',
        api_key: Optional[str] = None,
        base_url: str = 'https://openrouter.ai/api/v1',
        timeout: int = 60,
        **kwargs
    ):
        """
        Initialize OpenRouter provider.
        
        Args:
            model: OpenRouter model identifier
            api_key: OpenRouter API key
            base_url: API base URL
            timeout: Request timeout in seconds
            **kwargs: Additional parameters
        
        Example:
            >>> provider = OpenRouterProvider(
            ...     model='google/gemini-2.0-flash-exp:free',
            ...     api_key='sk-or-v1-...'
            ... )
            >>> response = provider.chat_completion([
            ...     {'role': 'user', 'content': 'Hello!'}
            ... ])
        """
        super().__init__(model=model, base_url=base_url, api_key=api_key, **kwargs)
        self.timeout = timeout
        logger.info(
            f"OpenRouterProvider initialized",
            model=model,
            has_api_key=bool(api_key)
        )
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "OpenRouter"
    
    def is_available(self) -> bool:
        """
        Check if OpenRouter is available and API key is set.
        
        Returns:
            bool: True if provider can be used
        
        Example:
            >>> provider = OpenRouterProvider(api_key='sk-or-v1-...')
            >>> if provider.is_available():
            ...     print("OpenRouter is ready")
        """
        if not self.api_key:
            logger.debug("OpenRouter API key not set")
            return False
        
        try:
            # Test API connectivity
            response = requests.get(
                f"{self.base_url}/models",
                headers=self._get_headers(),
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"OpenRouter availability check failed: {e}")
            return False
    
    def _get_headers(self) -> dict:
        """
        Get HTTP headers for OpenRouter API.
        
        Returns:
            dict: Request headers
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://techflow-ai.local',  # Required by OpenRouter
            'X-Title': 'TechFlow AI RAG Agent'  # Optional, for tracking
        }
        return headers
    
    def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Generate chat completion using OpenRouter.
        
        Args:
            messages: List of message dicts
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
            >>> provider = OpenRouterProvider(api_key='sk-or-v1-...')
            >>> messages = [{'role': 'user', 'content': 'Hello!'}]
            >>> response = provider.chat_completion(messages)
            >>> print(response)
        """
        # Validate inputs
        self.validate_messages(messages)
        self.validate_temperature(temperature)
        
        if not self.api_key:
            raise LLMAPIError("OpenRouter", "API key not set")
        
        # Build request payload
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'stream': stream
        }
        
        # Add max_tokens if specified
        if max_tokens:
            payload['max_tokens'] = max_tokens
        
        # Add any additional parameters
        payload.update(kwargs)
        
        logger.debug(
            f"OpenRouter chat completion request",
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
            logger.error(f"OpenRouter request timeout", model=self.model)
            raise LLMTimeoutError("OpenRouter", self.timeout)
        
        except requests.HTTPError as e:
            # Check for rate limit (429)
            if e.response.status_code == 429:
                retry_after = e.response.headers.get('Retry-After')
                logger.warning(f"OpenRouter rate limit exceeded")
                raise LLMRateLimitError(
                    "OpenRouter",
                    int(retry_after) if retry_after else None
                )
            else:
                logger.error(f"OpenRouter HTTP error", status=e.response.status_code)
                raise LLMAPIError("OpenRouter", f"HTTP {e.response.status_code}")
        
        except requests.RequestException as e:
            logger.error(f"OpenRouter API error", error=str(e), exc_info=True)
            raise LLMAPIError("OpenRouter", str(e))
        
        except Exception as e:
            logger.error(f"Unexpected OpenRouter error", error=str(e), exc_info=True)
            raise LLMAPIError("OpenRouter", f"Unexpected error: {e}")
    
    def _chat_completion_blocking(self, payload: dict) -> str:
        """
        Execute blocking (non-streaming) chat completion.
        
        Args:
            payload: Request payload
        
        Returns:
            str: Complete response text
        """
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self._get_headers(),
            json=payload,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        
        try:
            data = response.json()
            
            if 'choices' not in data or len(data['choices']) == 0:
                raise LLMInvalidResponseError(
                    "OpenRouter",
                    "Response missing 'choices' field"
                )
            
            choice = data['choices'][0]
            
            if 'message' not in choice or 'content' not in choice['message']:
                raise LLMInvalidResponseError(
                    "OpenRouter",
                    "Response missing 'message.content' field"
                )
            
            response_text = choice['message']['content']
            
            logger.info(
                f"OpenRouter completion successful",
                model=self.model,
                response_length=len(response_text),
                finish_reason=choice.get('finish_reason')
            )
            
            return response_text
            
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Failed to parse OpenRouter response", error=str(e))
            raise LLMInvalidResponseError("OpenRouter", f"Invalid JSON response: {e}")
    
    def _chat_completion_stream(self, payload: dict) -> Iterator[str]:
        """
        Execute streaming chat completion.
        
        Args:
            payload: Request payload
        
        Yields:
            str: Response chunks
        """
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self._get_headers(),
            json=payload,
            timeout=self.timeout,
            stream=True
        )
        
        response.raise_for_status()
        
        logger.info(f"OpenRouter streaming started", model=self.model)
        
        try:
            import json
            
            for line in response.iter_lines():
                if line:
                    # OpenRouter uses SSE format: "data: {...}"
                    line_str = line.decode('utf-8')
                    
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove "data: " prefix
                        
                        # Skip [DONE] message
                        if data_str.strip() == '[DONE]':
                            logger.debug("OpenRouter streaming complete")
                            break
                        
                        try:
                            data = json.loads(data_str)
                            
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                chunk = delta.get('content')
                                
                                if chunk:
                                    yield chunk
                                    
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse stream chunk", error=str(e))
                            continue
                            
        except Exception as e:
            logger.error(f"OpenRouter streaming error", error=str(e), exc_info=True)
            raise LLMAPIError("OpenRouter", f"Streaming error: {e}")
    
    def list_models(self) -> list[dict]:
        """
        List available OpenRouter models.
        
        Returns:
            list[dict]: List of model information dicts
        
        Example:
            >>> provider = OpenRouterProvider(api_key='sk-or-v1-...')
            >>> models = provider.list_models()
            >>> for model in models:
            ...     print(model['id'], '-', model.get('name'))
        """
        if not self.api_key:
            logger.warning("Cannot list models - API key not set")
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            models = data.get('data', [])
            
            logger.debug(f"Listed {len(models)} OpenRouter models")
            return models
            
        except Exception as e:
            logger.error(f"Failed to list OpenRouter models", error=str(e))
            return []


# Convenience: Allow direct import
__all__ = [
    'OpenRouterProvider',
]
