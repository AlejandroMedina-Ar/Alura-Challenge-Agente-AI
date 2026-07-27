"""
Setup Script for TechFlow Solutions RAG Agent

This script initializes the project:
- Creates necessary directories
- Sets up configuration files
- Initializes database
- Validates environment

Run: python setup.py

Author: TechFlow Solutions Project
License: MIT
"""

import os
import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import get_paths
from src.storage import ConfigRepository
from src.auth import get_authenticator
from src.utils import get_logger, setup_logging


def main():
    """Run setup process."""
    print("=" * 60)
    print("TechFlow Solutions RAG Agent - Setup")
    print("=" * 60)
    print()
    
    # Setup logging
    setup_logging()
    logger = get_logger()
    
    logger.info("Starting setup process")
    
    try:
        # Step 1: Create directories
        print("📁 Creating directory structure...")
        create_directories()
        print("   ✅ Directories created\n")
        
        # Step 2: Initialize configuration
        print("⚙️  Initializing configuration...")
        initialize_configuration()
        print("   ✅ Configuration initialized\n")
        
        # Step 3: Validate environment
        print("🔍 Validating environment...")
        validate_environment()
        print("   ✅ Environment validated\n")
        
        # Step 4: Check authentication
        print("🔐 Checking authentication setup...")
        check_authentication()
        print("   ✅ Authentication configured\n")
        
        print("=" * 60)
        print("✅ Setup completed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Configure your API keys in .env file")
        print("2. Run the application: streamlit run src/app.py")
        print()
        
        logger.info("Setup completed successfully")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        logger.error(f"Setup failed", error=str(e), exc_info=True)
        sys.exit(1)


def create_directories():
    """Create necessary directories."""
    paths = get_paths()
    directories = [
        paths.DATA_DIR,
        paths.LOGS_DIR,
        paths.CHROMADB_DIR,
        paths.KNOWLEDGE_LIBRARY_DIR,
        paths.DOCUMENTS_DIR,
        paths.METADATA_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"   📂 {directory}")


def initialize_configuration():
    """Initialize configuration file."""
    config_repo = ConfigRepository()
    
    # Check if config exists
    if config_repo.config_file.exists():
        print(f"   ℹ️  Configuration file already exists")
        return
    
    # Create default configuration
    config_repo.reset_to_defaults()
    print(f"   ✅ Default configuration created")


def validate_environment():
    """Validate environment setup."""
    # Check Python version
    python_version = sys.version_info
    print(f"   Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        raise Exception("Python 3.9 or higher is required")
    
    # Check .env file
    env_file = PROJECT_ROOT / '.env'
    if not env_file.exists():
        print(f"   ⚠️  .env file not found (using defaults)")
        
        # Create from example
        env_example = PROJECT_ROOT / '.env.example'
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print(f"   ✅ Created .env from .env.example")
    else:
        print(f"   ✅ .env file exists")
    
    # Check required packages
    try:
        import streamlit
        print(f"   ✅ Streamlit: {streamlit.__version__}")
    except ImportError:
        raise Exception("Streamlit not installed. Run: pip install -r requirements.txt")
    
    try:
        import chromadb
        print(f"   ✅ ChromaDB installed")
    except ImportError:
        raise Exception("ChromaDB not installed. Run: pip install -r requirements.txt")


def check_authentication():
    """Check authentication setup."""
    authenticator = get_authenticator()
    
    if not authenticator.is_password_set():
        print(f"   ⚠️  Admin password not set")
        print(f"   ℹ️  Default password will be used")
        print(f"   ℹ️  Set ADMIN_PASSWORD in .env to change")
    else:
        print(f"   ✅ Admin password configured")


if __name__ == "__main__":
    main()
