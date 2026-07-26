"""
LLM Package

This package provides LLM provider implementations.

Modules:
- base_provider: Abstract base class for all providers
- ollama_provider: Local Ollama LLM provider
- openrouter_provider: OpenRouter API provider

Author: TechFlow AI Project
License: MIT
"""

from .base_provider import BaseProvider
from .ollama_provider import OllamaProvider
from .openrouter_provider import OpenRouterProvider


__all__ = [
    # Base class
    'BaseProvider',
    
    # Providers
    'OllamaProvider',
    'OpenRouterProvider',
]
