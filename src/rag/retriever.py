"""
Retriever Module

This module handles document retrieval from the vector store.
Performs similarity search to find relevant context for queries.

Author: TechFlow AI Project
License: MIT
"""

from typing import Optional
import numpy as np

from src.config import DEFAULT_TOP_K, MIN_TOP_K, MAX_TOP_K
from src.utils import (
    get_logger,
    RetrievalError,
    validate_top_k
)


logger = get_logger()


class Retriever:
    """
    Document retriever for RAG pipeline.
    
    Features:
    - Top-k similarity search
    - Metadata filtering
    - Score thresholding
    - Result formatting
    
    Uses vector store for similarity search and returns
    the most relevant document chunks for a query.
    """
    
    def __init__(
        self,
        vector_store,
        embedding_service,
        default_top_k: int = DEFAULT_TOP_K
    ):
        """
        Initialize retriever.
        
        Args:
            vector_store: VectorStore instance
            embedding_service: EmbeddingService instance
            default_top_k: Default number of results to return
        
        Example:
            >>> from src.rag import get_vector_store, get_embedding_service
            >>> store = get_vector_store()
            >>> embedder = get_embedding_service()
            >>> retriever = Retriever(store, embedder)
        """
        validate_top_k(default_top_k)
        
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.default_top_k = default_top_k
        
        logger.info(
            f"Retriever initialized",
            default_top_k=default_top_k
        )
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        where: Optional[dict] = None,
        score_threshold: Optional[float] = None
    ) -> list[dict]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query text
            top_k: Number of results to return (uses default if None)
            where: Metadata filter (e.g., {'source': 'doc.pdf'})
            score_threshold: Minimum similarity score (0-1, lower is more similar)
        
        Returns:
            list[dict]: List of retrieved documents with metadata
                Each dict contains: text, metadata, score, id
        
        Raises:
            RetrievalError: If retrieval fails
        
        Example:
            >>> retriever = Retriever(store, embedder)
            >>> results = retriever.retrieve("What is RAG?", top_k=5)
            >>> for result in results:
            ...     print(f"Score: {result['score']:.3f}")
            ...     print(f"Text: {result['text'][:100]}...")
            ...     print(f"Source: {result['metadata']['source']}")
        """
        if not query or not query.strip():
            raise RetrievalError("Query cannot be empty")
        
        # Use default top_k if not provided
        if top_k is None:
            top_k = self.default_top_k
        
        # Validate top_k
        validate_top_k(top_k)
        
        try:
            # Generate query embedding
            logger.debug(f"Generating query embedding", query_length=len(query))
            query_embedding = self.embedding_service.generate_query_embedding(query)
            
            # Search vector store
            logger.debug(f"Searching vector store", top_k=top_k, has_filter=bool(where))
            results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                where=where
            )
            
            # Format results
            formatted_results = self._format_results(results, score_threshold)
            
            logger.info(
                f"Retrieved documents",
                query_length=len(query),
                results_found=len(formatted_results),
                top_k=top_k
            )
            
            return formatted_results
            
        except Exception as e:
            logger.error(
                f"Retrieval failed",
                query=query[:100],
                error=str(e),
                exc_info=True
            )
            raise RetrievalError(f"Failed to retrieve documents: {e}")
    
    def _format_results(
        self,
        raw_results: dict,
        score_threshold: Optional[float] = None
    ) -> list[dict]:
        """
        Format raw vector store results into structured list.
        
        Args:
            raw_results: Raw results from vector store
            score_threshold: Optional score threshold for filtering
        
        Returns:
            list[dict]: Formatted results
        """
        if not raw_results or not raw_results.get('ids'):
            return []
        
        formatted = []
        
        # ChromaDB returns results as nested lists (batch format)
        ids = raw_results['ids'][0] if raw_results['ids'] else []
        documents = raw_results['documents'][0] if raw_results['documents'] else []
        metadatas = raw_results['metadatas'][0] if raw_results['metadatas'] else []
        distances = raw_results['distances'][0] if raw_results['distances'] else []
        
        for i in range(len(ids)):
            score = distances[i] if i < len(distances) else 1.0
            
            # Apply score threshold if provided
            if score_threshold is not None and score > score_threshold:
                continue
            
            formatted.append({
                'id': ids[i],
                'text': documents[i] if i < len(documents) else '',
                'metadata': metadatas[i] if i < len(metadatas) else {},
                'score': score  # Lower is better (distance)
            })
        
        return formatted
    
    def retrieve_by_embedding(
        self,
        query_embedding: np.ndarray,
        top_k: Optional[int] = None,
        where: Optional[dict] = None
    ) -> list[dict]:
        """
        Retrieve documents using pre-computed embedding.
        
        Useful when you already have the embedding and want to avoid
        re-computing it.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            where: Metadata filter
        
        Returns:
            list[dict]: Retrieved documents
        
        Example:
            >>> retriever = Retriever(store, embedder)
            >>> embedding = embedder.generate_embedding("query")
            >>> results = retriever.retrieve_by_embedding(embedding, top_k=3)
        """
        if top_k is None:
            top_k = self.default_top_k
        
        validate_top_k(top_k)
        
        try:
            results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                where=where
            )
            
            formatted_results = self._format_results(results)
            
            logger.debug(
                f"Retrieved by embedding",
                results_found=len(formatted_results)
            )
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Retrieval by embedding failed", error=str(e))
            raise RetrievalError(f"Failed to retrieve: {e}")
    
    def retrieve_with_scores(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> list[tuple[str, float]]:
        """
        Retrieve documents with simplified (text, score) format.
        
        Args:
            query: Search query
            top_k: Number of results
        
        Returns:
            list[tuple]: List of (text, score) tuples
        
        Example:
            >>> retriever = Retriever(store, embedder)
            >>> results = retriever.retrieve_with_scores("query", top_k=3)
            >>> for text, score in results:
            ...     print(f"{score:.3f}: {text[:50]}...")
        """
        full_results = self.retrieve(query, top_k)
        return [(r['text'], r['score']) for r in full_results]
    
    def retrieve_texts_only(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> list[str]:
        """
        Retrieve only the text content of documents.
        
        Args:
            query: Search query
            top_k: Number of results
        
        Returns:
            list[str]: List of document texts
        
        Example:
            >>> retriever = Retriever(store, embedder)
            >>> texts = retriever.retrieve_texts_only("query", top_k=5)
            >>> for text in texts:
            ...     print(text[:100])
        """
        full_results = self.retrieve(query, top_k)
        return [r['text'] for r in full_results]
    
    def get_context_window(
        self,
        query: str,
        max_tokens: int,
        tokens_per_char: float = 0.25
    ) -> list[dict]:
        """
        Retrieve documents that fit within a token budget.
        
        Dynamically adjusts top_k to fit within max_tokens.
        
        Args:
            query: Search query
            max_tokens: Maximum tokens allowed
            tokens_per_char: Approximate tokens per character
        
        Returns:
            list[dict]: Retrieved documents that fit in budget
        
        Example:
            >>> retriever = Retriever(store, embedder)
            >>> # Get documents that fit in 2000 tokens
            >>> results = retriever.get_context_window("query", max_tokens=2000)
            >>> total_chars = sum(len(r['text']) for r in results)
            >>> print(f"Estimated tokens: {total_chars * 0.25:.0f}")
        """
        # Start with default top_k
        results = self.retrieve(query, top_k=self.default_top_k)
        
        # Calculate total characters
        total_chars = 0
        fitting_results = []
        
        for result in results:
            text_chars = len(result['text'])
            estimated_tokens = text_chars * tokens_per_char
            
            if total_chars + estimated_tokens <= max_tokens:
                fitting_results.append(result)
                total_chars += estimated_tokens
            else:
                # Stop adding more results
                break
        
        logger.debug(
            f"Context window created",
            max_tokens=max_tokens,
            results_included=len(fitting_results),
            estimated_tokens=int(total_chars)
        )
        
        return fitting_results
    
    def update_top_k(self, new_top_k: int) -> None:
        """
        Update default top_k value.
        
        Args:
            new_top_k: New default top_k
        
        Example:
            >>> retriever = Retriever(store, embedder)
            >>> retriever.update_top_k(10)
        """
        validate_top_k(new_top_k)
        self.default_top_k = new_top_k
        logger.info(f"Updated default top_k", new_value=new_top_k)


# Convenience: Allow direct import
__all__ = [
    'Retriever',
]
