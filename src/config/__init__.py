"""
Configuration Package

This package provides centralized configuration management for the TechFlow AI application.

Modules:
    - settings: Environment variables and application settings
    - paths: File system paths configuration
    - constants: Application constants and enums

Usage:
    >>> from src.config import get_settings, get_paths
    >>> settings = get_settings()
    >>> paths = get_paths()
    >>> print(settings.GEMINI_MODEL)
    >>> print(paths.DOCUMENTS_DIR)

Author: TechFlow AI Project
License: MIT
"""

# Import main functions for convenient access
from .settings import (
    Settings,
    ConfigurationError,
    get_settings,
    reload_settings
)

from .paths import (
    Paths,
    PathConfigurationError,
    get_paths,
    reload_paths
)

from .constants import (
    # App metadata
    APP_NAME,
    APP_FULL_NAME,
    APP_VERSION,
    APP_TAGLINE,
    
    # Enums
    FileFormat,
    LLMProvider,
    View,
    Theme,
    
    # Classes
    SessionKey,
    MetadataField,
    ErrorMessage,
    SuccessMessage,
    FileSizeLimit,
    
    # Important constants
    SUPPORTED_EXTENSIONS,
    FILE_SIZE_LIMITS,
    MIN_DOCUMENTS_FOR_RAG,
    FALLBACK_DURATION_SECONDS,
    
    # Utility functions
    get_file_format,
    format_file_size,
    get_supported_extensions_list,
    get_supported_formats_display,
)


# Package version
__version__ = APP_VERSION

# Public API
__all__ = [
    # Settings
    'Settings',
    'ConfigurationError',
    'get_settings',
    'reload_settings',
    
    # Paths
    'Paths',
    'PathConfigurationError',
    'get_paths',
    'reload_paths',
    
    # Constants - App info
    'APP_NAME',
    'APP_FULL_NAME',
    'APP_VERSION',
    'APP_TAGLINE',
    
    # Constants - Enums
    'FileFormat',
    'LLMProvider',
    'View',
    'Theme',
    
    # Constants - Classes
    'SessionKey',
    'MetadataField',
    'ErrorMessage',
    'SuccessMessage',
    'FileSizeLimit',
    
    # Constants - Dicts
    'SUPPORTED_EXTENSIONS',
    'FILE_SIZE_LIMITS',
    'MIN_DOCUMENTS_FOR_RAG',
    'FALLBACK_DURATION_SECONDS',
    
    # Constants - Functions
    'get_file_format',
    'format_file_size',
    'get_supported_extensions_list',
    'get_supported_formats_display',
]
