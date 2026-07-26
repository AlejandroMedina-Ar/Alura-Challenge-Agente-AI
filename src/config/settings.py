"""
Configuration Settings Module

This module handles loading and validation of environment variables and application settings.
All configuration is loaded from .env file and validated at startup.

Author: TechFlow Solutions Project
License: MIT
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing required values."""
    pass


class Settings:
    """
    Application settings loaded from environment variables.
    
    This class loads configuration from .env file and provides validated
    access to all application settings.
    
    Attributes:
        GEMINI_API_KEY: Google Gemini API key for LLM
        COHERE_API_KEY: Cohere API key for fallback LLM
        GEMINI_MODEL: Gemini model name to use
        COHERE_MODEL: Cohere model name to use
        EMBEDDING_MODEL: HuggingFace embedding model name
        ADMIN_PASSWORD_HASH: Bcrypt hash of admin password
        CHUNK_SIZE: Size of text chunks for RAG
        CHUNK_OVERLAP: Overlap between chunks
        TOP_K_RESULTS: Number of results to retrieve from vector store
        TEMPERATURE: LLM temperature for generation
        MAX_CONTEXT_TOKENS: Maximum tokens for context window
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    
    def __init__(self):
        """Initialize settings by loading from .env file."""
        self._load_env()
        self._load_settings()
        self._validate()
    
    def _load_env(self) -> None:
        """
        Load environment variables from .env file.
        
        Searches for .env file starting from current directory up to project root.
        
        Raises:
            ConfigurationError: If .env file is not found
        """
        # Find project root (directory containing .env)
        current_dir = Path(__file__).resolve().parent
        
        # Search for .env in parent directories (up to 5 levels)
        env_file = None
        for _ in range(5):
            potential_env = current_dir / '.env'
            if potential_env.exists():
                env_file = potential_env
                break
            current_dir = current_dir.parent
        
        if env_file is None:
            raise ConfigurationError(
                ".env file not found. Please create a .env file in the project root. "
                "See .env.example for template."
            )
        
        # Load environment variables
        load_dotenv(dotenv_path=env_file, override=True)
    
    def _load_settings(self) -> None:
        """Load all settings from environment variables with defaults."""
        
        # === API Keys (Required) ===
        self.GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
        self.COHERE_API_KEY: str = os.getenv('COHERE_API_KEY', '')
        
        # === Model Names ===
        self.GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.COHERE_MODEL: str = os.getenv('COHERE_MODEL', 'command-r-plus-08-2024')
        self.EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-base')
        
        # === Authentication ===
        self.ADMIN_PASSWORD_HASH: str = os.getenv('ADMIN_PASSWORD_HASH', '')
        # If no hash provided, use plain password (will be hashed on first login)
        self.ADMIN_PASSWORD: Optional[str] = os.getenv('ADMIN_PASSWORD', None)
        
        # === RAG Configuration ===
        self.CHUNK_SIZE: int = int(os.getenv('CHUNK_SIZE', '1000'))
        self.CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP', '200'))
        self.TOP_K_RESULTS: int = int(os.getenv('TOP_K_RESULTS', '5'))
        
        # === LLM Parameters ===
        self.TEMPERATURE: float = float(os.getenv('TEMPERATURE', '0.7'))
        self.MAX_CONTEXT_TOKENS: int = int(os.getenv('MAX_CONTEXT_TOKENS', '8000'))
        self.MAX_OUTPUT_TOKENS: int = int(os.getenv('MAX_OUTPUT_TOKENS', '2000'))
        
        # === Vector Store ===
        self.COLLECTION_NAME: str = os.getenv('COLLECTION_NAME', 'techflow_knowledge')
        
        # === Logging ===
        self.LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # === Feature Flags ===
        self.ENABLE_STREAMING: bool = os.getenv('ENABLE_STREAMING', 'true').lower() == 'true'
        self.ENABLE_FALLBACK: bool = os.getenv('ENABLE_FALLBACK', 'true').lower() == 'true'
    
    def _validate(self) -> None:
        """
        Validate all required settings are present and valid.
        
        Raises:
            ConfigurationError: If any required setting is missing or invalid
        """
        errors = []
        
        # Validate required API keys
        if not self.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required but not set")
        
        if not self.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is required but not set")
        
        # Validate authentication
        if not self.ADMIN_PASSWORD_HASH and not self.ADMIN_PASSWORD:
            errors.append(
                "Either ADMIN_PASSWORD_HASH or ADMIN_PASSWORD must be set. "
                "Use ADMIN_PASSWORD for first-time setup."
            )
        
        # Validate numeric ranges
        if self.CHUNK_SIZE < 100 or self.CHUNK_SIZE > 5000:
            errors.append(f"CHUNK_SIZE must be between 100 and 5000, got {self.CHUNK_SIZE}")
        
        if self.CHUNK_OVERLAP < 0 or self.CHUNK_OVERLAP >= self.CHUNK_SIZE:
            errors.append(
                f"CHUNK_OVERLAP must be >= 0 and < CHUNK_SIZE, "
                f"got {self.CHUNK_OVERLAP} (CHUNK_SIZE={self.CHUNK_SIZE})"
            )
        
        if self.TOP_K_RESULTS < 1 or self.TOP_K_RESULTS > 20:
            errors.append(f"TOP_K_RESULTS must be between 1 and 20, got {self.TOP_K_RESULTS}")
        
        if self.TEMPERATURE < 0.0 or self.TEMPERATURE > 2.0:
            errors.append(f"TEMPERATURE must be between 0.0 and 2.0, got {self.TEMPERATURE}")
        
        if self.MAX_CONTEXT_TOKENS < 1000:
            errors.append(f"MAX_CONTEXT_TOKENS must be at least 1000, got {self.MAX_CONTEXT_TOKENS}")
        
        if self.MAX_OUTPUT_TOKENS < 100:
            errors.append(f"MAX_OUTPUT_TOKENS must be at least 100, got {self.MAX_OUTPUT_TOKENS}")
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.LOG_LEVEL not in valid_log_levels:
            errors.append(
                f"LOG_LEVEL must be one of {valid_log_levels}, got '{self.LOG_LEVEL}'"
            )
        
        # Raise all errors together
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ConfigurationError(error_msg)
    
    def get_summary(self) -> dict:
        """
        Get a summary of current settings (safe for logging - no secrets).
        
        Returns:
            dict: Dictionary with non-sensitive configuration values
        """
        return {
            'gemini_model': self.GEMINI_MODEL,
            'cohere_model': self.COHERE_MODEL,
            'embedding_model': self.EMBEDDING_MODEL,
            'chunk_size': self.CHUNK_SIZE,
            'chunk_overlap': self.CHUNK_OVERLAP,
            'top_k_results': self.TOP_K_RESULTS,
            'temperature': self.TEMPERATURE,
            'max_context_tokens': self.MAX_CONTEXT_TOKENS,
            'max_output_tokens': self.MAX_OUTPUT_TOKENS,
            'collection_name': self.COLLECTION_NAME,
            'log_level': self.LOG_LEVEL,
            'streaming_enabled': self.ENABLE_STREAMING,
            'fallback_enabled': self.ENABLE_FALLBACK,
            'gemini_api_key_set': bool(self.GEMINI_API_KEY),
            'cohere_api_key_set': bool(self.COHERE_API_KEY),
            'admin_auth_configured': bool(self.ADMIN_PASSWORD_HASH or self.ADMIN_PASSWORD)
        }
    
    def __repr__(self) -> str:
        """String representation (safe - no secrets)."""
        return f"Settings(model={self.GEMINI_MODEL}, embedding={self.EMBEDDING_MODEL})"


# Global settings instance (singleton pattern)
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton).
    
    This function ensures only one Settings instance exists throughout the application.
    
    Returns:
        Settings: The global settings instance
    
    Raises:
        ConfigurationError: If settings cannot be loaded or validated
    
    Example:
        >>> from src.config.settings import get_settings
        >>> settings = get_settings()
        >>> print(settings.GEMINI_MODEL)
        'gemini-2.0-flash-exp'
    """
    global _settings_instance
    
    if _settings_instance is None:
        _settings_instance = Settings()
    
    return _settings_instance


def reload_settings() -> Settings:
    """
    Reload settings from .env file.
    
    This is useful for testing or when .env file changes during runtime.
    
    Returns:
        Settings: New settings instance
    
    Example:
        >>> from src.config.settings import reload_settings
        >>> settings = reload_settings()
    """
    global _settings_instance
    _settings_instance = Settings()
    return _settings_instance


# Convenience: Allow direct import
__all__ = [
    'Settings',
    'ConfigurationError',
    'get_settings',
    'reload_settings'
]
