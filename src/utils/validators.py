"""
Validators Module

This module provides validation functions for files, inputs, and data.
All validators return True if valid, or raise an exception if invalid.

Author: TechFlow AI Project
License: MIT
"""

import re
from pathlib import Path
from typing import BinaryIO, Optional

from src.config import (
    get_file_format,
    get_supported_extensions_list,
    FILE_SIZE_LIMITS,
    FileFormat,
    VALID_FILENAME_PATTERN,
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH
)

from src.utils.exceptions import (
    FileTooLargeError,
    UnsupportedFileFormatError,
    InvalidFilenameError,
    FileCorruptedError,
    InvalidInputError,
    MissingRequiredFieldError
)


def validate_file_size(filename: str, size: int, file_format: FileFormat) -> bool:
    """
    Validate that file size is within allowed limits.
    
    Args:
        filename: Name of the file
        size: File size in bytes
        file_format: File format enum
    
    Returns:
        bool: True if valid
    
    Raises:
        FileTooLargeError: If file exceeds maximum size
    
    Example:
        >>> validate_file_size('test.pdf', 1024, FileFormat.PDF)
        True
        >>> validate_file_size('huge.pdf', 100*1024*1024, FileFormat.PDF)
        FileTooLargeError: File 'huge.pdf' is too large...
    """
    max_size = FILE_SIZE_LIMITS.get(file_format)
    
    if max_size is None:
        # No limit defined for this format (shouldn't happen)
        return True
    
    if size > max_size:
        raise FileTooLargeError(filename, size, max_size)
    
    return True


def validate_file_format(filename: str) -> FileFormat:
    """
    Validate file format and return format enum.
    
    Args:
        filename: Name of the file (with extension)
    
    Returns:
        FileFormat: The file format enum
    
    Raises:
        UnsupportedFileFormatError: If format is not supported
    
    Example:
        >>> validate_file_format('document.pdf')
        <FileFormat.PDF: 'pdf'>
        >>> validate_file_format('image.jpg')
        UnsupportedFileFormatError: File 'image.jpg' has unsupported format...
    """
    extension = Path(filename).suffix.lower()
    
    if not extension:
        raise UnsupportedFileFormatError(
            filename,
            "no extension",
            get_supported_extensions_list()
        )
    
    file_format = get_file_format(extension)
    
    if file_format is None:
        raise UnsupportedFileFormatError(
            filename,
            extension,
            get_supported_extensions_list()
        )
    
    return file_format


def validate_filename(filename: str, allow_path: bool = False) -> bool:
    """
    Validate filename for invalid characters.
    
    Args:
        filename: Filename to validate
        allow_path: If True, allow path separators (/ or \\)
    
    Returns:
        bool: True if valid
    
    Raises:
        InvalidFilenameError: If filename contains invalid characters
    
    Example:
        >>> validate_filename('document.pdf')
        True
        >>> validate_filename('doc<>ument.pdf')
        InvalidFilenameError: Invalid filename: doc<>ument.pdf
    """
    if not filename:
        raise InvalidFilenameError(filename, "filename is empty")
    
    # Remove path if present (only validate filename part)
    if not allow_path:
        filename = Path(filename).name
    
    # Check for invalid characters
    if not re.match(VALID_FILENAME_PATTERN, filename):
        raise InvalidFilenameError(
            filename,
            "contains invalid characters (only letters, numbers, spaces, hyphens, underscores, and dots allowed)"
        )
    
    # Check for reserved names (Windows)
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                      'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                      'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    
    name_without_ext = Path(filename).stem.upper()
    if name_without_ext in reserved_names:
        raise InvalidFilenameError(filename, f"'{name_without_ext}' is a reserved system name")
    
    # Check length (max 255 characters is common limit)
    if len(filename) > 255:
        raise InvalidFilenameError(filename, "filename too long (max 255 characters)")
    
    return True


def validate_pdf_file(file_content: bytes, filename: str) -> bool:
    """
    Validate that file content is a valid PDF.
    
    Args:
        file_content: File content as bytes
        filename: Filename for error messages
    
    Returns:
        bool: True if valid PDF
    
    Raises:
        FileCorruptedError: If file is not a valid PDF
    
    Example:
        >>> with open('test.pdf', 'rb') as f:
        ...     content = f.read()
        ...     validate_pdf_file(content, 'test.pdf')
        True
    """
    # PDF files start with "%PDF-" magic number
    if not file_content.startswith(b'%PDF-'):
        raise FileCorruptedError(filename, "not a valid PDF file (missing PDF header)")
    
    # Check for EOF marker (should be present in valid PDFs)
    if b'%%EOF' not in file_content:
        raise FileCorruptedError(filename, "PDF file appears incomplete (missing EOF marker)")
    
    return True


def validate_text_file(file_content: bytes, filename: str, max_size: int = 10 * 1024 * 1024) -> bool:
    """
    Validate that file content is valid text.
    
    Args:
        file_content: File content as bytes
        filename: Filename for error messages
        max_size: Maximum size in bytes (default 10MB)
    
    Returns:
        bool: True if valid text
    
    Raises:
        FileTooLargeError: If file is too large
        FileCorruptedError: If file is not valid text
    
    Example:
        >>> content = b"This is a text file"
        >>> validate_text_file(content, 'test.txt')
        True
    """
    if len(file_content) > max_size:
        raise FileTooLargeError(filename, len(file_content), max_size)
    
    # Try to decode as UTF-8
    try:
        file_content.decode('utf-8')
    except UnicodeDecodeError:
        # Try other encodings
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                file_content.decode(encoding)
                return True
            except UnicodeDecodeError:
                continue
        
        raise FileCorruptedError(filename, "not a valid text file (encoding not supported)")
    
    return True


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        InvalidInputError: If password doesn't meet requirements
    
    Example:
        >>> validate_password('MySecurePass123')
        True
        >>> validate_password('weak')
        InvalidInputError: Invalid password: too short
    """
    if not password:
        raise MissingRequiredFieldError('password')
    
    if len(password) < MIN_PASSWORD_LENGTH:
        raise InvalidInputError(
            'password',
            password,
            f'too short (minimum {MIN_PASSWORD_LENGTH} characters)'
        )
    
    if len(password) > MAX_PASSWORD_LENGTH:
        raise InvalidInputError(
            'password',
            password,
            f'too long (maximum {MAX_PASSWORD_LENGTH} characters)'
        )
    
    return True


def validate_query(query: str, min_length: int = 3, max_length: int = 1000) -> bool:
    """
    Validate user query.
    
    Args:
        query: User query string
        min_length: Minimum query length (default 3)
        max_length: Maximum query length (default 1000)
    
    Returns:
        bool: True if valid
    
    Raises:
        InvalidInputError: If query is invalid
    
    Example:
        >>> validate_query('What is RAG?')
        True
        >>> validate_query('a')
        InvalidInputError: Invalid query: too short
    """
    if not query or not query.strip():
        raise MissingRequiredFieldError('query')
    
    query = query.strip()
    
    if len(query) < min_length:
        raise InvalidInputError(
            'query',
            query,
            f'too short (minimum {min_length} characters)'
        )
    
    if len(query) > max_length:
        raise InvalidInputError(
            'query',
            query,
            f'too long (maximum {max_length} characters)'
        )
    
    return True


def validate_chunk_parameters(chunk_size: int, chunk_overlap: int) -> bool:
    """
    Validate RAG chunking parameters.
    
    Args:
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
    
    Returns:
        bool: True if valid
    
    Raises:
        InvalidInputError: If parameters are invalid
    
    Example:
        >>> validate_chunk_parameters(1000, 200)
        True
        >>> validate_chunk_parameters(100, 200)
        InvalidInputError: Invalid chunk_overlap: must be less than chunk_size
    """
    from src.config import MIN_CHUNK_SIZE, MAX_CHUNK_SIZE
    
    if chunk_size < MIN_CHUNK_SIZE:
        raise InvalidInputError(
            'chunk_size',
            chunk_size,
            f'too small (minimum {MIN_CHUNK_SIZE})'
        )
    
    if chunk_size > MAX_CHUNK_SIZE:
        raise InvalidInputError(
            'chunk_size',
            chunk_size,
            f'too large (maximum {MAX_CHUNK_SIZE})'
        )
    
    if chunk_overlap < 0:
        raise InvalidInputError(
            'chunk_overlap',
            chunk_overlap,
            'cannot be negative'
        )
    
    if chunk_overlap >= chunk_size:
        raise InvalidInputError(
            'chunk_overlap',
            chunk_overlap,
            'must be less than chunk_size'
        )
    
    return True


def validate_top_k(top_k: int) -> bool:
    """
    Validate top-k parameter for retrieval.
    
    Args:
        top_k: Number of results to retrieve
    
    Returns:
        bool: True if valid
    
    Raises:
        InvalidInputError: If top_k is invalid
    
    Example:
        >>> validate_top_k(5)
        True
        >>> validate_top_k(0)
        InvalidInputError: Invalid top_k: must be at least 1
    """
    from src.config import MIN_TOP_K, MAX_TOP_K
    
    if top_k < MIN_TOP_K:
        raise InvalidInputError(
            'top_k',
            top_k,
            f'too small (minimum {MIN_TOP_K})'
        )
    
    if top_k > MAX_TOP_K:
        raise InvalidInputError(
            'top_k',
            top_k,
            f'too large (maximum {MAX_TOP_K})'
        )
    
    return True


def validate_temperature(temperature: float) -> bool:
    """
    Validate LLM temperature parameter.
    
    Args:
        temperature: Temperature value
    
    Returns:
        bool: True if valid
    
    Raises:
        InvalidInputError: If temperature is invalid
    
    Example:
        >>> validate_temperature(0.7)
        True
        >>> validate_temperature(3.0)
        InvalidInputError: Invalid temperature: out of range
    """
    from src.config import MIN_TEMPERATURE, MAX_TEMPERATURE
    
    if temperature < MIN_TEMPERATURE or temperature > MAX_TEMPERATURE:
        raise InvalidInputError(
            'temperature',
            temperature,
            f'out of range ({MIN_TEMPERATURE} - {MAX_TEMPERATURE})'
        )
    
    return True


# Convenience: Allow direct import
__all__ = [
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
]
