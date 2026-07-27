"""
Chat Service Module

This module provides business logic for chat operations.
Coordinates RAG pipeline and LLM invocation with fallback.

Author: TechFlow Solutions Project
License: MIT
"""

from typing import Optional, Generator

from src.rag import get_rag_pipeline
from src.llm import get_gemini_provider, get_cohere_provider
from src.storage import ConfigRepository
from src.utils import (
    get_logger,
    LLMError,
    EmptyKnowledgeLibraryError,
    RAGError
)


logger = get_logger()


class ChatService:
    """
    Service for chat operations with RAG and LLM.
    
    Features:
    - RAG-powered chat (query → retrieve → prompt → LLM)
    - Provider fallback (Gemini → Cohere)
    - Streaming responses
    - Conversation history management
    - Configuration-aware (temperature, top_k, etc.)
    
    Workflow:
    1. Get user query
    2. RAG pipeline retrieves relevant context
    3. Build prompt with context
    4. Invoke LLM (with fallback)
    5. Stream response to user
    """
    
    def __init__(self):
        """Initialize chat service."""
        self.rag_pipeline = get_rag_pipeline()
        self.gemini_provider = get_gemini_provider()
        self.cohere_provider = get_cohere_provider()
        self.config_repo = ConfigRepository()
        logger.debug("ChatService initialized")
    
    def chat(
        self,
        query: str,
        conversation_history: Optional[list[dict]] = None,
        stream: bool = True
    ) -> Generator[str, None, None] | str:
        """
        Execute RAG-powered chat query.
        
        Args:
            query: User query
            conversation_history: Previous messages (OpenAI format)
            stream: Whether to stream response
        
        Returns:
            Generator[str] if stream=True, str if stream=False
        
        Raises:
            EmptyKnowledgeLibraryError: If no documents indexed
            LLMError: If both providers fail
        
        Example:
            >>> service = ChatService()
            >>> # Streaming
            >>> for chunk in service.chat("What is RAG?", stream=True):
            ...     print(chunk, end='', flush=True)
            >>> # Non-streaming
            >>> response = service.chat("What is RAG?", stream=False)
            >>> print(response)
        """
        try:
            logger.info(f"Chat query started", query_length=len(query), stream=stream)
            
            # Get configuration
            config = self.config_repo.load_config()
            rag_config = config.get('rag', {})
            llm_config = config.get('llm', {})
            
            top_k = rag_config.get('top_k', 5)
            temperature = rag_config.get('temperature', 0.7)
            provider = llm_config.get('provider', 'gemini')
            
            # Execute RAG pipeline
            messages = self.rag_pipeline.query(
                user_query=query,
                top_k=top_k,
                conversation_history=conversation_history
            )
            
            logger.info(f"RAG pipeline completed", message_count=len(messages))
            
            # Invoke LLM with fallback
            if stream:
                return self._chat_streaming(messages, temperature, provider)
            else:
                return self._chat_non_streaming(messages, temperature, provider)
                
        except EmptyKnowledgeLibraryError:
            logger.warning("Chat attempted on empty knowledge library")
            raise
        except Exception as e:
            logger.error(f"Chat failed", query=query[:100], error=str(e), exc_info=True)
            raise LLMError(f"Chat failed: {e}")
    
    def _chat_streaming(
        self,
        messages: list[dict],
        temperature: float,
        provider: str
    ) -> Generator[str, None, None]:
        """
        Execute streaming chat with provider fallback.
        
        Args:
            messages: Messages for LLM
            temperature: LLM temperature
            provider: Primary provider ('gemini' or 'cohere')
        
        Yields:
            str: Response chunks
        """
        primary_provider = self.gemini_provider if provider == 'gemini' else self.cohere_provider
        fallback_provider = self.cohere_provider if provider == 'gemini' else self.gemini_provider
        primary_name = provider
        fallback_name = 'cohere' if provider == 'gemini' else 'gemini'
        
        # Try primary provider
        try:
            logger.info(f"Attempting streaming with primary provider", provider=primary_name)
            
            for chunk in primary_provider.chat_completion(
                messages=messages,
                temperature=temperature,
                stream=True
            ):
                yield chunk
            
            logger.info(f"Streaming completed", provider=primary_name)
            return
            
        except Exception as e:
            logger.warning(
                f"Primary provider failed, trying fallback",
                primary=primary_name,
                fallback=fallback_name,
                error=str(e)
            )
        
        # Try fallback provider
        try:
            logger.info(f"Attempting streaming with fallback provider", provider=fallback_name)
            
            for chunk in fallback_provider.chat_completion_stream(
                messages=messages,
                temperature=temperature
            ):
                yield chunk
            
            logger.info(f"Streaming completed with fallback", provider=fallback_name)
            return
            
        except Exception as e:
            logger.error(
                f"Both providers failed",
                primary=primary_name,
                fallback=fallback_name,
                error=str(e)
            )
            raise LLMError(f"All providers failed. Last error: {e}")
    
    def _chat_non_streaming(
        self,
        messages: list[dict],
        temperature: float,
        provider: str
    ) -> str:
        """
        Execute non-streaming chat with provider fallback.
        
        Args:
            messages: Messages for LLM
            temperature: LLM temperature
            provider: Primary provider
        
        Returns:
            str: Complete response
        """
        primary_provider = self.gemini_provider if provider == 'gemini' else self.cohere_provider
        fallback_provider = self.cohere_provider if provider == 'gemini' else self.gemini_provider
        primary_name = provider
        fallback_name = 'cohere' if provider == 'gemini' else 'gemini'
        
        # Try primary provider
        try:
            logger.info(f"Attempting chat with primary provider", provider=primary_name)
            
            response = primary_provider.chat_completion(
                messages=messages,
                temperature=temperature
            )
            
            logger.info(
                f"Chat completed",
                provider=primary_name,
                response_length=len(response)
            )
            
            return response
            
        except Exception as e:
            logger.warning(
                f"Primary provider failed, trying fallback",
                primary=primary_name,
                fallback=fallback_name,
                error=str(e)
            )
        
        # Try fallback provider
        try:
            logger.info(f"Attempting chat with fallback provider", provider=fallback_name)
            
            response = fallback_provider.chat_completion(
                messages=messages,
                temperature=temperature
            )
            
            logger.info(
                f"Chat completed with fallback",
                provider=fallback_name,
                response_length=len(response)
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Both providers failed",
                primary=primary_name,
                fallback=fallback_name,
                error=str(e)
            )
            raise LLMError(f"All providers failed. Last error: {e}")
    
    def chat_without_rag(
        self,
        query: str,
        conversation_history: Optional[list[dict]] = None,
        stream: bool = True
    ) -> Generator[str, None, None] | str:
        """
        Execute chat without RAG (direct LLM query).
        
        Useful for general questions not requiring knowledge library.
        
        Args:
            query: User query
            conversation_history: Previous messages
            stream: Whether to stream
        
        Returns:
            Generator[str] or str
        
        Example:
            >>> service = ChatService()
            >>> # Ask general question (no RAG)
            >>> for chunk in service.chat_without_rag("Hello!", stream=True):
            ...     print(chunk, end='')
        """
        try:
            logger.info(f"Chat without RAG", query_length=len(query))
            
            # Get configuration
            config = self.config_repo.load_config()
            llm_config = config.get('llm', {})
            rag_config = config.get('rag', {})
            
            temperature = rag_config.get('temperature', 0.7)
            provider = llm_config.get('provider', 'gemini')
            
            # Build simple messages (no RAG context)
            messages = []
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                'role': 'user',
                'content': query
            })
            
            # Invoke LLM
            if stream:
                return self._chat_streaming(messages, temperature, provider)
            else:
                return self._chat_non_streaming(messages, temperature, provider)
                
        except Exception as e:
            logger.error(f"Chat without RAG failed", error=str(e))
            raise LLMError(f"Chat failed: {e}")
    
    def test_provider(self, provider: str) -> dict:
        """
        Test LLM provider connectivity.
        
        Args:
            provider: Provider to test ('gemini' or 'cohere')
        
        Returns:
            dict: Test results (success, message, response_time)
        
        Example:
            >>> service = ChatService()
            >>> result = service.test_provider('gemini')
            >>> if result['success']:
            ...     print("Provider is working!")
        """
        import time
        
        test_messages = [
            {'role': 'user', 'content': 'Hello, respond with "OK"'}
        ]
        
        provider_obj = self.gemini_provider if provider == 'gemini' else self.cohere_provider
        
        try:
            start_time = time.time()
            
            response = provider_obj.chat_completion(
                messages=test_messages,
                temperature=0.0
            )
            
            elapsed = time.time() - start_time
            
            logger.info(f"Provider test successful", provider=provider, elapsed=elapsed)
            
            return {
                'success': True,
                'provider': provider,
                'message': 'Provider is working',
                'response': response,
                'response_time': elapsed
            }
            
        except Exception as e:
            logger.error(f"Provider test failed", provider=provider, error=str(e))
            
            return {
                'success': False,
                'provider': provider,
                'message': f'Provider test failed: {e}',
                'response': None,
                'response_time': None
            }
    
    def get_chat_stats(self) -> dict:
        """
        Get chat service statistics.
        
        Returns:
            dict: Statistics about chat service state
        
        Example:
            >>> service = ChatService()
            >>> stats = service.get_chat_stats()
            >>> print(f"RAG ready: {stats['rag_ready']}")
        """
        config = self.config_repo.load_config()
        rag_config = config.get('rag', {})
        llm_config = config.get('llm', {})
        
        return {
            'rag_ready': self.rag_pipeline.is_ready(),
            'vector_store_count': self.rag_pipeline.get_stats()['vector_store_count'],
            'primary_provider': llm_config.get('provider', 'gemini'),
            'temperature': rag_config.get('temperature', 0.7),
            'top_k': rag_config.get('top_k', 5),
            'chunk_size': rag_config.get('chunk_size', 512),
            'chunk_overlap': rag_config.get('chunk_overlap', 50)
        }


# Singleton instance
_chat_service_instance = None


def get_chat_service() -> ChatService:
    """
    Get singleton ChatService instance.
    
    Returns:
        ChatService: Singleton instance
    
    Example:
        >>> from src.services import get_chat_service
        >>> chat_service = get_chat_service()
        >>> for chunk in chat_service.chat("What is RAG?"):
        ...     print(chunk, end='')
    """
    global _chat_service_instance
    
    if _chat_service_instance is None:
        _chat_service_instance = ChatService()
        logger.debug("ChatService singleton created")
    
    return _chat_service_instance


# Convenience: Allow direct import
__all__ = [
    'ChatService',
    'get_chat_service',
]
