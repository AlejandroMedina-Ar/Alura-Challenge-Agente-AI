"""
Knowledge Library Service Module

This module provides business logic for knowledge library document management.
Handles document upload, deletion, listing, and metadata operations.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional
import os

from src.storage import (
    DocumentRepository,
    MetadataRepository,
    FileManager
)
from src.utils import (
    get_logger,
    DocumentNotFoundError,
    DocumentAlreadyExistsError,
    InvalidDocumentError
)


logger = get_logger()


class KnowledgeLibraryService:
    """
    Service for knowledge library document management.
    
    Features:
    - Upload documents (with duplicate detection)
    - Delete documents
    - List documents with metadata
    - Get document info
    - Search by filename
    """
    
    def __init__(self):
        """Initialize knowledge library service."""
        self.doc_repo = DocumentRepository()
        self.metadata_repo = MetadataRepository()
        self.file_manager = FileManager()
        logger.debug("KnowledgeLibraryService initialized")
    
    def upload_document(
        self,
        file_path: str,
        filename: str,
        file_type: str,
        file_size: int
    ) -> dict:
        """
        Upload document to knowledge library.
        
        Args:
            file_path: Path to uploaded file (temp location)
            filename: Original filename
            file_type: File MIME type
            file_size: File size in bytes
        
        Returns:
            dict: Document metadata
        
        Raises:
            DocumentAlreadyExistsError: If document exists
            InvalidDocumentError: If file is invalid
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> metadata = service.upload_document(
            ...     file_path="/tmp/upload.pdf",
            ...     filename="manual.pdf",
            ...     file_type="application/pdf",
            ...     file_size=1024000
            ... )
            >>> print(metadata['doc_id'])
        """
        try:
            # Check if document already exists
            if self.doc_repo.exists(filename):
                logger.warning(f"Document already exists", filename=filename)
                raise DocumentAlreadyExistsError(filename)
            
            # Save document file
            doc_id = self.file_manager.save_document(file_path, filename)
            
            # Create metadata
            metadata = self.metadata_repo.create_metadata(
                doc_id=doc_id,
                filename=filename,
                file_type=file_type,
                file_size=file_size
            )
            
            logger.info(
                f"Document uploaded",
                doc_id=doc_id,
                filename=filename,
                size=file_size
            )
            
            return metadata
            
        except (DocumentAlreadyExistsError, InvalidDocumentError):
            raise
        except Exception as e:
            logger.error(f"Document upload failed", filename=filename, error=str(e))
            raise InvalidDocumentError(f"Upload failed: {e}")
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete document from knowledge library.
        
        Removes both file and metadata.
        
        Args:
            doc_id: Document ID
        
        Returns:
            bool: True if deleted successfully
        
        Raises:
            DocumentNotFoundError: If document not found
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> service.delete_document("doc_123")
        """
        try:
            # Check if document exists
            metadata = self.metadata_repo.get_metadata(doc_id)
            if not metadata:
                raise DocumentNotFoundError(doc_id)
            
            filename = metadata['filename']
            
            # Delete file
            self.file_manager.delete_document(filename)
            
            # Delete metadata
            self.metadata_repo.delete_metadata(doc_id)
            
            logger.info(
                f"Document deleted",
                doc_id=doc_id,
                filename=filename
            )
            
            return True
            
        except DocumentNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Document deletion failed", doc_id=doc_id, error=str(e))
            return False
    
    def delete_document_by_filename(self, filename: str) -> bool:
        """
        Delete document by filename.
        
        Args:
            filename: Document filename
        
        Returns:
            bool: True if deleted
        
        Raises:
            DocumentNotFoundError: If not found
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> service.delete_document_by_filename("manual.pdf")
        """
        # Find document by filename
        doc_id = self.doc_repo.get_doc_id_by_filename(filename)
        
        if not doc_id:
            raise DocumentNotFoundError(filename)
        
        return self.delete_document(doc_id)
    
    def list_documents(self) -> list[dict]:
        """
        List all documents in knowledge library.
        
        Returns:
            list[dict]: List of document metadata
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> docs = service.list_documents()
            >>> for doc in docs:
            ...     print(f"{doc['filename']} - {doc['file_size']} bytes")
        """
        return self.metadata_repo.list_all_metadata()
    
    def get_document_info(self, doc_id: str) -> Optional[dict]:
        """
        Get document metadata.
        
        Args:
            doc_id: Document ID
        
        Returns:
            dict: Document metadata or None
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> info = service.get_document_info("doc_123")
            >>> if info:
            ...     print(info['filename'])
        """
        return self.metadata_repo.get_metadata(doc_id)
    
    def get_document_by_filename(self, filename: str) -> Optional[dict]:
        """
        Get document metadata by filename.
        
        Args:
            filename: Document filename
        
        Returns:
            dict: Document metadata or None
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> doc = service.get_document_by_filename("manual.pdf")
        """
        doc_id = self.doc_repo.get_doc_id_by_filename(filename)
        
        if not doc_id:
            return None
        
        return self.get_document_info(doc_id)
    
    def document_exists(self, filename: str) -> bool:
        """
        Check if document exists.
        
        Args:
            filename: Document filename
        
        Returns:
            bool: True if exists
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> if service.document_exists("manual.pdf"):
            ...     print("Document already uploaded")
        """
        return self.doc_repo.exists(filename)
    
    def get_document_count(self) -> int:
        """
        Get total number of documents.
        
        Returns:
            int: Document count
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> count = service.get_document_count()
            >>> print(f"Knowledge library has {count} documents")
        """
        return len(self.list_documents())
    
    def get_document_path(self, filename: str) -> str:
        """
        Get full path to document file.
        
        Args:
            filename: Document filename
        
        Returns:
            str: Full file path
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> path = service.get_document_path("manual.pdf")
            >>> with open(path, 'rb') as f:
            ...     content = f.read()
        """
        return self.file_manager.get_document_path(filename)
    
    def update_document_metadata(
        self,
        doc_id: str,
        **metadata_updates
    ) -> bool:
        """
        Update document metadata.
        
        Args:
            doc_id: Document ID
            **metadata_updates: Fields to update
        
        Returns:
            bool: True if updated
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> service.update_document_metadata(
            ...     doc_id="doc_123",
            ...     indexed=True,
            ...     chunk_count=42
            ... )
        """
        try:
            return self.metadata_repo.update_metadata(doc_id, **metadata_updates)
        except Exception as e:
            logger.error(f"Metadata update failed", doc_id=doc_id, error=str(e))
            return False
    
    def search_documents(self, query: str) -> list[dict]:
        """
        Search documents by filename.
        
        Simple substring matching on filenames.
        
        Args:
            query: Search query
        
        Returns:
            list[dict]: Matching documents
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> results = service.search_documents("manual")
            >>> for doc in results:
            ...     print(doc['filename'])
        """
        all_docs = self.list_documents()
        query_lower = query.lower()
        
        matching = [
            doc for doc in all_docs
            if query_lower in doc['filename'].lower()
        ]
        
        logger.debug(
            f"Document search",
            query=query,
            results=len(matching)
        )
        
        return matching
    
    def get_storage_stats(self) -> dict:
        """
        Get storage statistics.
        
        Returns:
            dict: Storage stats (total_documents, total_size, etc.)
        
        Example:
            >>> service = KnowledgeLibraryService()
            >>> stats = service.get_storage_stats()
            >>> print(f"Total size: {stats['total_size_mb']:.2f} MB")
        """
        all_docs = self.list_documents()
        
        total_size = sum(doc.get('file_size', 0) for doc in all_docs)
        indexed_count = sum(1 for doc in all_docs if doc.get('indexed', False))
        
        return {
            'total_documents': len(all_docs),
            'indexed_documents': indexed_count,
            'pending_documents': len(all_docs) - indexed_count,
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024)
        }


# Singleton instance
_kl_service_instance = None


def get_knowledge_library_service() -> KnowledgeLibraryService:
    """
    Get singleton KnowledgeLibraryService instance.
    
    Returns:
        KnowledgeLibraryService: Singleton instance
    
    Example:
        >>> from src.services import get_knowledge_library_service
        >>> kl_service = get_knowledge_library_service()
        >>> docs = kl_service.list_documents()
    """
    global _kl_service_instance
    
    if _kl_service_instance is None:
        _kl_service_instance = KnowledgeLibraryService()
        logger.debug("KnowledgeLibraryService singleton created")
    
    return _kl_service_instance


# Convenience: Allow direct import
__all__ = [
    'KnowledgeLibraryService',
    'get_knowledge_library_service',
]
