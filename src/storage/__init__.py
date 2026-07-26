"""
Storage Package

This package handles all data persistence and storage operations.

Modules:
- file_manager: Low-level file operations
- document_repository: Document CRUD operations
- metadata_repository: Document metadata management
- config_repository: Runtime configuration management

Author: TechFlow AI Project
License: MIT
"""

from .file_manager import FileManager
from .document_repository import DocumentRepository
from .metadata_repository import MetadataRepository
from .config_repository import ConfigRepository


__all__ = [
    # Classes
    'FileManager',
    'DocumentRepository',
    'MetadataRepository',
    'ConfigRepository',
]
