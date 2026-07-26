"""
Text Chunker Module

This module handles text chunking for RAG pipeline.
Uses recursive character splitting with overlap to preserve context.

Author: TechFlow AI Project
License: MIT
"""

from typing import Optional

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from src.config import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    MIN_CHUNK_SIZE,
    MAX_CHUNK_SIZE
)
from src.utils import (
    get_logger,
    ChunkingError,
    validate_chunk_parameters
)


logger = get_logger()


class TextChunker:
    """
    Text chunking service for RAG pipeline.
    
    Features:
    - Recursive character splitting
    - Configurable chunk size and overlap
    - Preserves context with overlap
    - Handles multiple languages
    - Smart splitting at sentence/paragraph boundaries
    
    Uses LangChain's RecursiveCharacterTextSplitter which tries to split at:
    1. Double newlines (paragraphs)
    2. Single newlines
    3. Spaces
    4. Characters (as last resort)
    """
    
    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    ):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        
        Raises:
            ChunkingError: If parameters are invalid
        
        Example:
            >>> chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
            >>> chunks = chunker.chunk_text("Long document text...")
            >>> print(len(chunks))
            5
        """
        # Validate parameters
        validate_chunk_parameters(chunk_size, chunk_overlap)
        
        if not LANGCHAIN_AVAILABLE:
            logger.error("langchain not available")
            raise ChunkingError("langchain package not installed")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Create text splitter
        try:
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]  # Try these in order
            )
            
            logger.info(
                f"TextChunker initialized",
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize text splitter", error=str(e))
            raise ChunkingError(f"Failed to initialize: {e}")
    
    def chunk_text(self, text: str) -> list[str]:
        """
        Split text into chunks.
        
        Args:
            text: Text to chunk
        
        Returns:
            list[str]: List of text chunks
        
        Raises:
            ChunkingError: If chunking fails
        
        Example:
            >>> chunker = TextChunker()
            >>> text = "Long document..." * 1000
            >>> chunks = chunker.chunk_text(text)
            >>> for i, chunk in enumerate(chunks):
            ...     print(f"Chunk {i+1}: {len(chunk)} chars")
        """
        if not text or not text.strip():
            logger.warning("Attempted to chunk empty text")
            return []
        
        try:
            chunks = self.splitter.split_text(text)
            
            logger.debug(
                f"Text chunked",
                original_length=len(text),
                num_chunks=len(chunks),
                avg_chunk_size=len(text) // len(chunks) if chunks else 0
            )
            
            return chunks
            
        except Exception as e:
            logger.error(
                f"Chunking failed",
                text_length=len(text),
                error=str(e),
                exc_info=True
            )
            raise ChunkingError(f"Failed to chunk text: {e}")
    
    def chunk_documents(
        self,
        documents: list[str],
        document_ids: Optional[list[str]] = None
    ) -> tuple[list[str], list[dict]]:
        """
        Chunk multiple documents with metadata tracking.
        
        Args:
            documents: List of document texts
            document_ids: Optional list of document IDs
        
        Returns:
            tuple: (chunks, metadatas)
                - chunks: List of all text chunks
                - metadatas: List of metadata dicts with source tracking
        
        Example:
            >>> chunker = TextChunker()
            >>> docs = ["Doc 1 text...", "Doc 2 text..."]
            >>> doc_ids = ["doc1.pdf", "doc2.pdf"]
            >>> chunks, metadatas = chunker.chunk_documents(docs, doc_ids)
            >>> print(len(chunks), len(metadatas))
            10 10
            >>> print(metadatas[0])
            {'source': 'doc1.pdf', 'chunk_index': 0}
        """
        if not documents:
            return [], []
        
        all_chunks = []
        all_metadatas = []
        
        for doc_idx, document in enumerate(documents):
            if not document or not document.strip():
                continue
            
            # Get document ID
            doc_id = document_ids[doc_idx] if document_ids else f"doc_{doc_idx}"
            
            # Chunk this document
            try:
                chunks = self.chunk_text(document)
                
                # Create metadata for each chunk
                for chunk_idx, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadatas.append({
                        'source': doc_id,
                        'chunk_index': chunk_idx,
                        'total_chunks': len(chunks)
                    })
                    
            except ChunkingError as e:
                logger.error(
                    f"Failed to chunk document",
                    doc_id=doc_id,
                    error=str(e)
                )
                continue
        
        logger.info(
            f"Chunked multiple documents",
            num_documents=len(documents),
            total_chunks=len(all_chunks)
        )
        
        return all_chunks, all_metadatas
    
    def get_chunk_count_estimate(self, text: str) -> int:
        """
        Estimate number of chunks without actually chunking.
        
        Args:
            text: Text to estimate
        
        Returns:
            int: Estimated chunk count
        
        Example:
            >>> chunker = TextChunker(chunk_size=1000)
            >>> text = "..." * 5000
            >>> estimate = chunker.get_chunk_count_estimate(text)
            >>> print(f"Estimated chunks: {estimate}")
            Estimated chunks: 5
        """
        if not text:
            return 0
        
        # Simple estimate: text length / (chunk_size - overlap)
        effective_chunk_size = self.chunk_size - self.chunk_overlap
        if effective_chunk_size <= 0:
            effective_chunk_size = self.chunk_size
        
        estimate = max(1, len(text) // effective_chunk_size)
        return estimate
    
    def update_chunk_size(self, chunk_size: int, chunk_overlap: Optional[int] = None) -> None:
        """
        Update chunking parameters.
        
        Args:
            chunk_size: New chunk size
            chunk_overlap: New overlap (optional, keeps current if not provided)
        
        Raises:
            ChunkingError: If parameters are invalid
        
        Example:
            >>> chunker = TextChunker()
            >>> chunker.update_chunk_size(2000, 400)
            >>> print(chunker.chunk_size)
            2000
        """
        if chunk_overlap is None:
            chunk_overlap = self.chunk_overlap
        
        # Validate new parameters
        validate_chunk_parameters(chunk_size, chunk_overlap)
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Recreate splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        logger.info(
            f"Chunk parameters updated",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )


# Singleton instance
_text_chunker_instance = None


def get_text_chunker(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> TextChunker:
    """
    Get singleton TextChunker instance.
    
    Args:
        chunk_size: Chunk size (only used on first call)
        chunk_overlap: Overlap size (only used on first call)
    
    Returns:
        TextChunker: Singleton instance
    
    Example:
        >>> from src.rag import get_text_chunker
        >>> chunker = get_text_chunker()
        >>> chunks = chunker.chunk_text("Long text...")
    """
    global _text_chunker_instance
    
    if _text_chunker_instance is None:
        _text_chunker_instance = TextChunker(chunk_size, chunk_overlap)
        logger.debug("TextChunker singleton created")
    
    return _text_chunker_instance


# Convenience: Allow direct import
__all__ = [
    'TextChunker',
    'get_text_chunker',
]
