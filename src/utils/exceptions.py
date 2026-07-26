"""
Custom Exceptions Module

This module defines all custom exceptions used throughout the application.
Exceptions are organized by category for better error handling.

Author: TechFlow AI Project
License: MIT
"""


# ==========================================
# BASE EXCEPTION
# ==========================================

class TechFlowError(Exception):
    """
    Base exception for all TechFlow AI errors.
    
    All custom exceptions inherit from this class for easy catching.
    """
    pass


# ==========================================
# CONFIGURATION ERRORS
# ==========================================

class ConfigurationError(TechFlowError):
    """Raised when configuration is invalid or missing."""
    pass


class PathConfigurationError(ConfigurationError):
    """Raised when path configuration fails."""
    pass


class SettingsValidationError(ConfigurationError):
    """Raised when settings validation fails."""
    pass


# ==========================================
# FILE ERRORS
# ==========================================

class FileError(TechFlowError):
    """Base exception for file-related errors."""
    pass


class FileNotFoundError(FileError):
    """Raised when a file is not found."""
    
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"File not found: {filename}")


class FileTooLargeError(FileError):
    """Raised when a file exceeds maximum size limit."""
    
    def __init__(self, filename: str, size: int, max_size: int):
        self.filename = filename
        self.size = size
        self.max_size = max_size
        super().__init__(
            f"File '{filename}' is too large ({size} bytes). "
            f"Maximum allowed: {max_size} bytes"
        )


class UnsupportedFileFormatError(FileError):
    """Raised when file format is not supported."""
    
    def __init__(self, filename: str, format: str, supported_formats: list[str]):
        self.filename = filename
        self.format = format
        self.supported_formats = supported_formats
        super().__init__(
            f"File '{filename}' has unsupported format '{format}'. "
            f"Supported formats: {', '.join(supported_formats)}"
        )


class InvalidFilenameError(FileError):
    """Raised when filename contains invalid characters."""
    
    def __init__(self, filename: str, reason: str = None):
        self.filename = filename
        message = f"Invalid filename: {filename}"
        if reason:
            message += f" ({reason})"
        super().__init__(message)


class FileCorruptedError(FileError):
    """Raised when a file is corrupted or unreadable."""
    
    def __init__(self, filename: str, reason: str = None):
        self.filename = filename
        message = f"File '{filename}' is corrupted or unreadable"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class WriteError(FileError):
    """Raised when a write operation fails."""
    
    def __init__(self, filepath: str, reason: str = None):
        self.filepath = filepath
        message = f"Failed to write file: {filepath}"
        if reason:
            message += f" ({reason})"
        super().__init__(message)


class ReadError(FileError):
    """Raised when a read operation fails."""
    
    def __init__(self, filepath: str, reason: str = None):
        self.filepath = filepath
        message = f"Failed to read file: {filepath}"
        if reason:
            message += f" ({reason})"
        super().__init__(message)


class DeleteError(FileError):
    """Raised when a delete operation fails."""
    
    def __init__(self, filepath: str, reason: str = None):
        self.filepath = filepath
        message = f"Failed to delete file: {filepath}"
        if reason:
            message += f" ({reason})"
        super().__init__(message)


# ==========================================
# AUTHENTICATION ERRORS
# ==========================================

class AuthenticationError(TechFlowError):
    """Base exception for authentication errors."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""
    
    def __init__(self):
        super().__init__("Invalid credentials")


class NotAuthenticatedError(AuthenticationError):
    """Raised when user tries to access protected resource without authentication."""
    
    def __init__(self, resource: str = None):
        message = "Authentication required"
        if resource:
            message += f" to access {resource}"
        super().__init__(message)


class SessionExpiredError(AuthenticationError):
    """Raised when user session has expired."""
    
    def __init__(self):
        super().__init__("Session has expired. Please login again.")


# ==========================================
# KNOWLEDGE LIBRARY ERRORS
# ==========================================

class KnowledgeLibraryError(TechFlowError):
    """Base exception for knowledge library errors."""
    pass


class EmptyKnowledgeLibraryError(KnowledgeLibraryError):
    """Raised when knowledge library is empty and RAG is attempted."""
    
    def __init__(self, min_documents: int = 1):
        self.min_documents = min_documents
        super().__init__(
            f"Knowledge library is empty. Please upload at least {min_documents} document(s)."
        )


class DuplicateDocumentError(KnowledgeLibraryError):
    """Raised when attempting to upload a document that already exists."""
    
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"Document '{filename}' already exists in knowledge library")


class DocumentNotFoundError(KnowledgeLibraryError):
    """Raised when a document is not found in knowledge library."""
    
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"Document '{filename}' not found in knowledge library")


class MetadataNotFoundError(KnowledgeLibraryError):
    """Raised when metadata is not found for a document."""
    
    def __init__(self, document_name: str):
        self.document_name = document_name
        super().__init__(f"Metadata not found for document: {document_name}")


class IndexingError(KnowledgeLibraryError):
    """Raised when document indexing fails."""
    
    def __init__(self, filename: str, reason: str):
        self.filename = filename
        self.reason = reason
        super().__init__(f"Failed to index document '{filename}': {reason}")


# ==========================================
# LLM PROVIDER ERRORS
# ==========================================

class LLMError(TechFlowError):
    """Base exception for LLM provider errors."""
    pass


class LLMAPIError(LLMError):
    """Raised when LLM API call fails."""
    
    def __init__(self, provider: str, error: str):
        self.provider = provider
        self.error = error
        super().__init__(f"LLM API error ({provider}): {error}")


class LLMRateLimitError(LLMError):
    """Raised when LLM API rate limit is exceeded."""
    
    def __init__(self, provider: str, retry_after: int = None):
        self.provider = provider
        self.retry_after = retry_after
        message = f"Rate limit exceeded for {provider}"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message)


class LLMTimeoutError(LLMError):
    """Raised when LLM API call times out."""
    
    def __init__(self, provider: str, timeout: int):
        self.provider = provider
        self.timeout = timeout
        super().__init__(f"LLM API timeout ({provider}): {timeout}s")


class LLMInvalidResponseError(LLMError):
    """Raised when LLM returns invalid or empty response."""
    
    def __init__(self, provider: str, reason: str = None):
        self.provider = provider
        message = f"Invalid response from {provider}"
        if reason:
            message += f": {reason}"
        super().__init__(message)


# ==========================================
# RAG PIPELINE ERRORS
# ==========================================

class RAGError(TechFlowError):
    """Base exception for RAG pipeline errors."""
    pass


class EmbeddingError(RAGError):
    """Raised when embedding generation fails."""
    
    def __init__(self, text: str, reason: str):
        self.text = text[:100]  # First 100 chars
        self.reason = reason
        super().__init__(f"Failed to generate embedding: {reason}")


class VectorStoreError(RAGError):
    """Raised when vector store operation fails."""
    
    def __init__(self, operation: str, reason: str):
        self.operation = operation
        self.reason = reason
        super().__init__(f"Vector store {operation} failed: {reason}")


class RetrievalError(RAGError):
    """Raised when document retrieval fails."""
    
    def __init__(self, query: str, reason: str):
        self.query = query[:100]
        self.reason = reason
        super().__init__(f"Retrieval failed: {reason}")


class ChunkingError(RAGError):
    """Raised when text chunking fails."""
    
    def __init__(self, document: str, reason: str):
        self.document = document
        self.reason = reason
        super().__init__(f"Failed to chunk document '{document}': {reason}")


# ==========================================
# VALIDATION ERRORS
# ==========================================

class ValidationError(TechFlowError):
    """Base exception for validation errors."""
    pass


class InvalidInputError(ValidationError):
    """Raised when user input is invalid."""
    
    def __init__(self, field: str, value: any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid {field}: {reason}")


class MissingRequiredFieldError(ValidationError):
    """Raised when required field is missing."""
    
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"Required field missing: {field}")


# ==========================================
# STORAGE ERRORS
# ==========================================

class StorageError(TechFlowError):
    """Base exception for storage errors."""
    pass


class ReadError(StorageError):
    """Raised when reading from storage fails."""
    
    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to read from '{path}': {reason}")


class WriteError(StorageError):
    """Raised when writing to storage fails."""
    
    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to write to '{path}': {reason}")


class DeleteError(StorageError):
    """Raised when deleting from storage fails."""
    
    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to delete '{path}': {reason}")


# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def format_exception(exc: Exception) -> str:
    """
    Format exception for logging.
    
    Args:
        exc: Exception to format
    
    Returns:
        str: Formatted exception string
    
    Example:
        >>> try:
        ...     raise ValueError("Invalid value")
        ... except Exception as e:
        ...     print(format_exception(e))
        ValueError: Invalid value
    """
    return f"{exc.__class__.__name__}: {str(exc)}"


def is_techflow_error(exc: Exception) -> bool:
    """
    Check if exception is a TechFlow custom exception.
    
    Args:
        exc: Exception to check
    
    Returns:
        bool: True if exception is a TechFlowError subclass
    
    Example:
        >>> from src.utils.exceptions import FileNotFoundError
        >>> exc = FileNotFoundError("test.pdf")
        >>> is_techflow_error(exc)
        True
        >>> is_techflow_error(ValueError("test"))
        False
    """
    return isinstance(exc, TechFlowError)


# Convenience: Allow direct import
__all__ = [
    # Base
    'TechFlowError',
    
    # Configuration
    'ConfigurationError',
    'PathConfigurationError',
    'SettingsValidationError',
    
    # File
    'FileError',
    'FileNotFoundError',
    'FileTooLargeError',
    'UnsupportedFileFormatError',
    'InvalidFilenameError',
    'FileCorruptedError',
    
    # Authentication
    'AuthenticationError',
    'InvalidCredentialsError',
    'NotAuthenticatedError',
    'SessionExpiredError',
    
    # Knowledge Library
    'KnowledgeLibraryError',
    'EmptyKnowledgeLibraryError',
    'DuplicateDocumentError',
    'DocumentNotFoundError',
    'IndexingError',
    
    # LLM
    'LLMError',
    'LLMAPIError',
    'LLMRateLimitError',
    'LLMTimeoutError',
    'LLMInvalidResponseError',
    
    # RAG
    'RAGError',
    'EmbeddingError',
    'VectorStoreError',
    'RetrievalError',
    'ChunkingError',
    
    # Validation
    'ValidationError',
    'InvalidInputError',
    'MissingRequiredFieldError',
    
    # Storage
    'StorageError',
    'ReadError',
    'WriteError',
    'DeleteError',
    
    # Utilities
    'format_exception',
    'is_techflow_error',
]
