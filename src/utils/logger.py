"""
Logging Module

This module provides a centralized logging system for the application.
Logs are written to both console and file with rotation support.

Author: TechFlow AI Project
License: MIT
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from src.config import get_settings, get_paths, LOG_FORMAT, LOG_DATE_FORMAT


class LoggerSetupError(Exception):
    """Raised when logger setup fails."""
    pass


class AppLogger:
    """
    Application logger with console and file output.
    
    Features:
    - Dual output (console + file)
    - Log rotation (max 10MB per file, keep 5 backups)
    - Configurable log level from settings
    - Colored console output (optional)
    - Separate error log file
    
    Attributes:
        logger: The underlying Python logger instance
        log_level: Current log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    def __init__(self, name: str = "techflow"):
        """
        Initialize the application logger.
        
        Args:
            name: Logger name (default: "techflow")
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Configure logger with console and file handlers."""
        # Prevent duplicate handlers if logger is reinitialized
        if self.logger.handlers:
            return
        
        try:
            # Get configuration
            settings = get_settings()
            paths = get_paths()
            
            # Set log level from settings
            log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
            self.logger.setLevel(log_level)
            self.log_level = settings.LOG_LEVEL
            
            # Create formatters
            formatter = logging.Formatter(
                fmt=LOG_FORMAT,
                datefmt=LOG_DATE_FORMAT
            )
            
            # === Console Handler ===
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # === File Handler (Application Log) ===
            file_handler = RotatingFileHandler(
                filename=paths.APPLICATION_LOG,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # === File Handler (Error Log) ===
            error_handler = RotatingFileHandler(
                filename=paths.ERROR_LOG,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            self.logger.addHandler(error_handler)
            
            # Prevent propagation to root logger
            self.logger.propagate = False
            
            # Log initialization
            self.logger.info(f"Logger initialized - Level: {settings.LOG_LEVEL}")
            
        except Exception as e:
            raise LoggerSetupError(f"Failed to setup logger: {e}")
    
    def debug(self, message: str, **kwargs) -> None:
        """
        Log debug message.
        
        Args:
            message: Log message
            **kwargs: Additional context (will be added to message)
        """
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.debug(message)
    
    def info(self, message: str, **kwargs) -> None:
        """
        Log info message.
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.info(message)
    
    def warning(self, message: str, **kwargs) -> None:
        """
        Log warning message.
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False, **kwargs) -> None:
        """
        Log error message.
        
        Args:
            message: Log message
            exc_info: Include exception traceback
            **kwargs: Additional context
        """
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False, **kwargs) -> None:
        """
        Log critical message.
        
        Args:
            message: Log message
            exc_info: Include exception traceback
            **kwargs: Additional context
        """
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.critical(message, exc_info=exc_info)
    
    def exception(self, message: str, **kwargs) -> None:
        """
        Log exception with traceback.
        
        Should be called from exception handler.
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.exception(message)
    
    def _format_kwargs(self, kwargs: dict) -> str:
        """
        Format kwargs dict as string for logging.
        
        Args:
            kwargs: Dictionary of key-value pairs
        
        Returns:
            str: Formatted string (e.g., "key1=value1, key2=value2")
        """
        return ", ".join(f"{k}={v}" for k, v in kwargs.items())
    
    def set_level(self, level: str) -> None:
        """
        Change log level at runtime.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
        Example:
            >>> logger = get_logger()
            >>> logger.set_level('DEBUG')
        """
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        self.log_level = level.upper()
        
        # Update all handlers
        for handler in self.logger.handlers:
            if not isinstance(handler, logging.FileHandler) or 'error' not in handler.baseFilename:
                handler.setLevel(log_level)
        
        self.logger.info(f"Log level changed to {level.upper()}")
    
    def log_function_call(self, func_name: str, **kwargs) -> None:
        """
        Log function call with parameters.
        
        Args:
            func_name: Name of the function
            **kwargs: Function parameters
        
        Example:
            >>> logger = get_logger()
            >>> logger.log_function_call('upload_document', filename='test.pdf', size=1024)
        """
        params = self._format_kwargs(kwargs) if kwargs else "no params"
        self.logger.debug(f"Function call: {func_name}({params})")
    
    def log_api_call(self, provider: str, model: str, success: bool, duration_ms: float) -> None:
        """
        Log API call to LLM provider.
        
        Args:
            provider: Provider name (e.g., 'Gemini', 'Cohere')
            model: Model name
            success: Whether call succeeded
            duration_ms: Call duration in milliseconds
        
        Example:
            >>> logger = get_logger()
            >>> logger.log_api_call('Gemini', 'gemini-2.0-flash', True, 1250.5)
        """
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"API call to {provider} ({model}) - {status} - {duration_ms:.2f}ms"
        )
    
    def log_document_operation(self, operation: str, filename: str, success: bool, **kwargs) -> None:
        """
        Log document operation (upload, delete, index).
        
        Args:
            operation: Operation type (e.g., 'upload', 'delete', 'index')
            filename: Document filename
            success: Whether operation succeeded
            **kwargs: Additional context (e.g., size, chunks, error)
        
        Example:
            >>> logger = get_logger()
            >>> logger.log_document_operation('upload', 'manual.pdf', True, size=1048576)
        """
        status = "SUCCESS" if success else "FAILED"
        context = f" | {self._format_kwargs(kwargs)}" if kwargs else ""
        self.logger.info(f"Document {operation}: {filename} - {status}{context}")
    
    def __repr__(self) -> str:
        """String representation."""
        return f"AppLogger(name={self.name}, level={self.log_level})"


# Global logger instance (singleton)
_logger_instance: Optional[AppLogger] = None


def get_logger(name: str = "techflow") -> AppLogger:
    """
    Get the global logger instance (singleton).
    
    Args:
        name: Logger name (default: "techflow")
    
    Returns:
        AppLogger: The global logger instance
    
    Example:
        >>> from src.utils.logger import get_logger
        >>> logger = get_logger()
        >>> logger.info("Application started")
        >>> logger.error("An error occurred", exc_info=True)
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = AppLogger(name)
    
    return _logger_instance


def log_startup_info() -> None:
    """
    Log application startup information.
    
    Logs: version, configuration summary, paths.
    Should be called once at application startup.
    
    Example:
        >>> from src.utils.logger import log_startup_info
        >>> log_startup_info()
    """
    logger = get_logger()
    settings = get_settings()
    paths = get_paths()
    
    from src.config import APP_NAME, APP_VERSION
    
    logger.info("=" * 60)
    logger.info(f"{APP_NAME} v{APP_VERSION} - Starting up")
    logger.info("=" * 60)
    
    # Log configuration summary
    config = settings.get_summary()
    logger.info("Configuration:")
    for key, value in config.items():
        logger.info(f"  {key}: {value}")
    
    # Log important paths
    logger.info("Paths:")
    logger.info(f"  Project root: {paths.PROJECT_ROOT}")
    logger.info(f"  Documents: {paths.DOCUMENTS_DIR}")
    logger.info(f"  Logs: {paths.LOGS_DIR}")
    logger.info(f"  ChromaDB: {paths.CHROMADB_DIR}")
    
    logger.info("=" * 60)


def log_shutdown_info() -> None:
    """
    Log application shutdown information.
    
    Should be called before application exits.
    
    Example:
        >>> from src.utils.logger import log_shutdown_info
        >>> log_shutdown_info()
    """
    logger = get_logger()
    
    from src.config import APP_NAME
    
    logger.info("=" * 60)
    logger.info(f"{APP_NAME} - Shutting down")
    logger.info("=" * 60)


# Convenience: Allow direct import
__all__ = [
    'AppLogger',
    'LoggerSetupError',
    'get_logger',
    'log_startup_info',
    'log_shutdown_info'
]
