"""
Constants Module

This module defines all application constants, enums, and magic values.
Constants are organized by category for easy maintenance.

Author: TechFlow Solutions Project
License: MIT
"""

from enum import Enum
from typing import Final


# ==========================================
# APPLICATION METADATA
# ==========================================

APP_NAME: Final[str] = "TechFlow Solutions"
APP_FULL_NAME: Final[str] = "TechFlow Solutions Corporate Knowledge Agent"
APP_VERSION: Final[str] = "0.1.0-alpha"
APP_TAGLINE: Final[str] = "Corporate Knowledge Agent"
APP_DESCRIPTION: Final[str] = "RAG-powered AI assistant for enterprise knowledge management"


# ==========================================
# SUPPORTED FILE FORMATS
# ==========================================

class FileFormat(Enum):
    """Supported document file formats."""
    PDF = "pdf"
    TXT = "txt"
    MD = "md"
    DOCX = "docx"
    CSV = "csv"
    JSON = "json"
    HTML = "html"


# File extensions mapping
SUPPORTED_EXTENSIONS: Final[dict[str, FileFormat]] = {
    '.pdf': FileFormat.PDF,
    '.txt': FileFormat.TXT,
    '.md': FileFormat.MD,
    '.markdown': FileFormat.MD,
    '.docx': FileFormat.DOCX,
    '.csv': FileFormat.CSV,
    '.json': FileFormat.JSON,
    '.html': FileFormat.HTML,
    '.htm': FileFormat.HTML,
}

# MIME types mapping
MIME_TYPES: Final[dict[FileFormat, str]] = {
    FileFormat.PDF: 'application/pdf',
    FileFormat.TXT: 'text/plain',
    FileFormat.MD: 'text/markdown',
    FileFormat.DOCX: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    FileFormat.CSV: 'text/csv',
    FileFormat.JSON: 'application/json',
    FileFormat.HTML: 'text/html',
}


# ==========================================
# FILE SIZE LIMITS (bytes)
# ==========================================

class FileSizeLimit:
    """Default file size limits in bytes."""
    PDF: Final[int] = 50 * 1024 * 1024    # 50 MB
    DOCX: Final[int] = 25 * 1024 * 1024   # 25 MB
    TXT: Final[int] = 10 * 1024 * 1024    # 10 MB
    MD: Final[int] = 10 * 1024 * 1024     # 10 MB
    CSV: Final[int] = 25 * 1024 * 1024    # 25 MB
    JSON: Final[int] = 10 * 1024 * 1024   # 10 MB
    HTML: Final[int] = 10 * 1024 * 1024   # 10 MB


# File size limits by format
FILE_SIZE_LIMITS: Final[dict[FileFormat, int]] = {
    FileFormat.PDF: FileSizeLimit.PDF,
    FileFormat.DOCX: FileSizeLimit.DOCX,
    FileFormat.TXT: FileSizeLimit.TXT,
    FileFormat.MD: FileSizeLimit.MD,
    FileFormat.CSV: FileSizeLimit.CSV,
    FileFormat.JSON: FileSizeLimit.JSON,
    FileFormat.HTML: FileSizeLimit.HTML,
}


# ==========================================
# LLM PROVIDERS
# ==========================================

class LLMProvider(Enum):
    """Supported LLM providers."""
    GEMINI = "gemini"
    COHERE = "cohere"


# Provider display names
PROVIDER_NAMES: Final[dict[LLMProvider, str]] = {
    LLMProvider.GEMINI: "Google Gemini 1.5 Flash",
    LLMProvider.COHERE: "Cohere Command-R",
}


# ==========================================
# RAG CONFIGURATION
# ==========================================

# Chunking defaults
DEFAULT_CHUNK_SIZE: Final[int] = 1000
DEFAULT_CHUNK_OVERLAP: Final[int] = 200
MIN_CHUNK_SIZE: Final[int] = 100
MAX_CHUNK_SIZE: Final[int] = 5000

# Retrieval defaults
DEFAULT_TOP_K: Final[int] = 5
MIN_TOP_K: Final[int] = 1
MAX_TOP_K: Final[int] = 20

# Minimum documents required in knowledge library
MIN_DOCUMENTS_FOR_RAG: Final[int] = 1


# ==========================================
# LLM PARAMETERS
# ==========================================

# Temperature limits
DEFAULT_TEMPERATURE: Final[float] = 0.7
MIN_TEMPERATURE: Final[float] = 0.0
MAX_TEMPERATURE: Final[float] = 2.0

# Token limits
DEFAULT_MAX_CONTEXT_TOKENS: Final[int] = 8000
DEFAULT_MAX_OUTPUT_TOKENS: Final[int] = 2000
MIN_CONTEXT_TOKENS: Final[int] = 1000
MIN_OUTPUT_TOKENS: Final[int] = 100


# ==========================================
# FALLBACK CONFIGURATION
# ==========================================

# Fallback duration (seconds)
FALLBACK_DURATION_SECONDS: Final[int] = 300  # 5 minutes
FALLBACK_MAX_RETRIES: Final[int] = 3


# ==========================================
# SESSION CONFIGURATION
# ==========================================

# Session state keys
class SessionKey:
    """Streamlit session state keys."""
    AUTHENTICATED: Final[str] = "authenticated"
    IS_ADMIN: Final[str] = "is_admin"
    GUEST_MODE: Final[str] = "guest_mode"
    CONVERSATION_HISTORY: Final[str] = "conversation_history"
    CURRENT_VIEW: Final[str] = "current_view"
    THEME: Final[str] = "theme"
    LLM_PROVIDER: Final[str] = "llm_provider"
    FALLBACK_UNTIL: Final[str] = "fallback_until"
    UPLOAD_PROGRESS: Final[str] = "upload_progress"


# ==========================================
# UI CONFIGURATION
# ==========================================

# View names
class View(Enum):
    """Available UI views."""
    CHAT = "chat"
    ADMIN = "admin"
    SETTINGS = "settings"


# Theme names
class Theme(Enum):
    """Available UI themes."""
    DARK = "dark"
    LIGHT = "light"


# Tokyo Night color palette (dark theme)
TOKYO_NIGHT_COLORS: Final[dict[str, str]] = {
    'background': '#1a1b26',
    'foreground': '#c0caf5',
    'primary': '#7aa2f7',
    'secondary': '#bb9af7',
    'accent': '#7dcfff',
    'success': '#9ece6a',
    'warning': '#e0af68',
    'error': '#f7768e',
    'info': '#7aa2f7',
    'muted': '#565f89',
}


# ==========================================
# METADATA FIELDS
# ==========================================

class MetadataField:
    """Document metadata field names."""
    # Document identification
    DOCUMENT_NAME: Final[str] = "document_name"
    FILENAME: Final[str] = "filename"
    ORIGINAL_FILENAME: Final[str] = "original_filename"
    
    # File properties
    FILE_SIZE: Final[str] = "file_size"
    FILE_TYPE: Final[str] = "file_type"
    FILE_FORMAT: Final[str] = "file_format"
    CHECKSUM: Final[str] = "checksum"
    
    # Dates
    UPLOAD_DATE: Final[str] = "upload_date"
    LAST_INDEXED: Final[str] = "last_indexed"
    INDEX_DATE: Final[str] = "index_date"
    
    # Indexing info
    INDEXED: Final[str] = "indexed"
    NUM_CHUNKS: Final[str] = "num_chunks"
    CHUNK_COUNT: Final[str] = "chunk_count"
    
    # Document analysis
    LANGUAGE: Final[str] = "language"
    PAGE_COUNT: Final[str] = "page_count"  # For PDFs
    WORD_COUNT: Final[str] = "word_count"
    CHAR_COUNT: Final[str] = "char_count"
    
    # Metadata
    TAGS: Final[str] = "tags"
    DESCRIPTION: Final[str] = "description"


# ==========================================
# VALIDATION PATTERNS
# ==========================================

# Filename validation (alphanumeric, spaces, hyphens, underscores, dots)
VALID_FILENAME_PATTERN: Final[str] = r'^[a-zA-Z0-9\s\-_.]+$'

# Password requirements
MIN_PASSWORD_LENGTH: Final[int] = 8
MAX_PASSWORD_LENGTH: Final[int] = 128


# ==========================================
# ERROR MESSAGES
# ==========================================

class ErrorMessage:
    """Standard error messages."""
    
    # File validation
    FILE_TOO_LARGE: Final[str] = "File size exceeds maximum allowed size of {max_size} MB"
    UNSUPPORTED_FORMAT: Final[str] = "File format not supported. Supported formats: {formats}"
    INVALID_FILENAME: Final[str] = "Invalid filename. Use only letters, numbers, spaces, hyphens, and underscores"
    FILE_NOT_FOUND: Final[str] = "File not found: {filename}"
    
    # Authentication
    INVALID_CREDENTIALS: Final[str] = "Invalid password"
    NOT_AUTHENTICATED: Final[str] = "You must be logged in to access this feature"
    
    # Knowledge library
    EMPTY_KNOWLEDGE_LIBRARY: Final[str] = "Knowledge library is empty. Please upload at least {min_docs} document(s)"
    DUPLICATE_DOCUMENT: Final[str] = "Document '{filename}' already exists in the knowledge library"
    
    # LLM
    LLM_API_ERROR: Final[str] = "Error communicating with {provider}: {error}"
    FALLBACK_ACTIVATED: Final[str] = "Primary LLM unavailable. Using fallback provider for {duration} minutes"
    
    # General
    UNEXPECTED_ERROR: Final[str] = "An unexpected error occurred: {error}"
    CONFIGURATION_ERROR: Final[str] = "Configuration error: {error}"


# ==========================================
# SUCCESS MESSAGES
# ==========================================

class SuccessMessage:
    """Standard success messages."""
    
    DOCUMENT_UPLOADED: Final[str] = "Document '{filename}' uploaded successfully"
    DOCUMENT_DELETED: Final[str] = "Document '{filename}' deleted successfully"
    DOCUMENT_INDEXED: Final[str] = "Document '{filename}' indexed successfully ({num_chunks} chunks)"
    LOGIN_SUCCESS: Final[str] = "Login successful"
    LOGOUT_SUCCESS: Final[str] = "Logged out successfully"
    SETTINGS_SAVED: Final[str] = "Settings saved successfully"


# ==========================================
# LOGGING FORMAT
# ==========================================

LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


# ==========================================
# API RATE LIMITS
# ==========================================

# Gemini free tier limits
GEMINI_REQUESTS_PER_MINUTE: Final[int] = 15
GEMINI_REQUESTS_PER_DAY: Final[int] = 1500

# Cohere free tier limits
COHERE_REQUESTS_PER_MONTH: Final[int] = 1000


# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def get_file_format(extension: str) -> FileFormat | None:
    """
    Get FileFormat enum from file extension.
    
    Args:
        extension: File extension (with or without leading dot)
    
    Returns:
        FileFormat: Corresponding format, or None if unsupported
    
    Example:
        >>> get_file_format('.pdf')
        <FileFormat.PDF: 'pdf'>
        >>> get_file_format('pdf')
        <FileFormat.PDF: 'pdf'>
        >>> get_file_format('.xyz')
        None
    """
    if not extension.startswith('.'):
        extension = f'.{extension}'
    
    return SUPPORTED_EXTENSIONS.get(extension.lower())


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        str: Formatted size (e.g., "1.5 MB")
    
    Example:
        >>> format_file_size(1536)
        '1.5 KB'
        >>> format_file_size(1048576)
        '1.0 MB'
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_supported_extensions_list() -> list[str]:
    """
    Get list of supported file extensions.
    
    Returns:
        list[str]: List of extensions (e.g., ['.pdf', '.txt', ...])
    
    Example:
        >>> exts = get_supported_extensions_list()
        >>> '.pdf' in exts
        True
    """
    return list(SUPPORTED_EXTENSIONS.keys())


def get_supported_formats_display() -> str:
    """
    Get comma-separated string of supported formats for display.
    
    Returns:
        str: Display string (e.g., "PDF, TXT, MD, DOCX, CSV, JSON, HTML")
    
    Example:
        >>> print(get_supported_formats_display())
        'PDF, TXT, MD, DOCX, CSV, JSON, HTML'
    """
    formats = set(fmt.value.upper() for fmt in SUPPORTED_EXTENSIONS.values())
    return ", ".join(sorted(formats))


# Convenience: Allow direct import
__all__ = [
    # Metadata
    'APP_NAME',
    'APP_FULL_NAME',
    'APP_VERSION',
    'APP_TAGLINE',
    'APP_DESCRIPTION',
    
    # Enums
    'FileFormat',
    'LLMProvider',
    'View',
    'Theme',
    
    # Classes
    'SessionKey',
    'MetadataField',
    'ErrorMessage',
    'SuccessMessage',
    'FileSizeLimit',
    
    # Dicts
    'SUPPORTED_EXTENSIONS',
    'FILE_SIZE_LIMITS',
    'MIME_TYPES',
    'PROVIDER_NAMES',
    'TOKYO_NIGHT_COLORS',
    
    # Constants
    'DEFAULT_CHUNK_SIZE',
    'DEFAULT_CHUNK_OVERLAP',
    'DEFAULT_TOP_K',
    'MIN_DOCUMENTS_FOR_RAG',
    'FALLBACK_DURATION_SECONDS',
    'LOG_FORMAT',
    'LOG_DATE_FORMAT',
    
    # Functions
    'get_file_format',
    'format_file_size',
    'get_supported_extensions_list',
    'get_supported_formats_display',
]
