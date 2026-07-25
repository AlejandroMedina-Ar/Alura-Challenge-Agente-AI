"""
Base Provider

Abstract interface implemented by all LLM providers.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    """Abstract language model provider."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response."""
        raise NotImplementedError
