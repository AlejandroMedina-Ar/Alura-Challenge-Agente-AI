"""
LLM Package

This package provides LLM provider implementations.

Modules:
- base_provider: Abstract base class for all providers
- gemini_provider: Google Gemini 2.0 Flash provider (primary)
- cohere_provider: Cohere Command-R provider (fallback)

Author: TechFlow AI Project
License: MIT
"""

from .base_provider import BaseProvider
from .gemini_provider import GeminiProvider
from .cohere_provider import CohereProvider


__all__ = [
    # Base class
    'BaseProvider',
    
    # Providers
    'GeminiProvider',
    'CohereProvider',
]
