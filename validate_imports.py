"""
Import Validation Script for TechFlow Solutions RAG Agent

This script validates ALL imports in the project before running setup.
It will catch any ImportError before the user tries to run the application.

Run: python validate_imports.py

Author: TechFlow Solutions Project
License: MIT
"""

import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Track results
errors = []
warnings = []
success_count = 0


def test_import(module_name, item_names=None, description=""):
    """Test importing a module or specific items from a module."""
    global errors, success_count
    
    try:
        if item_names:
            # Import specific items
            module = __import__(module_name, fromlist=item_names)
            for item in item_names:
                if not hasattr(module, item):
                    errors.append(f"❌ {module_name}.{item} does not exist")
                    return False
            success_count += 1
            return True
        else:
            # Import entire module
            __import__(module_name)
            success_count += 1
            return True
    except ImportError as e:
        errors.append(f"❌ {module_name}: {str(e)}")
        return False
    except Exception as e:
        errors.append(f"❌ {module_name}: Unexpected error - {str(e)}")
        return False


def validate_config_imports():
    """Validate config package imports."""
    print("🔍 Validating config package...")
    
    results = [
        test_import('src.config', ['get_settings', 'get_paths']),
        test_import('src.config', ['Settings', 'Paths']),
        test_import('src.config', ['APP_NAME', 'APP_VERSION']),
        test_import('src.config', ['FileFormat', 'LLMProvider', 'View', 'Theme']),
        test_import('src.config', ['get_file_format', 'format_file_size']),
    ]
    
    if all(results):
        print("   ✅ config package OK")
    return all(results)


def validate_utils_imports():
    """Validate utils package imports."""
    print("🔍 Validating utils package...")
    
    results = [
        test_import('src.utils', ['get_logger']),
        test_import('src.utils', ['TechFlowError', 'ConfigurationError', 'FileError']),
        test_import('src.utils', ['validate_file_size', 'validate_filename']),
        test_import('src.utils', ['hash_password', 'verify_password']),
        test_import('src.utils', ['sanitize_filename', 'format_timestamp']),
    ]
    
    if all(results):
        print("   ✅ utils package OK")
    return all(results)


def validate_storage_imports():
    """Validate storage package imports."""
    print("🔍 Validating storage package...")
    
    results = [
        test_import('src.storage', ['FileManager']),
        test_import('src.storage', ['DocumentRepository']),
        test_import('src.storage', ['MetadataRepository']),
        test_import('src.storage', ['ConfigRepository']),
    ]
    
    if all(results):
        print("   ✅ storage package OK")
    return all(results)


def validate_auth_imports():
    """Validate auth package imports."""
    print("🔍 Validating auth package...")
    
    results = [
        test_import('src.auth', ['get_authenticator']),
        test_import('src.auth', ['get_session_manager']),
        test_import('src.auth', ['Authenticator', 'SessionManager']),
    ]
    
    if all(results):
        print("   ✅ auth package OK")
    return all(results)


def validate_llm_imports():
    """Validate llm package imports."""
    print("🔍 Validating llm package...")
    
    results = [
        test_import('src.llm', ['BaseProvider']),
        test_import('src.llm', ['GeminiProvider']),
        test_import('src.llm', ['CohereProvider']),
    ]
    
    # Check for get_gemini_provider and get_cohere_provider
    try:
        from src.llm import GeminiProvider, CohereProvider
        # These should exist as classes, factory functions should be in services
        results.append(True)
    except ImportError as e:
        errors.append(f"❌ src.llm provider classes: {str(e)}")
        results.append(False)
    
    if all(results):
        print("   ✅ llm package OK")
    return all(results)


def validate_rag_imports():
    """Validate rag package imports."""
    print("🔍 Validating rag package...")
    
    results = [
        test_import('src.rag', ['get_embedding_service']),
        test_import('src.rag', ['get_vector_store']),
        test_import('src.rag', ['get_text_chunker']),
        test_import('src.rag', ['get_rag_pipeline']),
        test_import('src.rag', ['EmbeddingService', 'VectorStore', 'TextChunker']),
        test_import('src.rag', ['Retriever', 'PromptBuilder', 'RAGPipeline']),
    ]
    
    if all(results):
        print("   ✅ rag package OK")
    return all(results)


def validate_services_imports():
    """Validate services package imports."""
    print("🔍 Validating services package...")
    
    results = [
        test_import('src.services', ['get_authentication_service']),
        test_import('src.services', ['get_configuration_service']),
        test_import('src.services', ['get_knowledge_library_service']),
        test_import('src.services', ['get_indexing_service']),
        test_import('src.services', ['get_chat_service']),
    ]
    
    if all(results):
        print("   ✅ services package OK")
    return all(results)


def validate_ui_imports():
    """Validate ui package imports."""
    print("🔍 Validating ui package...")
    
    results = [
        test_import('src.ui', ['apply_theme', 'get_theme_icon']),
        test_import('src.ui', ['render_sidebar']),
        test_import('src.ui', ['render_chat_page']),
        test_import('src.ui', ['render_admin_panel']),
        test_import('src.ui', ['render_settings_panel']),
        test_import('src.ui', ['render_header', 'render_button']),
    ]
    
    if all(results):
        print("   ✅ ui package OK")
    return all(results)


def validate_main_scripts():
    """Validate imports in main scripts."""
    print("🔍 Validating main scripts...")
    
    # Check setup.py imports
    try:
        from src.config import get_paths
        from src.storage import ConfigRepository
        from src.auth import get_authenticator
        from src.utils import get_logger
        print("   ✅ setup.py imports OK")
        setup_ok = True
    except Exception as e:
        errors.append(f"❌ setup.py imports: {str(e)}")
        setup_ok = False
    
    # Check run.py imports
    try:
        from src.config import get_paths
        print("   ✅ run.py imports OK")
        run_ok = True
    except Exception as e:
        errors.append(f"❌ run.py imports: {str(e)}")
        run_ok = False
    
    # Check test_integration.py imports
    try:
        from src.config import get_paths
        from src.utils import get_logger
        from src.storage import ConfigRepository, DocumentRepository
        from src.auth import get_authenticator, get_session_manager
        from src.services import get_chat_service
        print("   ✅ test_integration.py imports OK")
        test_ok = True
    except Exception as e:
        errors.append(f"❌ test_integration.py imports: {str(e)}")
        test_ok = False
    
    return setup_ok and run_ok and test_ok


def check_llm_factory_functions():
    """Check if LLM factory functions exist."""
    print("🔍 Checking LLM factory functions...")
    
    try:
        from src.llm import get_gemini_provider, get_cohere_provider
        print("   ✅ LLM factory functions found in src.llm")
        return True
    except ImportError as e:
        errors.append(f"❌ LLM factory functions: {str(e)}")
        return False


def check_config_constants():
    """Check if required config constants are exported."""
    print("🔍 Checking config constants...")
    
    required_constants = [
        'DEFAULT_TOP_K',
        'DEFAULT_CHUNK_SIZE',
        'DEFAULT_CHUNK_OVERLAP',
        'DEFAULT_TEMPERATURE',
        'MIN_TOP_K',
        'MAX_TOP_K',
        'MIN_CHUNK_SIZE',
        'MAX_CHUNK_SIZE',
    ]
    
    try:
        from src.config import constants
        missing = []
        
        for const in required_constants:
            if not hasattr(constants, const):
                missing.append(const)
        
        if missing:
            errors.append(f"❌ Missing constants in src.config.constants: {', '.join(missing)}")
            return False
        
        # Now check if they're exported in __init__.py
        import src.config as config
        for const in required_constants:
            if not hasattr(config, const):
                errors.append(f"❌ Constant {const} not exported in src.config.__init__.py")
                return False
        
        print("   ✅ All required config constants present")
        return True
        
    except Exception as e:
        errors.append(f"❌ Config constants check: {str(e)}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 70)
    print("TechFlow Solutions - Import Validation")
    print("=" * 70)
    print()
    
    # Run all validations
    validations = [
        validate_config_imports(),
        validate_utils_imports(),
        validate_storage_imports(),
        validate_auth_imports(),
        validate_llm_imports(),
        validate_rag_imports(),
        validate_services_imports(),
        validate_ui_imports(),
        validate_main_scripts(),
        check_llm_factory_functions(),
        check_config_constants(),
    ]
    
    print()
    print("=" * 70)
    print("Validation Results")
    print("=" * 70)
    print()
    
    # Show errors
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"   {error}")
        print()
    
    # Show warnings
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    # Summary
    total_checks = len(validations)
    passed_checks = sum(validations)
    
    print(f"Checks Passed: {passed_checks}/{total_checks}")
    print(f"Success Count: {success_count}")
    print()
    
    if all(validations) and not errors:
        print("✅ ALL IMPORTS ARE VALID!")
        print()
        print("You can now safely run:")
        print("  1. python setup.py")
        print("  2. python test_integration.py")
        print("  3. python run.py")
        print()
        return True
    else:
        print("❌ VALIDATION FAILED!")
        print()
        print("Please fix the errors above before running setup.py")
        print()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
