"""
Services Package

This package provides business logic services that orchestrate
lower-level modules (auth, storage, rag, llm).

Modules:
- authentication_service: Login, logout, session management
- configuration_service: Runtime configuration (LLM, RAG, UI)
- knowledge_library_service: Document upload, delete, list
- indexing_service: Document chunking, embedding, vector store
- chat_service: RAG pipeline + LLM invocation with fallback

Author: TechFlow AI Project
License: MIT
"""

from .authentication_service import (
    AuthenticationService,
    get_authentication_service
)

from .configuration_service import (
    ConfigurationService,
    get_configuration_service
)

from .knowledge_library_service import (
    KnowledgeLibraryService,
    get_knowledge_library_service
)

from .indexing_service import (
    IndexingService,
    get_indexing_service
)

from .chat_service import (
    ChatService,
    get_chat_service
)


__all__ = [
    # Classes
    'AuthenticationService',
    'ConfigurationService',
    'KnowledgeLibraryService',
    'IndexingService',
    'ChatService',
    
    # Singletons
    'get_authentication_service',
    'get_configuration_service',
    'get_knowledge_library_service',
    'get_indexing_service',
    'get_chat_service',
]
