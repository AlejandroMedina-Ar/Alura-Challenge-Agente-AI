"""
Ollama Provider

Local Ollama implementation.
"""

from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    """Ollama provider."""

    def generate(self, prompt: str) -> str:
        raise NotImplementedError
