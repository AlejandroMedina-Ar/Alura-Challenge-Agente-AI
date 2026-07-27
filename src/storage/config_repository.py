"""
Config Repository Module

This module manages runtime configuration stored in config.json.
Provides CRUD operations for user preferences and app settings.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Any, Optional

from src.config import get_paths, LLMProvider, Theme
from src.utils import (
    get_logger,
    ConfigurationError,
    WriteError,
    ReadError,
    safe_json_load,
    safe_json_save
)


logger = get_logger()


class ConfigRepository:
    """
    Repository for managing runtime configuration (config.json).
    
    Configuration includes:
    - LLM provider settings (provider, model, base_url, api_key)
    - RAG parameters (chunk_size, chunk_overlap, top_k, temperature)
    - UI preferences (theme)
    
    The config file is created with defaults if it doesn't exist.
    """
    
    # Default configuration
    DEFAULT_CONFIG = {
        'llm': {
            'provider': LLMProvider.GEMINI.value,
            'model': 'gemini-1.5-flash',
            'api_key': ''
        },
        'rag': {
            'chunk_size': 512,
            'chunk_overlap': 50,
            'top_k': 5,
            'temperature': 0.7
        },
        'ui': {
            'theme': Theme.DARK.value
        }
    }
    
    def __init__(self):
        """Initialize config repository."""
        self.paths = get_paths()
        self.config_path = self.paths.CONFIG_FILE
        
        # Ensure config file exists
        self._ensure_config_exists()
        
        logger.debug("ConfigRepository initialized")
    
    def _ensure_config_exists(self):
        """Create config file with defaults if it doesn't exist."""
        if not self.config_path.exists():
            try:
                safe_json_save(self.config_path, self.DEFAULT_CONFIG)
                logger.info("Config file created with defaults", path=str(self.config_path))
            except Exception as e:
                logger.error("Failed to create config file", exc_info=True)
                raise WriteError(str(self.config_path), str(e))
    
    def load_config(self) -> dict:
        """
        Load complete configuration from file.
        
        Returns:
            dict: Complete configuration
        
        Raises:
            ReadError: If config cannot be read
        
        Example:
            >>> repo = ConfigRepository()
            >>> config = repo.load_config()
            >>> print(config['llm']['provider'])
            'ollama'
        """
        try:
            config = safe_json_load(self.config_path)
            logger.debug("Configuration loaded")
            return config
            
        except Exception as e:
            logger.error("Failed to load config", exc_info=True)
            raise ReadError(str(self.config_path), str(e))
    
    def save_config(self, config: dict) -> bool:
        """
        Save complete configuration to file.
        
        Args:
            config: Complete configuration dict
        
        Returns:
            bool: True if saved successfully
        
        Raises:
            WriteError: If config cannot be saved
        
        Example:
            >>> repo = ConfigRepository()
            >>> config = repo.load_config()
            >>> config['llm']['model'] = 'llama3.3'
            >>> repo.save_config(config)
            True
        """
        try:
            safe_json_save(self.config_path, config)
            logger.info("Configuration saved")
            return True
            
        except Exception as e:
            logger.error("Failed to save config", exc_info=True)
            raise WriteError(str(self.config_path), str(e))
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by key path.
        
        Args:
            key_path: Dot-separated path (e.g., 'llm.provider', 'rag.chunk_size')
            default: Default value if key doesn't exist
        
        Returns:
            Any: Configuration value
        
        Example:
            >>> repo = ConfigRepository()
            >>> provider = repo.get_value('llm.provider')
            >>> print(provider)
            'ollama'
            >>> chunk_size = repo.get_value('rag.chunk_size')
            >>> print(chunk_size)
            512
        """
        config = self.load_config()
        
        # Navigate through nested dict using key path
        keys = key_path.split('.')
        value = config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            logger.debug(f"Config key not found, using default", key=key_path, default=default)
            return default
    
    def set_value(self, key_path: str, value: Any) -> bool:
        """
        Set configuration value by key path.
        
        Args:
            key_path: Dot-separated path (e.g., 'llm.provider', 'rag.chunk_size')
            value: Value to set
        
        Returns:
            bool: True if saved successfully
        
        Raises:
            ConfigurationError: If key path is invalid
        
        Example:
            >>> repo = ConfigRepository()
            >>> repo.set_value('llm.model', 'llama3.3')
            True
            >>> repo.set_value('rag.top_k', 10)
            True
        """
        config = self.load_config()
        
        # Navigate to parent dict
        keys = key_path.split('.')
        parent = config
        
        try:
            for key in keys[:-1]:
                if key not in parent:
                    parent[key] = {}
                parent = parent[key]
            
            # Set value
            parent[keys[-1]] = value
            
            # Save config
            self.save_config(config)
            logger.info(f"Config value updated", key=key_path, value=str(value)[:50])
            return True
            
        except (KeyError, TypeError) as e:
            logger.error(f"Invalid config key path", key=key_path, exc_info=True)
            raise ConfigurationError(f"Invalid config key path: {key_path}")
    
    # === LLM Configuration ===
    
    def get_llm_config(self) -> dict:
        """
        Get LLM provider configuration.
        
        Returns:
            dict: LLM config (provider, model, api_key)
        
        Example:
            >>> repo = ConfigRepository()
            >>> llm_config = repo.get_llm_config()
            >>> print(llm_config)
            {
                'provider': 'gemini',
                'model': 'gemini-1.5-flash',
                'api_key': ''
            }
        """
        return self.get_value('llm', self.DEFAULT_CONFIG['llm'])
    
    def set_llm_config(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> bool:
        """
        Update LLM configuration.
        
        Args:
            provider: LLM provider (gemini, cohere)
            model: Model name
            api_key: API key
        
        Returns:
            bool: True if saved successfully
        
        Example:
            >>> repo = ConfigRepository()
            >>> repo.set_llm_config(
            ...     provider='gemini',
            ...     model='gemini-1.5-flash',
            ...     api_key='AIza...'
            ... )
        """
        llm_config = self.get_llm_config()
        
        if provider is not None:
            llm_config['provider'] = provider
        if model is not None:
            llm_config['model'] = model
        if api_key is not None:
            llm_config['api_key'] = api_key
        
        return self.set_value('llm', llm_config)
    
    # === RAG Configuration ===
    
    def get_rag_config(self) -> dict:
        """
        Get RAG parameters configuration.
        
        Returns:
            dict: RAG config (chunk_size, chunk_overlap, top_k, temperature)
        
        Example:
            >>> repo = ConfigRepository()
            >>> rag_config = repo.get_rag_config()
            >>> print(rag_config)
            {
                'chunk_size': 512,
                'chunk_overlap': 50,
                'top_k': 5,
                'temperature': 0.7
            }
        """
        return self.get_value('rag', self.DEFAULT_CONFIG['rag'])
    
    def set_rag_config(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        top_k: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> bool:
        """
        Update RAG parameters.
        
        Args:
            chunk_size: Text chunk size (128-2048)
            chunk_overlap: Overlap between chunks (0-512)
            top_k: Number of chunks to retrieve (1-20)
            temperature: LLM temperature (0.0-2.0)
        
        Returns:
            bool: True if saved successfully
        
        Example:
            >>> repo = ConfigRepository()
            >>> repo.set_rag_config(
            ...     chunk_size=1024,
            ...     top_k=10,
            ...     temperature=0.5
            ... )
        """
        rag_config = self.get_rag_config()
        
        if chunk_size is not None:
            rag_config['chunk_size'] = chunk_size
        if chunk_overlap is not None:
            rag_config['chunk_overlap'] = chunk_overlap
        if top_k is not None:
            rag_config['top_k'] = top_k
        if temperature is not None:
            rag_config['temperature'] = temperature
        
        return self.set_value('rag', rag_config)
    
    # === UI Configuration ===
    
    def get_ui_config(self) -> dict:
        """
        Get UI preferences.
        
        Returns:
            dict: UI config (theme)
        
        Example:
            >>> repo = ConfigRepository()
            >>> ui_config = repo.get_ui_config()
            >>> print(ui_config['theme'])
            'light'
        """
        return self.get_value('ui', self.DEFAULT_CONFIG['ui'])
    
    def set_theme(self, theme: str) -> bool:
        """
        Set UI theme.
        
        Args:
            theme: Theme name ('light' or 'dark')
        
        Returns:
            bool: True if saved successfully
        
        Example:
            >>> repo = ConfigRepository()
            >>> repo.set_theme('dark')
            True
        """
        ui_config = self.get_ui_config()
        ui_config['theme'] = theme
        return self.set_value('ui', ui_config)
    
    def get_theme(self) -> str:
        """
        Get current theme.
        
        Returns:
            str: Current theme ('light' or 'dark')
        
        Example:
            >>> repo = ConfigRepository()
            >>> theme = repo.get_theme()
            >>> print(theme)
            'light'
        """
        return self.get_value('ui.theme', self.DEFAULT_CONFIG['ui']['theme'])
    
    # === Utility Methods ===
    
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values.
        
        Returns:
            bool: True if reset successfully
        
        Example:
            >>> repo = ConfigRepository()
            >>> repo.reset_to_defaults()
            True
        """
        try:
            self.save_config(self.DEFAULT_CONFIG.copy())
            logger.warning("Configuration reset to defaults")
            return True
        except WriteError:
            return False
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """
        Validate configuration integrity.
        
        Returns:
            tuple: (is_valid, error_messages)
        
        Example:
            >>> repo = ConfigRepository()
            >>> is_valid, errors = repo.validate_config()
            >>> if not is_valid:
            ...     for error in errors:
            ...         print(error)
        """
        errors = []
        
        try:
            config = self.load_config()
            
            # Check required sections exist
            if 'llm' not in config:
                errors.append("Missing 'llm' section")
            if 'rag' not in config:
                errors.append("Missing 'rag' section")
            if 'ui' not in config:
                errors.append("Missing 'ui' section")
            
            # Validate LLM config
            if 'llm' in config:
                llm = config['llm']
                if 'provider' not in llm:
                    errors.append("Missing 'llm.provider'")
                if 'model' not in llm:
                    errors.append("Missing 'llm.model'")
            
            # Validate RAG config
            if 'rag' in config:
                rag = config['rag']
                if 'chunk_size' not in rag:
                    errors.append("Missing 'rag.chunk_size'")
                if 'top_k' not in rag:
                    errors.append("Missing 'rag.top_k'")
            
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.debug("Configuration validated successfully")
            else:
                logger.warning(f"Configuration validation failed", errors=errors)
            
            return is_valid, errors
            
        except Exception as e:
            errors.append(f"Config validation error: {str(e)}")
            return False, errors
    
    def export_config(self) -> dict:
        """
        Export configuration for backup/sharing.
        
        Note: API keys are redacted in export.
        
        Returns:
            dict: Configuration with sensitive data redacted
        
        Example:
            >>> repo = ConfigRepository()
            >>> export = repo.export_config()
            >>> print(export['llm']['api_key'])
            '***REDACTED***'
        """
        config = self.load_config()
        
        # Redact sensitive data
        export = config.copy()
        if 'llm' in export and 'api_key' in export['llm']:
            if export['llm']['api_key']:
                export['llm']['api_key'] = '***REDACTED***'
        
        logger.info("Configuration exported (sensitive data redacted)")
        return export


# Convenience: Allow direct import
__all__ = [
    'ConfigRepository',
]
