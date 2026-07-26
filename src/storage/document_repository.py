"""
Document Repository Module

This module manages document records in the knowledge library.
Provides CRUD operations for document files.

Author: TechFlow AI Project
License: MIT
"""

from pathlib import Path
from typing import Optional

from src.config import get_paths, FileFormat, get_file_format
from src.utils import (
    get_logger,
    FileNotFoundError,
    DuplicateDocumentError,
    DocumentNotFoundError,
    validate_filename,
    validate_file_format,
    validate_file_size
)
from src.storage.file_manager import FileManager


logger = get_logger()


class DocumentRepository:
    """
    Repository for managing documents in the knowledge library.
    
    Features:
    - Add documents with duplicate detection
    - Retrieve document information
    - Delete documents
    - List all documents
    - Check document existence
    
    All operations are coordinated with FileManager and MetadataRepository.
    """
    
    def __init__(self):
        """Initialize document repository."""
        self.paths = get_paths()
        self.file_manager = FileManager()
        logger.debug("DocumentRepository initialized")
    
    def add_document(
        self,
        content: bytes,
        filename: str,
        allow_duplicates: bool = False
    ) -> dict:
        """
        Add new document to knowledge library.
        
        Args:
            content: Document content as bytes
            filename: Document filename
            allow_duplicates: If False, raise error if document exists
        
        Returns:
            dict: Document info (filename, path, size, format, checksum)
        
        Raises:
            DuplicateDocumentError: If document exists and allow_duplicates=False
            UnsupportedFileFormatError: If file format is not supported
            FileTooLargeError: If file exceeds size limit
            InvalidFilenameError: If filename is invalid
        
        Example:
            >>> repo = DocumentRepository()
            >>> with open('doc.pdf', 'rb') as f:
            ...     content = f.read()
            >>> info = repo.add_document(content, 'doc.pdf')
            >>> print(info['filename'])
            'doc.pdf'
        """
        # Validate filename
        validate_filename(filename)
        
        # Validate file format
        file_format = validate_file_format(filename)
        
        # Validate file size
        validate_file_size(filename, len(content), file_format)
        
        # Check for duplicates
        if not allow_duplicates and self.document_exists(filename):
            logger.warning(f"Duplicate document upload attempt", filename=filename)
            raise DuplicateDocumentError(filename)
        
        # Save file
        file_path = self.file_manager.save_file(content, filename, allow_duplicates)
        
        # Get file info
        actual_filename = file_path.name
        checksum = self.file_manager.get_file_checksum(actual_filename)
        
        doc_info = {
            'filename': actual_filename,
            'original_filename': filename,
            'path': str(file_path),
            'size': len(content),
            'format': file_format.value,
            'checksum': checksum
        }
        
        logger.info(
            f"Document added to knowledge library",
            filename=actual_filename,
            size=len(content),
            format=file_format.value
        )
        
        return doc_info
    
    def get_document(self, filename: str) -> bytes:
        """
        Retrieve document content.
        
        Args:
            filename: Document filename
        
        Returns:
            bytes: Document content
        
        Raises:
            DocumentNotFoundError: If document doesn't exist
        
        Example:
            >>> repo = DocumentRepository()
            >>> content = repo.get_document('doc.pdf')
            >>> print(len(content))
            1048576
        """
        if not self.document_exists(filename):
            raise DocumentNotFoundError(filename)
        
        try:
            return self.file_manager.read_file(filename)
        except FileNotFoundError:
            raise DocumentNotFoundError(filename)
    
    def get_document_path(self, filename: str) -> Path:
        """
        Get full path to document file.
        
        Args:
            filename: Document filename
        
        Returns:
            Path: Full path to document
        
        Raises:
            DocumentNotFoundError: If document doesn't exist
        
        Example:
            >>> repo = DocumentRepository()
            >>> path = repo.get_document_path('doc.pdf')
            >>> print(path)
            WindowsPath('.../documents/doc.pdf')
        """
        if not self.document_exists(filename):
            raise DocumentNotFoundError(filename)
        
        return self.paths.get_document_path(filename)
    
    def delete_document(self, filename: str) -> bool:
        """
        Delete document from knowledge library.
        
        Args:
            filename: Document filename
        
        Returns:
            bool: True if document was deleted
        
        Raises:
            DocumentNotFoundError: If document doesn't exist
        
        Example:
            >>> repo = DocumentRepository()
            >>> repo.delete_document('doc.pdf')
            True
        """
        if not self.document_exists(filename):
            raise DocumentNotFoundError(filename)
        
        try:
            self.file_manager.delete_file(filename)
            logger.info(f"Document deleted from knowledge library", filename=filename)
            return True
        except FileNotFoundError:
            raise DocumentNotFoundError(filename)
    
    def document_exists(self, filename: str) -> bool:
        """
        Check if document exists in knowledge library.
        
        Args:
            filename: Document filename
        
        Returns:
            bool: True if document exists
        
        Example:
            >>> repo = DocumentRepository()
            >>> repo.document_exists('doc.pdf')
            True
        """
        return self.file_manager.file_exists(filename)
    
    def list_documents(self, extension: Optional[str] = None) -> list[dict]:
        """
        List all documents in knowledge library.
        
        Args:
            extension: Filter by extension (e.g., '.pdf'). None = all files
        
        Returns:
            list[dict]: List of document info dicts
        
        Example:
            >>> repo = DocumentRepository()
            >>> docs = repo.list_documents(extension='.pdf')
            >>> for doc in docs:
            ...     print(doc['filename'], doc['size'])
            doc1.pdf 1048576
            doc2.pdf 2097152
        """
        pattern = f"*{extension}" if extension else "*"
        file_paths = self.file_manager.list_files(pattern)
        
        documents = []
        for file_path in file_paths:
            try:
                file_format = get_file_format(file_path.suffix)
                if file_format is None:
                    continue
                
                documents.append({
                    'filename': file_path.name,
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'format': file_format.value
                })
            except Exception as e:
                logger.error(
                    f"Error reading document info",
                    filename=file_path.name,
                    error=str(e)
                )
                continue
        
        logger.debug(f"Listed {len(documents)} documents", extension=extension)
        return documents
    
    def get_document_count(self) -> int:
        """
        Get total number of documents in knowledge library.
        
        Returns:
            int: Number of documents
        
        Example:
            >>> repo = DocumentRepository()
            >>> count = repo.get_document_count()
            >>> print(f"Knowledge library has {count} documents")
            Knowledge library has 42 documents
        """
        return self.file_manager.get_file_count()
    
    def get_total_size(self) -> int:
        """
        Get total size of all documents.
        
        Returns:
            int: Total size in bytes
        
        Example:
            >>> repo = DocumentRepository()
            >>> size = repo.get_total_size()
            >>> from src.config import format_file_size
            >>> print(format_file_size(size))
            '125.5 MB'
        """
        return self.file_manager.get_total_size()
    
    def get_document_info(self, filename: str) -> dict:
        """
        Get detailed information about a document.
        
        Args:
            filename: Document filename
        
        Returns:
            dict: Document information
        
        Raises:
            DocumentNotFoundError: If document doesn't exist
        
        Example:
            >>> repo = DocumentRepository()
            >>> info = repo.get_document_info('doc.pdf')
            >>> print(info)
            {
                'filename': 'doc.pdf',
                'path': '.../documents/doc.pdf',
                'size': 1048576,
                'format': 'pdf',
                'checksum': 'a3f5b2c1...'
            }
        """
        if not self.document_exists(filename):
            raise DocumentNotFoundError(filename)
        
        file_path = self.paths.get_document_path(filename)
        file_format = get_file_format(file_path.suffix)
        
        return {
            'filename': filename,
            'path': str(file_path),
            'size': self.file_manager.get_file_size(filename),
            'format': file_format.value if file_format else 'unknown',
            'checksum': self.file_manager.get_file_checksum(filename)
        }
    
    def is_empty(self) -> bool:
        """
        Check if knowledge library is empty.
        
        Returns:
            bool: True if no documents exist
        
        Example:
            >>> repo = DocumentRepository()
            >>> if repo.is_empty():
            ...     print("Please upload documents")
        """
        return self.get_document_count() == 0
    
    def clear_all(self) -> int:
        """
        Delete all documents from knowledge library.
        
        **WARNING:** This is destructive and cannot be undone!
        
        Returns:
            int: Number of documents deleted
        
        Example:
            >>> repo = DocumentRepository()
            >>> deleted = repo.clear_all()
            >>> print(f"Deleted {deleted} documents")
        """
        deleted = self.file_manager.clear_all_files()
        logger.warning(f"Knowledge library cleared", documents_deleted=deleted)
        return deleted


# Convenience: Allow direct import
__all__ = [
    'DocumentRepository',
]
