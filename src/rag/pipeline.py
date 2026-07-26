"""
RAG Pipeline Module

This module orchestrates the complete RAG workflow.
Coordinates embedding, retrieval, and prompt building.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional

from src.config import DEFAULT_TOP_K
from src.rag.embedding_service import get_embedding_service
from src.rag.vector_store import get_vector_store
from src.rag.retriever import Retriever
from src.rag.prompt_builder import PromptBuilder
from src.utils import (
    get_logger,
    RAGError,
    EmptyKnowledgeLibraryError
)


logger = get_logger()


class RAGPipeline:
    """
    Complete RAG pipeline orchestrator.
    
    Workflow:
    1. User submits query
    2. Generate query embedding
    3. Search vector store (similarity search)
    4. Retrieve top-k relevant chunks
    5. Build RAG prompt (query + context)
    6. Return prompt for LLM
    
    Note: LLM invocation is handled by chat_service, not by this pipeline.
    This allows conversation management and provider fallback logic.
    """
    
    def __init__(
        self,
        embedding_service=None,
        vector_store=None,
        top_k: int = DEFAULT_TOP_K,
        include_sources: bool = True
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            embedding_service: EmbeddingService instance (creates if None)
            vector_store: VectorStore instance (creates if None)
            top_k: Default number of chunks to retrieve
            include_sources: Include source citations in context
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> messages = pipeline.query("What is RAG?")
            >>> # messages ready for LLM
        """
        # Initialize components
        self.embedding_service = embedding_service or get_embedding_service()
        self.vector_store = vector_store or get_vector_store()
        self.retriever = Retriever(
            vector_store=self.vector_store,
            embedding_service=self.embedding_service,
            default_top_k=top_k
        )
        self.prompt_builder = PromptBuilder(include_sources=include_sources)
        
        logger.info(
            f"RAG Pipeline initialized",
            top_k=top_k,
            include_sources=include_sources,
            vector_store_count=self.vector_store.count()
        )
    
    def query(
        self,
        user_query: str,
        top_k: Optional[int] = None,
        conversation_history: Optional[list[dict]] = None,
        metadata_filter: Optional[dict] = None
    ) -> list[dict]:
        """
        Execute RAG pipeline for a user query.
        
        Args:
            user_query: User's question
            top_k: Number of chunks to retrieve (uses default if None)
            conversation_history: Previous conversation messages
            metadata_filter: Optional metadata filter for retrieval
        
        Returns:
            list[dict]: Messages ready for LLM (OpenAI format)
        
        Raises:
            EmptyKnowledgeLibraryError: If vector store is empty
            RAGError: If pipeline execution fails
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> messages = pipeline.query(
            ...     user_query="What is RAG?",
            ...     top_k=5
            ... )
            >>> # Pass messages to LLM provider
            >>> response = llm_provider.chat_completion(messages)
        """
        # Check if vector store has documents
        if self.vector_store.count() == 0:
            logger.warning("Query attempted on empty vector store")
            raise EmptyKnowledgeLibraryError(min_documents=1)
        
        try:
            logger.info(
                f"RAG query started",
                query_length=len(user_query),
                top_k=top_k or self.retriever.default_top_k
            )
            
            # Step 1: Retrieve relevant documents
            retrieved_docs = self.retriever.retrieve(
                query=user_query,
                top_k=top_k,
                where=metadata_filter
            )
            
            logger.info(
                f"Retrieved documents",
                num_docs=len(retrieved_docs),
                avg_score=sum(d['score'] for d in retrieved_docs) / len(retrieved_docs) if retrieved_docs else 0
            )
            
            # Step 2: Build prompt with retrieved context
            messages = self.prompt_builder.build_prompt(
                query=user_query,
                retrieved_documents=retrieved_docs,
                conversation_history=conversation_history
            )
            
            logger.info(
                f"RAG prompt built",
                num_messages=len(messages),
                estimated_tokens=self.prompt_builder.estimate_token_count(messages)
            )
            
            return messages
            
        except EmptyKnowledgeLibraryError:
            raise
        except Exception as e:
            logger.error(
                f"RAG pipeline failed",
                query=user_query[:100],
                error=str(e),
                exc_info=True
            )
            raise RAGError(f"RAG pipeline failed: {e}")
    
    def query_with_token_limit(
        self,
        user_query: str,
        max_context_tokens: int,
        conversation_history: Optional[list[dict]] = None
    ) -> list[dict]:
        """
        Execute RAG query with token budget constraint.
        
        Automatically truncates context to fit within token limit.
        
        Args:
            user_query: User's question
            max_context_tokens: Maximum tokens for retrieved context
            conversation_history: Previous conversation messages
        
        Returns:
            list[dict]: Messages ready for LLM
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> # Limit context to 2000 tokens
            >>> messages = pipeline.query_with_token_limit(
            ...     user_query="Explain RAG",
            ...     max_context_tokens=2000
            ... )
        """
        try:
            # Retrieve documents
            retrieved_docs = self.retriever.retrieve(user_query)
            
            # Truncate to fit budget
            truncated_docs = self.prompt_builder.truncate_context(
                retrieved_documents=retrieved_docs,
                max_context_tokens=max_context_tokens
            )
            
            # Build prompt with truncated context
            messages = self.prompt_builder.build_prompt(
                query=user_query,
                retrieved_documents=truncated_docs,
                conversation_history=conversation_history
            )
            
            logger.info(
                f"RAG query with token limit",
                max_tokens=max_context_tokens,
                docs_used=len(truncated_docs),
                docs_total=len(retrieved_docs)
            )
            
            return messages
            
        except Exception as e:
            logger.error(f"RAG query with token limit failed", error=str(e))
            raise RAGError(f"Failed: {e}")
    
    def get_relevant_chunks(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> list[dict]:
        """
        Get relevant document chunks without building full prompt.
        
        Useful for debugging or previewing retrieval results.
        
        Args:
            query: Search query
            top_k: Number of chunks to retrieve
        
        Returns:
            list[dict]: Retrieved documents with text, metadata, score
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> chunks = pipeline.get_relevant_chunks("query", top_k=3)
            >>> for chunk in chunks:
            ...     print(f"Score: {chunk['score']:.3f}")
            ...     print(f"Source: {chunk['metadata']['source']}")
            ...     print(f"Text: {chunk['text'][:100]}...")
        """
        return self.retriever.retrieve(query, top_k)
    
    def update_top_k(self, new_top_k: int) -> None:
        """
        Update default top_k for retrieval.
        
        Args:
            new_top_k: New default top_k value
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> pipeline.update_top_k(10)
        """
        self.retriever.update_top_k(new_top_k)
        logger.info(f"Pipeline top_k updated", new_value=new_top_k)
    
    def update_system_instruction(self, instruction: str) -> None:
        """
        Update system instruction for prompts.
        
        Args:
            instruction: New system instruction text
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> pipeline.update_system_instruction("Custom instruction...")
        """
        self.prompt_builder.update_system_instruction(instruction)
        logger.info("Pipeline system instruction updated")
    
    def get_stats(self) -> dict:
        """
        Get pipeline statistics.
        
        Returns:
            dict: Statistics about pipeline state
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> stats = pipeline.get_stats()
            >>> print(stats)
            {
                'vector_store_count': 42,
                'embedding_dimension': 768,
                'default_top_k': 5,
                'include_sources': True
            }
        """
        return {
            'vector_store_count': self.vector_store.count(),
            'embedding_dimension': self.embedding_service.get_embedding_dimension(),
            'default_top_k': self.retriever.default_top_k,
            'include_sources': self.prompt_builder.include_sources
        }
    
    def is_ready(self) -> bool:
        """
        Check if pipeline is ready for queries.
        
        Returns:
            bool: True if vector store has documents
        
        Example:
            >>> pipeline = RAGPipeline()
            >>> if pipeline.is_ready():
            ...     messages = pipeline.query("question")
            ... else:
            ...     print("Please index documents first")
        """
        return self.vector_store.count() > 0


# Singleton instance
_rag_pipeline_instance = None


def get_rag_pipeline(
    top_k: int = DEFAULT_TOP_K,
    include_sources: bool = True
) -> RAGPipeline:
    """
    Get singleton RAGPipeline instance.
    
    Args:
        top_k: Default top_k (only used on first call)
        include_sources: Include sources (only used on first call)
    
    Returns:
        RAGPipeline: Singleton instance
    
    Example:
        >>> from src.rag import get_rag_pipeline
        >>> pipeline = get_rag_pipeline()
        >>> messages = pipeline.query("What is RAG?")
    """
    global _rag_pipeline_instance
    
    if _rag_pipeline_instance is None:
        _rag_pipeline_instance = RAGPipeline(
            top_k=top_k,
            include_sources=include_sources
        )
        logger.debug("RAGPipeline singleton created")
    
    return _rag_pipeline_instance


# Convenience: Allow direct import
__all__ = [
    'RAGPipeline',
    'get_rag_pipeline',
]
