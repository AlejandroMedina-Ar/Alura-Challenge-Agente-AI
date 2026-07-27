"""
Indexing Service Module

This module provides business logic for document indexing.
Coordinates chunking, embedding, and vector store operations.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional

from src.storage import FileManager, MetadataRepository
from src.rag import (
    get_text_chunker,
    get_embedding_service,
    get_vector_store
)
from src.utils import (
    get_logger,
    DocumentNotFoundError,
    IndexingError
)


logger = get_logger()


class IndexingService:
    """
    Service for document indexing operations.
    
    Features:
    - Index single document (chunk + embed + store)
    - Batch indexing
    - Re-index document
    - Remove document from index
    - Index statistics
    
    Workflow:
    1. Load document from storage
    2. Chunk text
    3. Generate embeddings
    4. Store in vector database
    5. Update metadata
    """
    
    def __init__(self):
        """Initialize indexing service."""
        from src.services.knowledge_library_service import get_knowledge_library_service
        self.file_manager = FileManager()
        self.meta_repo = MetadataRepository()
        self.kl_service = get_knowledge_library_service()
        self.chunker = get_text_chunker()
        self.embedding_service = get_embedding_service()
        self.vector_store = get_vector_store()
        logger.debug("IndexingService initialized")
    
    def index_document(self, doc_id: str, filename: str) -> dict:
        """
        Index a single document.
        
        Args:
            doc_id: Document ID
            filename: Document filename
        
        Returns:
            dict: Indexing results (chunk_count, success)
        
        Raises:
            DocumentNotFoundError: If document not found
            IndexingError: If indexing fails
        
        Example:
            >>> service = IndexingService()
            >>> result = service.index_document("doc_123", "manual.pdf")
            >>> print(f"Indexed {result['chunk_count']} chunks")
        """
        try:
            logger.info(f"Starting document indexing", doc_id=doc_id, filename=filename)
            
            # Get document path
            doc_path = self.kl_service.get_document_path(filename)
            
            # Read document as bytes
            file_bytes = self.file_manager.read_file(filename)
            
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                from PyPDF2 import PdfReader
                import io
                reader = PdfReader(io.BytesIO(file_bytes))
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text() + "\n"
            elif filename.lower().endswith(('.txt', '.md')):
                text_content = file_bytes.decode('utf-8')
            elif filename.lower().endswith('.docx'):
                from docx import Document
                import io
                doc = Document(io.BytesIO(file_bytes))
                text_content = "\n".join([para.text for para in doc.paragraphs])
            else:
                # Try to decode as text
                text_content = file_bytes.decode('utf-8')
            
            if not text_content or not text_content.strip():
                raise IndexingError(filename, "Document is empty or contains no extractable text")
            
            # Chunk document
            chunks = self.chunker.chunk_text(text_content)
            
            if not chunks:
                raise IndexingError(filename, "No chunks generated")
            
            logger.info(f"Document chunked", doc_id=doc_id, chunk_count=len(chunks))
            
            # Prepare metadatas
            metadatas = [
                {
                    'source': filename,
                    'doc_id': doc_id,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            # Generate embeddings (batch)
            embeddings = self.embedding_service.generate_embeddings_batch(chunks)
            
            logger.info(f"Embeddings generated", doc_id=doc_id, count=len(embeddings))
            
            # Generate chunk IDs
            ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
            
            # Add to vector store
            self.vector_store.add_documents(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            logger.info(f"Chunks added to vector store", doc_id=doc_id)
            
            # Update document metadata
            self.meta_repo.update_metadata(
                document_name=filename,
                updates={
                    'indexed': True,
                    'chunk_count': len(chunks),
                    'index_date': __import__('datetime').datetime.now().isoformat()
                }
            )
            
            logger.info(
                f"Document indexing completed",
                doc_id=doc_id,
                filename=filename,
                chunk_count=len(chunks)
            )
            
            return {
                'success': True,
                'doc_id': doc_id,
                'filename': filename,
                'chunk_count': len(chunks),
                'embedding_dimension': len(embeddings[0]) if embeddings else 0
            }
            
        except DocumentNotFoundError:
            raise
        except Exception as e:
            logger.error(
                f"Document indexing failed",
                doc_id=doc_id,
                filename=filename,
                error=str(e),
                exc_info=True
            )
            raise IndexingError(filename, str(e))
    
    def remove_document_from_index(self, doc_id: str) -> bool:
        """
        Remove document chunks from vector store.
        
        Args:
            doc_id: Document ID
        
        Returns:
            bool: True if removed successfully
        
        Example:
            >>> service = IndexingService()
            >>> service.remove_document_from_index("doc_123")
        """
        try:
            # Try to get filename from doc_id (usually doc_id is the filename)
            # Get document metadata to find chunk count
            try:
                metadata = self.meta_repo.get_metadata(doc_id)
            except:
                # If doc_id doesn't work, it might BE the filename
                logger.warning(f"Could not find metadata for doc_id, trying as filename", doc_id=doc_id)
                return False
            
            if not metadata:
                logger.warning(f"Document metadata not found", doc_id=doc_id)
                return False
            
            chunk_count = metadata.get('chunk_count', 0)
            
            if chunk_count == 0:
                logger.info(f"No chunks to remove", doc_id=doc_id)
                return True
            
            # Generate chunk IDs
            chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(chunk_count)]
            
            # Delete from vector store
            self.vector_store.delete_documents(chunk_ids)
            
            # Update metadata
            filename = metadata.get('filename', doc_id)
            self.meta_repo.update_metadata(
                document_name=filename,
                updates={
                    'indexed': False,
                    'chunk_count': 0
                }
            )
            
            logger.info(
                f"Document removed from index",
                doc_id=doc_id,
                chunks_removed=chunk_count
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove document from index", doc_id=doc_id, error=str(e))
            return False
    
    def reindex_document(self, doc_id: str, filename: str) -> dict:
        """
        Re-index an existing document.
        
        Removes old chunks and creates new index.
        
        Args:
            doc_id: Document ID
            filename: Document filename
        
        Returns:
            dict: Indexing results
        
        Example:
            >>> service = IndexingService()
            >>> result = service.reindex_document("doc_123", "manual.pdf")
        """
        logger.info(f"Re-indexing document", doc_id=doc_id)
        
        # Remove old index
        self.remove_document_from_index(doc_id)
        
        # Create new index
        return self.index_document(doc_id, filename)
    
    def batch_index_documents(self, documents: list[dict]) -> dict:
        """
        Index multiple documents in batch.
        
        Args:
            documents: List of dicts with 'doc_id' and 'filename'
        
        Returns:
            dict: Batch results (success_count, failed_count, errors)
        
        Example:
            >>> service = IndexingService()
            >>> docs = [
            ...     {'doc_id': 'doc1', 'filename': 'file1.txt'},
            ...     {'doc_id': 'doc2', 'filename': 'file2.txt'}
            ... ]
            >>> results = service.batch_index_documents(docs)
            >>> print(f"Indexed {results['success_count']} documents")
        """
        logger.info(f"Starting batch indexing", document_count=len(documents))
        
        success_count = 0
        failed_count = 0
        errors = []
        
        for doc in documents:
            doc_id = doc['doc_id']
            filename = doc['filename']
            
            try:
                self.index_document(doc_id, filename)
                success_count += 1
            except Exception as e:
                failed_count += 1
                error_msg = f"{filename}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Batch indexing failed for document", filename=filename, error=str(e))
        
        logger.info(
            f"Batch indexing completed",
            total=len(documents),
            success=success_count,
            failed=failed_count
        )
        
        return {
            'total': len(documents),
            'success_count': success_count,
            'failed_count': failed_count,
            'errors': errors
        }
    
    def get_indexing_stats(self) -> dict:
        """
        Get indexing statistics.
        
        Returns:
            dict: Statistics (total_chunks, indexed_docs, etc.)
        
        Example:
            >>> service = IndexingService()
            >>> stats = service.get_indexing_stats()
            >>> print(f"Total chunks: {stats['total_chunks']}")
        """
        # Get all documents
        all_docs = self.meta_repo.list_all_metadata()
        
        indexed_docs = [doc for doc in all_docs if doc.get('indexed', False)]
        pending_docs = [doc for doc in all_docs if not doc.get('indexed', False)]
        
        total_chunks = sum(doc.get('chunk_count', 0) for doc in indexed_docs)
        
        # Get vector store count
        vector_store_count = self.vector_store.count()
        
        return {
            'total_documents': len(all_docs),
            'indexed_documents': len(indexed_docs),
            'pending_documents': len(pending_docs),
            'total_chunks': total_chunks,
            'vector_store_count': vector_store_count,
            'embedding_dimension': self.embedding_service.get_embedding_dimension()
        }
    
    def is_document_indexed(self, doc_id: str) -> bool:
        """
        Check if document is indexed.
        
        Args:
            doc_id: Document ID
        
        Returns:
            bool: True if indexed
        
        Example:
            >>> service = IndexingService()
            >>> if not service.is_document_indexed("doc_123"):
            ...     service.index_document("doc_123", "file.txt")
        """
        metadata = self.meta_repo.get_metadata(doc_id)
        
        if not metadata:
            return False
        
        return metadata.get('indexed', False)
    
    def get_pending_documents(self) -> list[dict]:
        """
        Get list of documents pending indexing.
        
        Returns:
            list[dict]: Documents not yet indexed
        
        Example:
            >>> service = IndexingService()
            >>> pending = service.get_pending_documents()
            >>> for doc in pending:
            ...     print(f"Pending: {doc['filename']}")
        """
        all_docs = self.meta_repo.list_all_metadata()
        return [doc for doc in all_docs if not doc.get('indexed', False)]
    
    def clear_all_indexes(self) -> bool:
        """
        Clear all indexes from vector store.
        
        WARNING: This removes all chunks from the vector store.
        
        Returns:
            bool: True if cleared successfully
        
        Example:
            >>> service = IndexingService()
            >>> # Careful! This deletes everything
            >>> service.clear_all_indexes()
        """
        try:
            # Get all document IDs
            all_docs = self.meta_repo.list_all_metadata()
            
            for doc in all_docs:
                doc_id = doc['doc_id']
                self.remove_document_from_index(doc_id)
            
            logger.warning("All indexes cleared from vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear indexes", error=str(e))
            return False


# Singleton instance
_indexing_service_instance = None


def get_indexing_service() -> IndexingService:
    """
    Get singleton IndexingService instance.
    
    Returns:
        IndexingService: Singleton instance
    
    Example:
        >>> from src.services import get_indexing_service
        >>> indexing_service = get_indexing_service()
        >>> stats = indexing_service.get_indexing_stats()
    """
    global _indexing_service_instance
    
    if _indexing_service_instance is None:
        _indexing_service_instance = IndexingService()
        logger.debug("IndexingService singleton created")
    
    return _indexing_service_instance


# Convenience: Allow direct import
__all__ = [
    'IndexingService',
    'get_indexing_service',
]
