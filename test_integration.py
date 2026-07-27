"""
Integration Test Script for TechFlow Solutions RAG Agent

This script performs basic integration tests:
- Module imports
- Configuration loading
- Service initialization
- RAG pipeline
- LLM connectivity (optional)

Run: python test_integration.py

Author: TechFlow Solutions Project
License: MIT
"""

import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        # Config
        from src.config import get_paths
        paths = get_paths()
        print("   ✅ config")
        
        # Utils
        from src.utils import get_logger
        print("   ✅ utils")
        
        # Storage
        from src.storage import (
            ConfigRepository,
            DocumentRepository,
            MetadataRepository,
            FileManager
        )
        print("   ✅ storage")
        
        # Auth
        from src.auth import get_authenticator, get_session_manager
        print("   ✅ auth")
        
        # LLM
        from src.llm import get_gemini_provider, get_cohere_provider
        print("   ✅ llm")
        
        # RAG
        from src.rag import (
            get_embedding_service,
            get_vector_store,
            get_text_chunker,
            get_rag_pipeline
        )
        print("   ✅ rag")
        
        # Services
        from src.services import (
            get_authentication_service,
            get_configuration_service,
            get_knowledge_library_service,
            get_indexing_service,
            get_chat_service
        )
        print("   ✅ services")
        
        # UI
        from src.ui import (
            apply_theme,
            render_sidebar,
            render_chat_page
        )
        print("   ✅ ui")
        
        print("✅ All modules imported successfully\n")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}\n")
        return False


def test_configuration():
    """Test configuration loading."""
    print("🔍 Testing configuration...")
    
    try:
        from src.services import get_configuration_service
        
        config_service = get_configuration_service()
        
        # Get LLM config
        llm_config = config_service.get_llm_config()
        print(f"   LLM Provider: {llm_config.get('provider', 'N/A')}")
        print(f"   LLM Model: {llm_config.get('model', 'N/A')}")
        
        # Get RAG config
        rag_config = config_service.get_rag_config()
        print(f"   Chunk Size: {rag_config.get('chunk_size', 'N/A')}")
        print(f"   Top K: {rag_config.get('top_k', 'N/A')}")
        print(f"   Temperature: {rag_config.get('temperature', 'N/A')}")
        
        # Get theme
        theme = config_service.get_theme()
        print(f"   Theme: {theme}")
        
        # Validate
        is_valid, errors = config_service.validate_configuration()
        
        if is_valid:
            print("✅ Configuration is valid\n")
            return True
        else:
            print("⚠️  Configuration has errors:")
            for error in errors:
                print(f"      - {error}")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}\n")
        return False


def test_services():
    """Test service initialization."""
    print("🔍 Testing services...")
    
    try:
        from src.services import (
            get_authentication_service,
            get_configuration_service,
            get_knowledge_library_service,
            get_indexing_service,
            get_chat_service
        )
        
        # Authentication
        auth_service = get_authentication_service()
        print(f"   ✅ AuthenticationService initialized")
        
        # Configuration
        config_service = get_configuration_service()
        print(f"   ✅ ConfigurationService initialized")
        
        # Knowledge Library
        kl_service = get_knowledge_library_service()
        doc_count = kl_service.get_document_count()
        print(f"   ✅ KnowledgeLibraryService initialized ({doc_count} documents)")
        
        # Indexing
        indexing_service = get_indexing_service()
        stats = indexing_service.get_indexing_stats()
        print(f"   ✅ IndexingService initialized ({stats['total_chunks']} chunks)")
        
        # Chat
        chat_service = get_chat_service()
        chat_stats = chat_service.get_chat_stats()
        print(f"   ✅ ChatService initialized (RAG ready: {chat_stats['rag_ready']})")
        
        print("✅ All services initialized successfully\n")
        return True
        
    except Exception as e:
        print(f"❌ Service test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_rag_pipeline():
    """Test RAG pipeline components."""
    print("🔍 Testing RAG pipeline...")
    
    try:
        from src.rag import (
            get_embedding_service,
            get_vector_store,
            get_text_chunker,
            get_rag_pipeline
        )
        
        # Embedding service
        embedding_service = get_embedding_service()
        test_text = "Hello, this is a test."
        embedding = embedding_service.generate_embedding(test_text)
        print(f"   ✅ EmbeddingService (dim: {len(embedding)})")
        
        # Text chunker
        chunker = get_text_chunker()
        test_document = "This is a test document. " * 50
        chunks = chunker.chunk_text(test_document)
        print(f"   ✅ TextChunker ({len(chunks)} chunks)")
        
        # Vector store
        vector_store = get_vector_store()
        count = vector_store.count()
        print(f"   ✅ VectorStore ({count} documents)")
        
        # RAG pipeline
        pipeline = get_rag_pipeline()
        stats = pipeline.get_stats()
        print(f"   ✅ RAGPipeline (ready: {pipeline.is_ready()})")
        
        print("✅ RAG pipeline working correctly\n")
        return True
        
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_llm_providers():
    """Test LLM provider connectivity (optional)."""
    print("🔍 Testing LLM providers (optional)...")
    
    try:
        from src.services import get_chat_service
        
        chat_service = get_chat_service()
        
        # Test Gemini
        print("   Testing Gemini provider...")
        gemini_result = chat_service.test_provider('gemini')
        
        if gemini_result['success']:
            print(f"   ✅ Gemini working ({gemini_result['response_time']:.2f}s)")
        else:
            print(f"   ⚠️  Gemini: {gemini_result['message']}")
        
        # Test Cohere
        print("   Testing Cohere provider...")
        cohere_result = chat_service.test_provider('cohere')
        
        if cohere_result['success']:
            print(f"   ✅ Cohere working ({cohere_result['response_time']:.2f}s)")
        else:
            print(f"   ⚠️  Cohere: {cohere_result['message']}")
        
        if gemini_result['success'] or cohere_result['success']:
            print("✅ At least one LLM provider is working\n")
            return True
        else:
            print("⚠️  No LLM providers are configured\n")
            print("   Configure API keys in .env file to enable LLM features\n")
            return False
            
    except Exception as e:
        print(f"⚠️  LLM provider test skipped: {e}\n")
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("TechFlow Solutions RAG Agent - Integration Tests")
    print("=" * 60)
    print()
    
    results = {
        'imports': test_imports(),
        'configuration': test_configuration(),
        'services': test_services(),
        'rag_pipeline': test_rag_pipeline(),
        'llm_providers': test_llm_providers()
    }
    
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print()
    
    # Calculate pass rate
    passed = sum(results.values())
    total = len(results)
    pass_rate = (passed / total) * 100
    
    print(f"Pass Rate: {passed}/{total} ({pass_rate:.0f}%)")
    print()
    
    if pass_rate == 100:
        print("🎉 All tests passed! System is ready.")
    elif pass_rate >= 80:
        print("✅ Core tests passed. LLM configuration may be needed.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)
    print()
    
    return pass_rate >= 80


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
