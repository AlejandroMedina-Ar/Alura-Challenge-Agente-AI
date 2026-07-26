"""
Helper Functions Module

This module provides utility functions used throughout the application.
Functions are organized by category for easy discovery.

Author: TechFlow Solutions Project
License: MIT
"""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import bcrypt

from src.config import format_file_size


# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    
    Args:
        password: Plain text password
    
    Returns:
        str: Bcrypt hash string
    
    Example:
        >>> hashed = hash_password('mypassword')
        >>> print(hashed)
        '$2b$12$...'
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against bcrypt hash.
    
    Args:
        password: Plain text password
        hashed: Bcrypt hash string
    
    Returns:
        bool: True if password matches hash
    
    Example:
        >>> hashed = hash_password('mypassword')
        >>> verify_password('mypassword', hashed)
        True
        >>> verify_password('wrongpassword', hashed)
        False
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


# ==========================================
# FILE CHECKSUMS
# ==========================================

def calculate_file_checksum(file_path: Path, algorithm: str = 'sha256') -> str:
    """
    Calculate checksum of a file.
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (default: sha256)
    
    Returns:
        str: Hexadecimal checksum string
    
    Example:
        >>> from pathlib import Path
        >>> checksum = calculate_file_checksum(Path('document.pdf'))
        >>> print(checksum)
        'a3f5...'
    """
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def calculate_content_checksum(content: bytes, algorithm: str = 'sha256') -> str:
    """
    Calculate checksum of byte content.
    
    Args:
        content: Byte content
        algorithm: Hash algorithm (default: sha256)
    
    Returns:
        str: Hexadecimal checksum string
    
    Example:
        >>> checksum = calculate_content_checksum(b'Hello, world!')
        >>> print(checksum)
        '315f5...'
    """
    hash_func = hashlib.new(algorithm)
    hash_func.update(content)
    return hash_func.hexdigest()


# ==========================================
# FILENAME SANITIZATION
# ==========================================

def sanitize_filename(filename: str, replacement: str = '_') -> str:
    """
    Sanitize filename by replacing invalid characters.
    
    Args:
        filename: Original filename
        replacement: Character to use for replacement (default: '_')
    
    Returns:
        str: Sanitized filename
    
    Example:
        >>> sanitize_filename('my<file>name.pdf')
        'my_file_name.pdf'
        >>> sanitize_filename('file: document.txt')
        'file_ document.txt'
    """
    # Replace invalid characters with replacement
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, replacement, filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure we still have a filename
    if not sanitized:
        sanitized = 'unnamed'
    
    return sanitized


def generate_unique_filename(base_filename: str, existing_files: list[str]) -> str:
    """
    Generate unique filename by appending number if needed.
    
    Args:
        base_filename: Original filename
        existing_files: List of existing filenames
    
    Returns:
        str: Unique filename
    
    Example:
        >>> generate_unique_filename('doc.pdf', ['doc.pdf', 'doc (1).pdf'])
        'doc (2).pdf'
    """
    if base_filename not in existing_files:
        return base_filename
    
    # Split name and extension
    path = Path(base_filename)
    name = path.stem
    ext = path.suffix
    
    # Find next available number
    counter = 1
    while True:
        new_filename = f"{name} ({counter}){ext}"
        if new_filename not in existing_files:
            return new_filename
        counter += 1


# ==========================================
# DATE/TIME FORMATTING
# ==========================================

def format_timestamp(timestamp: Optional[str] = None, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format timestamp or current time.
    
    Args:
        timestamp: ISO format timestamp (default: current time)
        format: strftime format string
    
    Returns:
        str: Formatted timestamp
    
    Example:
        >>> format_timestamp()
        '2026-07-26 10:30:45'
        >>> format_timestamp('2026-07-26T10:30:45', '%Y/%m/%d')
        '2026/07/26'
    """
    if timestamp is None:
        dt = datetime.now()
    else:
        # Parse ISO format
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    
    return dt.strftime(format)


def get_iso_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        str: ISO format timestamp
    
    Example:
        >>> get_iso_timestamp()
        '2026-07-26T10:30:45.123456'
    """
    return datetime.now().isoformat()


def format_duration_seconds(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        str: Formatted duration
    
    Example:
        >>> format_duration_seconds(65)
        '1m 5s'
        >>> format_duration_seconds(3661)
        '1h 1m 1s'
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    return f"{hours}h {remaining_minutes}m {remaining_seconds}s"


# ==========================================
# TEXT UTILITIES
# ==========================================

def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to append (default: '...')
    
    Returns:
        str: Truncated text
    
    Example:
        >>> truncate_text('This is a long text', 10)
        'This is...'
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def count_tokens_estimate(text: str) -> int:
    """
    Estimate token count (rough approximation).
    
    Uses simple heuristic: ~4 characters per token on average.
    
    Args:
        text: Text to estimate
    
    Returns:
        int: Estimated token count
    
    Example:
        >>> count_tokens_estimate('Hello, world!')
        3
    """
    # Rough estimate: 4 characters per token
    return len(text) // 4


def clean_whitespace(text: str) -> str:
    """
    Clean excessive whitespace from text.
    
    Args:
        text: Text to clean
    
    Returns:
        str: Cleaned text
    
    Example:
        >>> clean_whitespace('Hello    world\\n\\n\\nTest')
        'Hello world\\nTest'
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text.strip()


# ==========================================
# JSON UTILITIES
# ==========================================

def safe_json_load(file_path: Path, default: Any = None) -> Any:
    """
    Safely load JSON file with fallback to default.
    
    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid
    
    Returns:
        Any: Parsed JSON or default value
    
    Example:
        >>> data = safe_json_load(Path('config.json'), default={})
        >>> print(data)
        {...}
    """
    if not file_path.exists():
        return default
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def safe_json_save(file_path: Path, data: Any, indent: int = 2) -> bool:
    """
    Safely save data to JSON file.
    
    Args:
        file_path: Path to JSON file
        data: Data to save
        indent: JSON indentation (default: 2)
    
    Returns:
        bool: True if successful
    
    Example:
        >>> safe_json_save(Path('data.json'), {'key': 'value'})
        True
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        return True
    except (OSError, TypeError):
        return False


# ==========================================
# LIST UTILITIES
# ==========================================

def chunk_list(items: list, chunk_size: int) -> list[list]:
    """
    Split list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        list[list]: List of chunks
    
    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def deduplicate_list(items: list, key: callable = None) -> list:
    """
    Remove duplicates from list while preserving order.
    
    Args:
        items: List to deduplicate
        key: Function to extract comparison key (default: identity)
    
    Returns:
        list: Deduplicated list
    
    Example:
        >>> deduplicate_list([1, 2, 2, 3, 1])
        [1, 2, 3]
        >>> deduplicate_list([{'id': 1}, {'id': 2}, {'id': 1}], key=lambda x: x['id'])
        [{'id': 1}, {'id': 2}]
    """
    seen = set()
    result = []
    
    for item in items:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            result.append(item)
    
    return result


# ==========================================
# DISPLAY HELPERS
# ==========================================

def format_number(number: int) -> str:
    """
    Format number with thousands separators.
    
    Args:
        number: Number to format
    
    Returns:
        str: Formatted number
    
    Example:
        >>> format_number(1234567)
        '1,234,567'
    """
    return f"{number:,}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Value between 0 and 1
        decimals: Number of decimal places
    
    Returns:
        str: Formatted percentage
    
    Example:
        >>> format_percentage(0.856)
        '85.6%'
    """
    return f"{value * 100:.{decimals}f}%"


# Convenience: Allow direct import
__all__ = [
    # Password
    'hash_password',
    'verify_password',
    
    # Checksums
    'calculate_file_checksum',
    'calculate_content_checksum',
    
    # Filename
    'sanitize_filename',
    'generate_unique_filename',
    
    # Date/Time
    'format_timestamp',
    'get_iso_timestamp',
    'format_duration_seconds',
    
    # Text
    'truncate_text',
    'count_tokens_estimate',
    'clean_whitespace',
    
    # JSON
    'safe_json_load',
    'safe_json_save',
    
    # Lists
    'chunk_list',
    'deduplicate_list',
    
    # Display
    'format_number',
    'format_percentage',
]
