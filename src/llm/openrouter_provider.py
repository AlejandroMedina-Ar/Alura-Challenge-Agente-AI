"""
OpenRouter Provider

OpenRouter implementation.
"""

from .base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):

    """OpenRouter provider."""

    def generate(self, prompt: str) -> str:
        raise NotImplementedError
