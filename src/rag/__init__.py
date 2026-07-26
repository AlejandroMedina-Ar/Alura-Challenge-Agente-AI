"""
RAG Package

This package implements the complete RAG (Retrieval-Augmented Generation) pipeline.

Modules:
- embedding_service: Text embedding generation
- vector_store: Vector storage and similarity search (ChromaDB)
- chunker: Text chunking with overlap
- retriever: Document retrieval from vector store
- prompt_builder: RAG prompt construction
- pipeline: Complete RAG workflow orchestration

Author: TechFlow Solutions Project
License: MIT
"""

from .embedding_service import (
    EmbeddingService,
    get_embedding_service
)

from .vector_store import (
    VectorStore,
    get_vector_store
)

from .chunker import (
    TextChunker,
    get_text_chunker
)

from .retriever import Retriever

from .prompt_builder import PromptBuilder

from .pipeline import (
    RAGPipeline,
    get_rag_pipeline
)


__all__ = [
    # Classes
    'EmbeddingService',
    'VectorStore',
    'TextChunker',
    'Retriever',
    'PromptBuilder',
    'RAGPipeline',
    
    # Singletons
    'get_embedding_service',
    'get_vector_store',
    'get_text_chunker',
    'get_rag_pipeline',
]
