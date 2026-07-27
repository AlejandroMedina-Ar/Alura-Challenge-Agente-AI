"""
Metadata Repository Module

This module manages document metadata in JSON files.
Provides CRUD operations for metadata records.

Author: TechFlow Solutions Project
License: MIT
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.config import get_paths, MetadataField
from src.utils import (
    get_logger,
    MetadataNotFoundError,
    WriteError,
    ReadError,
    safe_json_load,
    safe_json_save
)


logger = get_logger()


class MetadataRepository:
    """
    Repository for managing document metadata.
    
    Metadata is stored as individual JSON files (one per document).
    
    Features:
    - Create metadata for new documents
    - Retrieve metadata by document name
    - Update metadata fields
    - Delete metadata
    - List all metadata records
    - Search metadata by criteria
    
    Metadata Structure:
    {
        "document_name": "example.pdf",
        "upload_date": "2026-07-26T10:30:00",
        "file_size": 1048576,
        "file_format": "pdf",
        "checksum": "a3f5b2c1...",
        "indexed": false,
        "index_date": null,
        "chunk_count": 0,
        "tags": [],
        "description": ""
    }
    """
    
    def __init__(self):
        """Initialize metadata repository."""
        self.paths = get_paths()
        logger.debug("MetadataRepository initialized")
    
    def _get_metadata_path(self, document_name: str) -> Path:
        """
        Get path to metadata file for a document.
        
        Args:
            document_name: Name of the document
        
        Returns:
            Path: Full path to metadata JSON file
        """
        # Metadata filename: document_name.json
        # Example: "example.pdf" -> "example.pdf.json"
        metadata_filename = f"{document_name}.json"
        return self.paths.get_metadata_path(metadata_filename)
    
    def create_metadata(
        self,
        document_name: str,
        file_size: int,
        file_format: str,
        checksum: str,
        description: str = "",
        tags: Optional[list[str]] = None
    ) -> dict:
        """
        Create metadata record for a new document.
        
        Args:
            document_name: Name of the document file
            file_size: File size in bytes
            file_format: File format (pdf, txt, docx, etc.)
            checksum: SHA256 checksum of file
            description: Optional document description
            tags: Optional list of tags
        
        Returns:
            dict: Created metadata record
        
        Raises:
            WriteError: If metadata cannot be saved
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.create_metadata(
            ...     document_name='doc.pdf',
            ...     file_size=1048576,
            ...     file_format='pdf',
            ...     checksum='abc123...',
            ...     description='Important document',
            ...     tags=['work', 'report']
            ... )
            >>> print(meta['document_name'])
            'doc.pdf'
        """
        metadata = {
            MetadataField.DOCUMENT_NAME: document_name,
            MetadataField.UPLOAD_DATE: datetime.now().isoformat(),
            MetadataField.FILE_SIZE: file_size,
            MetadataField.FILE_FORMAT: file_format,
            MetadataField.CHECKSUM: checksum,
            MetadataField.INDEXED: False,
            MetadataField.INDEX_DATE: None,
            MetadataField.CHUNK_COUNT: 0,
            MetadataField.TAGS: tags or [],
            MetadataField.DESCRIPTION: description
        }
        
        metadata_path = self._get_metadata_path(document_name)
        
        try:
            safe_json_save(metadata_path, metadata)
            logger.info(
                f"Metadata created",
                document=document_name,
                size=file_size,
                format=file_format
            )
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to create metadata", document=document_name, exc_info=True)
            raise WriteError(str(metadata_path), str(e))
    
    def get_metadata(self, document_name: str) -> dict:
        """
        Retrieve metadata for a document.
        
        Args:
            document_name: Name of the document
        
        Returns:
            dict: Metadata record
        
        Raises:
            MetadataNotFoundError: If metadata doesn't exist
            ReadError: If metadata cannot be read
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.get_metadata('doc.pdf')
            >>> print(meta['upload_date'])
            '2026-07-26T10:30:00'
        """
        metadata_path = self._get_metadata_path(document_name)
        
        if not metadata_path.exists():
            raise MetadataNotFoundError(document_name)
        
        try:
            metadata = safe_json_load(metadata_path)
            logger.debug(f"Metadata retrieved", document=document_name)
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to read metadata", document=document_name, exc_info=True)
            raise ReadError(str(metadata_path), str(e))
    
    def update_metadata(
        self,
        document_name: str,
        updates: dict
    ) -> dict:
        """
        Update metadata fields for a document.
        
        Args:
            document_name: Name of the document
            updates: Dict of fields to update
        
        Returns:
            dict: Updated metadata record
        
        Raises:
            MetadataNotFoundError: If metadata doesn't exist
            WriteError: If metadata cannot be saved
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.update_metadata('doc.pdf', {
            ...     'indexed': True,
            ...     'chunk_count': 42,
            ...     'index_date': datetime.now().isoformat()
            ... })
        """
        # Get existing metadata
        metadata = self.get_metadata(document_name)
        
        # Apply updates
        metadata.update(updates)
        
        # Save updated metadata
        metadata_path = self._get_metadata_path(document_name)
        
        try:
            safe_json_save(metadata_path, metadata)
            logger.info(
                f"Metadata updated",
                document=document_name,
                fields=list(updates.keys())
            )
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to update metadata", document=document_name, exc_info=True)
            raise WriteError(str(metadata_path), str(e))
    
    def delete_metadata(self, document_name: str) -> bool:
        """
        Delete metadata for a document.
        
        Args:
            document_name: Name of the document
        
        Returns:
            bool: True if metadata was deleted
        
        Raises:
            MetadataNotFoundError: If metadata doesn't exist
        
        Example:
            >>> repo = MetadataRepository()
            >>> repo.delete_metadata('doc.pdf')
            True
        """
        metadata_path = self._get_metadata_path(document_name)
        
        if not metadata_path.exists():
            raise MetadataNotFoundError(document_name)
        
        try:
            metadata_path.unlink()
            logger.info(f"Metadata deleted", document=document_name)
            return True
            
        except OSError as e:
            logger.error(f"Failed to delete metadata", document=document_name, exc_info=True)
            raise WriteError(str(metadata_path), f"delete failed: {e}")
    
    def metadata_exists(self, document_name: str) -> bool:
        """
        Check if metadata exists for a document.
        
        Args:
            document_name: Name of the document
        
        Returns:
            bool: True if metadata exists
        
        Example:
            >>> repo = MetadataRepository()
            >>> repo.metadata_exists('doc.pdf')
            True
        """
        metadata_path = self._get_metadata_path(document_name)
        return metadata_path.exists()
    
    def list_all_metadata(self) -> list[dict]:
        """
        List all metadata records.
        
        Returns:
            list[dict]: List of all metadata records
        
        Example:
            >>> repo = MetadataRepository()
            >>> all_meta = repo.list_all_metadata()
            >>> for meta in all_meta:
            ...     print(meta['document_name'])
        """
        metadata_files = self.paths.METADATA_DIR.glob("*.json")
        
        all_metadata = []
        for metadata_path in metadata_files:
            try:
                metadata = safe_json_load(metadata_path)
                all_metadata.append(metadata)
            except Exception as e:
                logger.error(
                    f"Failed to read metadata file",
                    file=metadata_path.name,
                    error=str(e)
                )
                continue
        
        logger.debug(f"Listed {len(all_metadata)} metadata records")
        return all_metadata
    
    def get_indexed_documents(self) -> list[dict]:
        """
        Get metadata for all indexed documents.
        
        Returns:
            list[dict]: List of metadata for indexed documents
        
        Example:
            >>> repo = MetadataRepository()
            >>> indexed = repo.get_indexed_documents()
            >>> print(f"{len(indexed)} documents are indexed")
        """
        all_metadata = self.list_all_metadata()
        indexed = [m for m in all_metadata if m.get(MetadataField.INDEXED, False)]
        
        logger.debug(f"Found {len(indexed)} indexed documents")
        return indexed
    
    def get_unindexed_documents(self) -> list[dict]:
        """
        Get metadata for all unindexed documents.
        
        Returns:
            list[dict]: List of metadata for unindexed documents
        
        Example:
            >>> repo = MetadataRepository()
            >>> unindexed = repo.get_unindexed_documents()
            >>> print(f"{len(unindexed)} documents need indexing")
        """
        all_metadata = self.list_all_metadata()
        unindexed = [m for m in all_metadata if not m.get(MetadataField.INDEXED, False)]
        
        logger.debug(f"Found {len(unindexed)} unindexed documents")
        return unindexed
    
    def mark_as_indexed(
        self,
        document_name: str,
        chunk_count: int
    ) -> dict:
        """
        Mark document as indexed with chunk information.
        
        Args:
            document_name: Name of the document
            chunk_count: Number of chunks created
        
        Returns:
            dict: Updated metadata
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.mark_as_indexed('doc.pdf', chunk_count=42)
        """
        updates = {
            MetadataField.INDEXED: True,
            MetadataField.INDEX_DATE: datetime.now().isoformat(),
            MetadataField.CHUNK_COUNT: chunk_count
        }
        
        return self.update_metadata(document_name, updates)
    
    def mark_as_unindexed(self, document_name: str) -> dict:
        """
        Mark document as unindexed (for re-indexing).
        
        Args:
            document_name: Name of the document
        
        Returns:
            dict: Updated metadata
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.mark_as_unindexed('doc.pdf')
        """
        updates = {
            MetadataField.INDEXED: False,
            MetadataField.INDEX_DATE: None,
            MetadataField.CHUNK_COUNT: 0
        }
        
        return self.update_metadata(document_name, updates)
    
    def add_tags(self, document_name: str, new_tags: list[str]) -> dict:
        """
        Add tags to document metadata.
        
        Args:
            document_name: Name of the document
            new_tags: Tags to add
        
        Returns:
            dict: Updated metadata
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.add_tags('doc.pdf', ['important', 'reviewed'])
        """
        metadata = self.get_metadata(document_name)
        current_tags = metadata.get(MetadataField.TAGS, [])
        
        # Add new tags (avoid duplicates)
        updated_tags = list(set(current_tags + new_tags))
        
        return self.update_metadata(document_name, {MetadataField.TAGS: updated_tags})
    
    def remove_tags(self, document_name: str, tags_to_remove: list[str]) -> dict:
        """
        Remove tags from document metadata.
        
        Args:
            document_name: Name of the document
            tags_to_remove: Tags to remove
        
        Returns:
            dict: Updated metadata
        
        Example:
            >>> repo = MetadataRepository()
            >>> meta = repo.remove_tags('doc.pdf', ['draft'])
        """
        metadata = self.get_metadata(document_name)
        current_tags = metadata.get(MetadataField.TAGS, [])
        
        # Remove specified tags
        updated_tags = [t for t in current_tags if t not in tags_to_remove]
        
        return self.update_metadata(document_name, {MetadataField.TAGS: updated_tags})
    
    def search_by_tags(self, tags: list[str], match_all: bool = False) -> list[dict]:
        """
        Search documents by tags.
        
        Args:
            tags: Tags to search for
            match_all: If True, document must have ALL tags. If False, ANY tag matches
        
        Returns:
            list[dict]: List of matching metadata records
        
        Example:
            >>> repo = MetadataRepository()
            >>> # Find documents with 'work' OR 'report' tag
            >>> docs = repo.search_by_tags(['work', 'report'], match_all=False)
            >>> # Find documents with BOTH 'work' AND 'report' tags
            >>> docs = repo.search_by_tags(['work', 'report'], match_all=True)
        """
        all_metadata = self.list_all_metadata()
        
        matching = []
        for metadata in all_metadata:
            doc_tags = metadata.get(MetadataField.TAGS, [])
            
            if match_all:
                # Document must have ALL specified tags
                if all(tag in doc_tags for tag in tags):
                    matching.append(metadata)
            else:
                # Document must have ANY of the specified tags
                if any(tag in doc_tags for tag in tags):
                    matching.append(metadata)
        
        logger.debug(
            f"Tag search found {len(matching)} documents",
            tags=tags,
            match_all=match_all
        )
        return matching
    
    def get_statistics(self) -> dict:
        """
        Get statistics about metadata repository.
        
        Returns:
            dict: Statistics (total, indexed, unindexed, total_size, etc.)
        
        Example:
            >>> repo = MetadataRepository()
            >>> stats = repo.get_statistics()
            >>> print(stats)
            {
                'total_documents': 42,
                'indexed_documents': 38,
                'unindexed_documents': 4,
                'total_size': 104857600,
                'total_chunks': 1234
            }
        """
        all_metadata = self.list_all_metadata()
        indexed_metadata = [m for m in all_metadata if m.get(MetadataField.INDEXED, False)]
        
        stats = {
            'total_documents': len(all_metadata),
            'indexed_documents': len(indexed_metadata),
            'unindexed_documents': len(all_metadata) - len(indexed_metadata),
            'total_size': sum(m.get(MetadataField.FILE_SIZE, 0) for m in all_metadata),
            'total_chunks': sum(m.get(MetadataField.CHUNK_COUNT, 0) for m in indexed_metadata)
        }
        
        logger.debug(f"Metadata statistics calculated", **stats)
        return stats
    
    def clear_all(self) -> int:
        """
        Delete all metadata files.
        
        **WARNING:** This is destructive and cannot be undone!
        
        Returns:
            int: Number of metadata files deleted
        
        Example:
            >>> repo = MetadataRepository()
            >>> deleted = repo.clear_all()
        """
        metadata_files = list(self.paths.METADATA_DIR.glob("*.json"))
        deleted = 0
        
        for metadata_path in metadata_files:
            try:
                metadata_path.unlink()
                deleted += 1
            except OSError as e:
                logger.error(f"Failed to delete metadata file", file=metadata_path.name)
                continue
        
        logger.warning(f"All metadata cleared", count=deleted)
        return deleted


# Convenience: Allow direct import
__all__ = [
    'MetadataRepository',
]
