"""
Configuration Service Module

This module provides business logic for runtime configuration management.
Handles LLM, RAG, and UI configuration.

Author: TechFlow AI Project
License: MIT
"""

from src.storage import ConfigRepository
from src.utils import (
    get_logger,
    ConfigurationError,
    validate_chunk_parameters,
    validate_top_k,
    validate_temperature
)


logger = get_logger()


class ConfigurationService:
    """
    Service for configuration management.
    
    Features:
    - Get/set LLM configuration
    - Get/set RAG parameters
    - Get/set UI preferences
    - Validate configuration
    - Export/reset configuration
    """
    
    def __init__(self):
        """Initialize configuration service."""
        self.config_repo = ConfigRepository()
        logger.debug("ConfigurationService initialized")
    
    # ===== LLM Configuration =====
    
    def get_llm_config(self) -> dict:
        """
        Get current LLM configuration.
        
        Returns:
            dict: LLM config (provider, model, api_key)
        
        Example:
            >>> service = ConfigurationService()
            >>> config = service.get_llm_config()
            >>> print(config['provider'])
            'gemini'
        """
        return self.config_repo.get_llm_config()
    
    def update_llm_config(
        self,
        provider: str = None,
        model: str = None,
        api_key: str = None
    ) -> bool:
        """
        Update LLM configuration.
        
        Args:
            provider: LLM provider ('gemini' or 'cohere')
            model: Model name
            api_key: API key
        
        Returns:
            bool: True if updated successfully
        
        Example:
            >>> service = ConfigurationService()
            >>> service.update_llm_config(
            ...     provider='gemini',
            ...     model='gemini-1.5-flash',
            ...     api_key='AIza...'
            ... )
        """
        try:
            success = self.config_repo.set_llm_config(
                provider=provider,
                model=model,
                api_key=api_key
            )
            
            if success:
                logger.info("LLM configuration updated", provider=provider, model=model)
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update LLM config", error=str(e))
            return False
    
    def get_llm_provider(self) -> str:
        """Get current LLM provider."""
        config = self.get_llm_config()
        return config.get('provider', 'gemini')
    
    def get_llm_model(self) -> str:
        """Get current LLM model."""
        config = self.get_llm_config()
        return config.get('model', 'gemini-1.5-flash')
    
    # ===== RAG Configuration =====
    
    def get_rag_config(self) -> dict:
        """
        Get current RAG configuration.
        
        Returns:
            dict: RAG config (chunk_size, chunk_overlap, top_k, temperature)
        
        Example:
            >>> service = ConfigurationService()
            >>> config = service.get_rag_config()
            >>> print(config['chunk_size'])
            512
        """
        return self.config_repo.get_rag_config()
    
    def update_rag_config(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
        top_k: int = None,
        temperature: float = None
    ) -> bool:
        """
        Update RAG configuration with validation.
        
        Args:
            chunk_size: Text chunk size (128-2048)
            chunk_overlap: Overlap between chunks (0-512)
            top_k: Number of chunks to retrieve (1-20)
            temperature: LLM temperature (0.0-2.0)
        
        Returns:
            bool: True if updated successfully
        
        Raises:
            ConfigurationError: If validation fails
        
        Example:
            >>> service = ConfigurationService()
            >>> service.update_rag_config(
            ...     chunk_size=1000,
            ...     top_k=10,
            ...     temperature=0.7
            ... )
        """
        try:
            # Validate chunk parameters if both provided
            if chunk_size is not None and chunk_overlap is not None:
                validate_chunk_parameters(chunk_size, chunk_overlap)
            elif chunk_size is not None:
                # Get current overlap for validation
                current_config = self.get_rag_config()
                chunk_overlap_val = current_config.get('chunk_overlap', 50)
                validate_chunk_parameters(chunk_size, chunk_overlap_val)
            elif chunk_overlap is not None:
                # Get current size for validation
                current_config = self.get_rag_config()
                chunk_size_val = current_config.get('chunk_size', 512)
                validate_chunk_parameters(chunk_size_val, chunk_overlap)
            
            # Validate top_k
            if top_k is not None:
                validate_top_k(top_k)
            
            # Validate temperature
            if temperature is not None:
                validate_temperature(temperature)
            
            # Update configuration
            success = self.config_repo.set_rag_config(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                top_k=top_k,
                temperature=temperature
            )
            
            if success:
                logger.info(
                    "RAG configuration updated",
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    top_k=top_k,
                    temperature=temperature
                )
            
            return success
            
        except (ValueError, ConfigurationError) as e:
            logger.error(f"RAG config validation failed", error=str(e))
            raise ConfigurationError(f"Invalid RAG configuration: {e}")
    
    def get_chunk_size(self) -> int:
        """Get current chunk size."""
        config = self.get_rag_config()
        return config.get('chunk_size', 512)
    
    def get_chunk_overlap(self) -> int:
        """Get current chunk overlap."""
        config = self.get_rag_config()
        return config.get('chunk_overlap', 50)
    
    def get_top_k(self) -> int:
        """Get current top_k."""
        config = self.get_rag_config()
        return config.get('top_k', 5)
    
    def get_temperature(self) -> float:
        """Get current temperature."""
        config = self.get_rag_config()
        return config.get('temperature', 0.7)
    
    # ===== UI Configuration =====
    
    def get_theme(self) -> str:
        """
        Get current UI theme.
        
        Returns:
            str: Theme name ('light' or 'dark')
        
        Example:
            >>> service = ConfigurationService()
            >>> theme = service.get_theme()
            >>> print(theme)
            'light'
        """
        return self.config_repo.get_theme()
    
    def set_theme(self, theme: str) -> bool:
        """
        Set UI theme.
        
        Args:
            theme: Theme name ('light' or 'dark')
        
        Returns:
            bool: True if set successfully
        
        Example:
            >>> service = ConfigurationService()
            >>> service.set_theme('dark')
        """
        if theme not in ['light', 'dark']:
            raise ConfigurationError(f"Invalid theme: {theme}. Must be 'light' or 'dark'")
        
        success = self.config_repo.set_theme(theme)
        
        if success:
            logger.info("Theme updated", theme=theme)
        
        return success
    
    # ===== Configuration Management =====
    
    def validate_configuration(self) -> tuple[bool, list[str]]:
        """
        Validate current configuration.
        
        Returns:
            tuple: (is_valid, error_messages)
        
        Example:
            >>> service = ConfigurationService()
            >>> is_valid, errors = service.validate_configuration()
            >>> if not is_valid:
            ...     for error in errors:
            ...         print(error)
        """
        return self.config_repo.validate_config()
    
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values.
        
        Returns:
            bool: True if reset successfully
        
        Example:
            >>> service = ConfigurationService()
            >>> service.reset_to_defaults()
        """
        success = self.config_repo.reset_to_defaults()
        
        if success:
            logger.warning("Configuration reset to defaults")
        
        return success
    
    def export_configuration(self) -> dict:
        """
        Export configuration (with API keys redacted).
        
        Returns:
            dict: Configuration with sensitive data redacted
        
        Example:
            >>> service = ConfigurationService()
            >>> config = service.export_configuration()
            >>> # Safe to display or log
        """
        return self.config_repo.export_config()
    
    def get_full_configuration(self) -> dict:
        """
        Get complete configuration.
        
        Returns:
            dict: Full configuration
        
        Example:
            >>> service = ConfigurationService()
            >>> config = service.get_full_configuration()
            >>> print(config.keys())
            dict_keys(['llm', 'rag', 'ui'])
        """
        return self.config_repo.load_config()


# Singleton instance
_config_service_instance = None


def get_configuration_service() -> ConfigurationService:
    """
    Get singleton ConfigurationService instance.
    
    Returns:
        ConfigurationService: Singleton instance
    
    Example:
        >>> from src.services import get_configuration_service
        >>> config_service = get_configuration_service()
        >>> theme = config_service.get_theme()
    """
    global _config_service_instance
    
    if _config_service_instance is None:
        _config_service_instance = ConfigurationService()
        logger.debug("ConfigurationService singleton created")
    
    return _config_service_instance


# Convenience: Allow direct import
__all__ = [
    'ConfigurationService',
    'get_configuration_service',
]
