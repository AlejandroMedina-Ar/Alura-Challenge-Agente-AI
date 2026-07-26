"""
Embedding Service Module

This module handles text embedding generation using sentence-transformers.
Uses multilingual-e5-base model optimized for Spanish and 100+ languages.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from src.utils import (
    get_logger,
    EmbeddingError
)


logger = get_logger()


class EmbeddingService:
    """
    Service for generating text embeddings.
    
    Features:
    - Multilingual embeddings (100+ languages)
    - Optimized for Spanish
    - Local execution (no API calls)
    - Batch processing support
    - Vector dimension: 768
    
    Model: intfloat/multilingual-e5-base
    - Performance: ~50% better than English-only models for Spanish
    - Context: Up to 512 tokens
    - Free to use locally
    """
    
    def __init__(
        self,
        model_name: str = 'intfloat/multilingual-e5-base',
        device: Optional[str] = None
    ):
        """
        Initialize embedding service.
        
        Args:
            model_name: Name of the sentence-transformers model
            device: Device to use ('cpu', 'cuda', or None for auto)
        
        Example:
            >>> service = EmbeddingService()
            >>> embedding = service.generate_embedding("Hello world")
            >>> print(embedding.shape)
            (768,)
        """
        self.model_name = model_name
        self.device = device
        self.model = None
        
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.error("sentence-transformers not available")
            raise EmbeddingError(
                "sentence-transformers",
                "sentence-transformers package not installed"
            )
        
        try:
            logger.info(f"Loading embedding model", model=model_name)
            self.model = SentenceTransformer(model_name, device=device)
            logger.info(
                f"Embedding model loaded successfully",
                model=model_name,
                dimension=self.get_embedding_dimension()
            )
        except Exception as e:
            logger.error(f"Failed to load embedding model", error=str(e), exc_info=True)
            raise EmbeddingError(model_name, f"Failed to load model: {e}")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
        
        Returns:
            np.ndarray: Embedding vector (768 dimensions)
        
        Raises:
            EmbeddingError: If embedding generation fails
        
        Example:
            >>> service = EmbeddingService()
            >>> embedding = service.generate_embedding("¿Qué es RAG?")
            >>> print(type(embedding), embedding.shape)
            <class 'numpy.ndarray'> (768,)
        """
        if not text or not text.strip():
            raise EmbeddingError("text", "Cannot generate embedding for empty text")
        
        try:
            # E5 models require "query: " or "passage: " prefix for best performance
            # For queries, use "query: " prefix
            prefixed_text = f"query: {text}"
            
            embedding = self.model.encode(prefixed_text, convert_to_numpy=True)
            
            logger.debug(
                f"Generated embedding",
                text_length=len(text),
                embedding_dim=len(embedding)
            )
            
            return embedding
            
        except Exception as e:
            logger.error(
                f"Failed to generate embedding",
                text_preview=text[:100],
                error=str(e),
                exc_info=True
            )
            raise EmbeddingError(text[:50], str(e))
    
    def generate_embeddings_batch(
        self,
        texts: list[str],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> list[np.ndarray]:
        """
        Generate embeddings for multiple texts (batch processing).
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process at once
            show_progress: Show progress bar
        
        Returns:
            list[np.ndarray]: List of embedding vectors
        
        Raises:
            EmbeddingError: If batch embedding generation fails
        
        Example:
            >>> service = EmbeddingService()
            >>> texts = ["First text", "Second text", "Third text"]
            >>> embeddings = service.generate_embeddings_batch(texts)
            >>> print(len(embeddings))
            3
        """
        if not texts:
            return []
        
        # Filter out empty texts
        non_empty_texts = [t for t in texts if t and t.strip()]
        
        if not non_empty_texts:
            raise EmbeddingError("texts", "All texts are empty")
        
        try:
            # Add "passage: " prefix for document chunks
            prefixed_texts = [f"passage: {text}" for text in non_empty_texts]
            
            embeddings = self.model.encode(
                prefixed_texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            
            logger.info(
                f"Generated batch embeddings",
                num_texts=len(non_empty_texts),
                batch_size=batch_size
            )
            
            return list(embeddings)
            
        except Exception as e:
            logger.error(
                f"Failed to generate batch embeddings",
                num_texts=len(texts),
                error=str(e),
                exc_info=True
            )
            raise EmbeddingError(f"{len(texts)} texts", str(e))
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a search query.
        
        This is an alias for generate_embedding with explicit naming
        for clarity in RAG pipeline.
        
        Args:
            query: Search query text
        
        Returns:
            np.ndarray: Query embedding vector
        
        Example:
            >>> service = EmbeddingService()
            >>> query_embedding = service.generate_query_embedding("What is RAG?")
        """
        return self.generate_embedding(query)
    
    def generate_document_embeddings(
        self,
        documents: list[str],
        batch_size: int = 32
    ) -> list[np.ndarray]:
        """
        Generate embeddings for document chunks.
        
        This is an alias for generate_embeddings_batch with explicit naming
        for clarity in RAG pipeline.
        
        Args:
            documents: List of document chunks
            batch_size: Batch size for processing
        
        Returns:
            list[np.ndarray]: List of document embeddings
        
        Example:
            >>> service = EmbeddingService()
            >>> chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
            >>> embeddings = service.generate_document_embeddings(chunks)
        """
        return self.generate_embeddings_batch(documents, batch_size=batch_size)
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model.
        
        Returns:
            int: Embedding dimension (768 for multilingual-e5-base)
        
        Example:
            >>> service = EmbeddingService()
            >>> dim = service.get_embedding_dimension()
            >>> print(dim)
            768
        """
        if self.model is None:
            return 768  # Default for multilingual-e5-base
        
        try:
            # Get dimension from model
            return self.model.get_sentence_embedding_dimension()
        except Exception:
            return 768  # Fallback
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
        
        Returns:
            float: Cosine similarity (0 to 1)
        
        Example:
            >>> service = EmbeddingService()
            >>> emb1 = service.generate_embedding("Hello")
            >>> emb2 = service.generate_embedding("Hi")
            >>> similarity = service.similarity(emb1, emb2)
            >>> print(f"Similarity: {similarity:.2f}")
            Similarity: 0.85
        """
        from numpy.linalg import norm
        
        # Cosine similarity
        cos_sim = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
        return float(cos_sim)


# Singleton instance
_embedding_service_instance = None


def get_embedding_service(
    model_name: str = 'intfloat/multilingual-e5-base',
    device: Optional[str] = None
) -> EmbeddingService:
    """
    Get singleton EmbeddingService instance.
    
    Args:
        model_name: Model name (only used on first call)
        device: Device to use (only used on first call)
    
    Returns:
        EmbeddingService: Singleton instance
    
    Example:
        >>> from src.rag import get_embedding_service
        >>> service = get_embedding_service()
        >>> embedding = service.generate_embedding("Hello world")
    """
    global _embedding_service_instance
    
    if _embedding_service_instance is None:
        _embedding_service_instance = EmbeddingService(model_name, device)
        logger.debug("EmbeddingService singleton created")
    
    return _embedding_service_instance


# Convenience: Allow direct import
__all__ = [
    'EmbeddingService',
    'get_embedding_service',
]
