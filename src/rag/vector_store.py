"""
Vector Store Module

This module provides a wrapper around ChromaDB for vector storage and retrieval.
Handles document embedding storage and similarity search.

Author: TechFlow AI Project
License: MIT
"""

from typing import Optional
import numpy as np

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from src.config import get_paths
from src.utils import (
    get_logger,
    VectorStoreError
)


logger = get_logger()


class VectorStore:
    """
    Vector store for document embeddings using ChromaDB.
    
    Features:
    - Persistent storage on disk
    - Similarity search (cosine distance)
    - Metadata storage
    - Collection management
    - Automatic persistence (ChromaDB v0.4.0+)
    
    ChromaDB is optimized for:
    - Fast similarity search
    - Metadata filtering
    - Local execution (no cloud required)
    """
    
    def __init__(
        self,
        collection_name: str = 'techflow_documents',
        persist_directory: Optional[str] = None
    ):
        """
        Initialize vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to store ChromaDB data
        
        Example:
            >>> store = VectorStore()
            >>> store.add_documents(
            ...     ids=['doc1'],
            ...     embeddings=[embedding],
            ...     documents=['Document text'],
            ...     metadatas=[{'source': 'file.pdf'}]
            ... )
        """
        if not CHROMADB_AVAILABLE:
            logger.error("chromadb not available")
            raise VectorStoreError("chromadb package not installed")
        
        self.collection_name = collection_name
        
        # Get persist directory from config if not provided
        if persist_directory is None:
            paths = get_paths()
            persist_directory = str(paths.CHROMADB_DIR)
        
        self.persist_directory = persist_directory
        
        try:
            # Initialize ChromaDB client with persistence
            logger.info(f"Initializing ChromaDB", path=persist_directory)
            
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # Use cosine distance
            )
            
            logger.info(
                f"Vector store initialized",
                collection=collection_name,
                count=self.collection.count()
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB", error=str(e), exc_info=True)
            raise VectorStoreError(f"Failed to initialize: {e}")
    
    def add_documents(
        self,
        ids: list[str],
        embeddings: list[np.ndarray],
        documents: list[str],
        metadatas: Optional[list[dict]] = None
    ) -> None:
        """
        Add documents to vector store.
        
        Args:
            ids: Unique IDs for each document
            embeddings: Embedding vectors
            documents: Original text content
            metadatas: Optional metadata dicts
        
        Raises:
            VectorStoreError: If addition fails
        
        Example:
            >>> store = VectorStore()
            >>> store.add_documents(
            ...     ids=['chunk_1', 'chunk_2'],
            ...     embeddings=[emb1, emb2],
            ...     documents=['Text 1', 'Text 2'],
            ...     metadatas=[{'page': 1}, {'page': 2}]
            ... )
        """
        if not ids or not embeddings or not documents:
            raise VectorStoreError("ids, embeddings, and documents are required")
        
        if len(ids) != len(embeddings) != len(documents):
            raise VectorStoreError("ids, embeddings, and documents must have same length")
        
        try:
            # Convert numpy arrays to lists for ChromaDB
            embeddings_list = [emb.tolist() if isinstance(emb, np.ndarray) else emb 
                              for emb in embeddings]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                documents=documents,
                metadatas=metadatas if metadatas else None
            )
            
            logger.info(
                f"Added documents to vector store",
                count=len(ids),
                collection=self.collection_name
            )
            
        except Exception as e:
            logger.error(
                f"Failed to add documents",
                count=len(ids),
                error=str(e),
                exc_info=True
            )
            raise VectorStoreError(f"Failed to add documents: {e}")
    
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        where: Optional[dict] = None
    ) -> dict:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            where: Optional metadata filter
        
        Returns:
            dict: Search results with ids, documents, metadatas, distances
        
        Example:
            >>> store = VectorStore()
            >>> results = store.search(query_embedding, top_k=5)
            >>> for doc, meta, dist in zip(
            ...     results['documents'][0],
            ...     results['metadatas'][0],
            ...     results['distances'][0]
            ... ):
            ...     print(f"{meta['source']}: {dist:.3f}")
        """
        try:
            # Convert numpy array to list
            query_list = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_list],
                n_results=min(top_k, self.collection.count()),
                where=where if where else None
            )
            
            logger.debug(
                f"Vector search completed",
                top_k=top_k,
                results_found=len(results['ids'][0]) if results['ids'] else 0
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed", error=str(e), exc_info=True)
            raise VectorStoreError(f"Search failed: {e}")
    
    def get_document(self, doc_id: str) -> Optional[dict]:
        """
        Get a document by ID.
        
        Args:
            doc_id: Document ID
        
        Returns:
            dict: Document data or None if not found
        
        Example:
            >>> store = VectorStore()
            >>> doc = store.get_document('chunk_1')
            >>> if doc:
            ...     print(doc['document'])
        """
        try:
            results = self.collection.get(
                ids=[doc_id],
                include=['documents', 'metadatas', 'embeddings']
            )
            
            if not results['ids']:
                return None
            
            return {
                'id': results['ids'][0],
                'document': results['documents'][0],
                'metadata': results['metadatas'][0] if results['metadatas'] else None,
                'embedding': results['embeddings'][0] if results['embeddings'] else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get document", doc_id=doc_id, error=str(e))
            return None
    
    def delete_documents(self, ids: list[str]) -> None:
        """
        Delete documents by IDs.
        
        Args:
            ids: List of document IDs to delete
        
        Example:
            >>> store = VectorStore()
            >>> store.delete_documents(['chunk_1', 'chunk_2'])
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted documents", count=len(ids))
        except Exception as e:
            logger.error(f"Failed to delete documents", error=str(e))
            raise VectorStoreError(f"Failed to delete: {e}")
    
    def delete_by_metadata(self, where: dict) -> None:
        """
        Delete documents by metadata filter.
        
        Args:
            where: Metadata filter dict
        
        Example:
            >>> store = VectorStore()
            >>> # Delete all chunks from a specific document
            >>> store.delete_by_metadata({'source': 'document.pdf'})
        """
        try:
            self.collection.delete(where=where)
            logger.info(f"Deleted documents by metadata", filter=where)
        except Exception as e:
            logger.error(f"Failed to delete by metadata", error=str(e))
            raise VectorStoreError(f"Failed to delete: {e}")
    
    def count(self) -> int:
        """
        Get number of documents in collection.
        
        Returns:
            int: Document count
        
        Example:
            >>> store = VectorStore()
            >>> count = store.count()
            >>> print(f"Vector store has {count} documents")
        """
        try:
            return self.collection.count()
        except Exception:
            return 0
    
    def clear(self) -> None:
        """
        Clear all documents from collection.
        
        **WARNING:** This is destructive and cannot be undone!
        
        Example:
            >>> store = VectorStore()
            >>> store.clear()
        """
        try:
            # Delete collection and recreate
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.warning(f"Cleared vector store", collection=self.collection_name)
        except Exception as e:
            logger.error(f"Failed to clear collection", error=str(e))
            raise VectorStoreError(f"Failed to clear: {e}")
    
    def list_collections(self) -> list[str]:
        """
        List all collections in the vector store.
        
        Returns:
            list[str]: Collection names
        
        Example:
            >>> store = VectorStore()
            >>> collections = store.list_collections()
            >>> print(collections)
            ['techflow_documents']
        """
        try:
            collections = self.client.list_collections()
            return [c.name for c in collections]
        except Exception as e:
            logger.error(f"Failed to list collections", error=str(e))
            return []
    
    def get_stats(self) -> dict:
        """
        Get statistics about the vector store.
        
        Returns:
            dict: Statistics (count, collection_name, persist_directory)
        
        Example:
            >>> store = VectorStore()
            >>> stats = store.get_stats()
            >>> print(stats)
            {
                'count': 42,
                'collection_name': 'techflow_documents',
                'persist_directory': '.../chromadb'
            }
        """
        return {
            'count': self.count(),
            'collection_name': self.collection_name,
            'persist_directory': self.persist_directory
        }


# Singleton instance
_vector_store_instance = None


def get_vector_store(
    collection_name: str = 'techflow_documents',
    persist_directory: Optional[str] = None
) -> VectorStore:
    """
    Get singleton VectorStore instance.
    
    Args:
        collection_name: Collection name (only used on first call)
        persist_directory: Persist directory (only used on first call)
    
    Returns:
        VectorStore: Singleton instance
    
    Example:
        >>> from src.rag import get_vector_store
        >>> store = get_vector_store()
        >>> count = store.count()
    """
    global _vector_store_instance
    
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore(collection_name, persist_directory)
        logger.debug("VectorStore singleton created")
    
    return _vector_store_instance


# Convenience: Allow direct import
__all__ = [
    'VectorStore',
    'get_vector_store',
]
