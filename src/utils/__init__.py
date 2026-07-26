"""
Utilities Package

This package provides utility functions and classes used throughout the application.

Modules:
    - logger: Centralized logging system
    - exceptions: Custom exception classes
    - validators: Input and file validation
    - helpers: General utility functions

Usage:
    >>> from src.utils import get_logger, validate_filename
    >>> logger = get_logger()
    >>> logger.info("Application started")
    >>> validate_filename("document.pdf")
    True

Author: TechFlow AI Project
License: MIT
"""

# Import main classes and functions for convenient access
from .logger import (
    AppLogger,
    LoggerSetupError,
    get_logger,
    log_startup_info,
    log_shutdown_info
)

from .exceptions import (
    # Base
    TechFlowError,
    
    # Configuration
    ConfigurationError,
    PathConfigurationError,
    SettingsValidationError,
    
    # File
    FileError,
    FileNotFoundError,
    FileTooLargeError,
    UnsupportedFileFormatError,
    InvalidFilenameError,
    FileCorruptedError,
    
    # Authentication
    AuthenticationError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    SessionExpiredError,
    
    # Knowledge Library
    KnowledgeLibraryError,
    EmptyKnowledgeLibraryError,
    DuplicateDocumentError,
    DocumentNotFoundError,
    IndexingError,
    
    # LLM
    LLMError,
    LLMAPIError,
    LLMRateLimitError,
    LLMTimeoutError,
    LLMInvalidResponseError,
    
    # RAG
    RAGError,
    EmbeddingError,
    VectorStoreError,
    RetrievalError,
    ChunkingError,
    
    # Validation
    ValidationError,
    InvalidInputError,
    MissingRequiredFieldError,
    
    # Storage
    StorageError,
    ReadError,
    WriteError,
    DeleteError,
    
    # Utilities
    format_exception,
    is_techflow_error,
)

from .validators import (
    validate_file_size,
    validate_file_format,
    validate_filename,
    validate_pdf_file,
    validate_text_file,
    validate_password,
    validate_query,
    validate_chunk_parameters,
    validate_top_k,
    validate_temperature,
)

from .helpers import (
    # Password
    hash_password,
    verify_password,
    
    # Checksums
    calculate_file_checksum,
    calculate_content_checksum,
    
    # Filename
    sanitize_filename,
    generate_unique_filename,
    
    # Date/Time
    format_timestamp,
    get_iso_timestamp,
    format_duration_seconds,
    
    # Text
    truncate_text,
    count_tokens_estimate,
    clean_whitespace,
    
    # JSON
    safe_json_load,
    safe_json_save,
    
    # Lists
    chunk_list,
    deduplicate_list,
    
    # Display
    format_number,
    format_percentage,
)


# Public API
__all__ = [
    # Logger
    'AppLogger',
    'LoggerSetupError',
    'get_logger',
    'log_startup_info',
    'log_shutdown_info',
    
    # Exceptions - Base
    'TechFlowError',
    
    # Exceptions - Configuration
    'ConfigurationError',
    'PathConfigurationError',
    'SettingsValidationError',
    
    # Exceptions - File
    'FileError',
    'FileNotFoundError',
    'FileTooLargeError',
    'UnsupportedFileFormatError',
    'InvalidFilenameError',
    'FileCorruptedError',
    
    # Exceptions - Authentication
    'AuthenticationError',
    'InvalidCredentialsError',
    'NotAuthenticatedError',
    'SessionExpiredError',
    
    # Exceptions - Knowledge Library
    'KnowledgeLibraryError',
    'EmptyKnowledgeLibraryError',
    'DuplicateDocumentError',
    'DocumentNotFoundError',
    'IndexingError',
    
    # Exceptions - LLM
    'LLMError',
    'LLMAPIError',
    'LLMRateLimitError',
    'LLMTimeoutError',
    'LLMInvalidResponseError',
    
    # Exceptions - RAG
    'RAGError',
    'EmbeddingError',
    'VectorStoreError',
    'RetrievalError',
    'ChunkingError',
    
    # Exceptions - Validation
    'ValidationError',
    'InvalidInputError',
    'MissingRequiredFieldError',
    
    # Exceptions - Storage
    'StorageError',
    'ReadError',
    'WriteError',
    'DeleteError',
    
    # Exceptions - Utilities
    'format_exception',
    'is_techflow_error',
    
    # Validators
    'validate_file_size',
    'validate_file_format',
    'validate_filename',
    'validate_pdf_file',
    'validate_text_file',
    'validate_password',
    'validate_query',
    'validate_chunk_parameters',
    'validate_top_k',
    'validate_temperature',
    
    # Helpers - Password
    'hash_password',
    'verify_password',
    
    # Helpers - Checksums
    'calculate_file_checksum',
    'calculate_content_checksum',
    
    # Helpers - Filename
    'sanitize_filename',
    'generate_unique_filename',
    
    # Helpers - Date/Time
    'format_timestamp',
    'get_iso_timestamp',
    'format_duration_seconds',
    
    # Helpers - Text
    'truncate_text',
    'count_tokens_estimate',
    'clean_whitespace',
    
    # Helpers - JSON
    'safe_json_load',
    'safe_json_save',
    
    # Helpers - Lists
    'chunk_list',
    'deduplicate_list',
    
    # Helpers - Display
    'format_number',
    'format_percentage',
]
