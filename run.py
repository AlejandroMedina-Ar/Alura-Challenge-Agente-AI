"""
Quick Start Script for TechFlow Solutions RAG Agent

This script provides a quick way to start the application.
Performs basic checks before launching Streamlit.

Run: python run.py

Author: TechFlow Solutions Project
License: MIT
"""

import sys
import subprocess
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_requirements():
    """Check if basic requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        return False
    
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check Streamlit
    try:
        import streamlit
        print(f"   ✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("   ❌ Streamlit not installed")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Check if setup was run
    from src.config import DATA_DIR
    
    if not DATA_DIR.exists():
        print("   ⚠️  Data directory not found")
        print("   Run: python setup.py")
        return False
    
    print("   ✅ Data directory exists")
    
    return True


def run_streamlit():
    """Launch Streamlit application."""
    print("\n🚀 Starting TechFlow Solutions RAG Agent...")
    print("=" * 60)
    print()
    
    app_path = PROJECT_ROOT / "src" / "app.py"
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped")
        print("=" * 60)


def main():
    """Main entry point."""
    print("=" * 60)
    print("TechFlow Solutions RAG Agent - Quick Start")
    print("=" * 60)
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed")
        print("Please fix the issues above before running the application")
        sys.exit(1)
    
    # Run Streamlit
    run_streamlit()


if __name__ == "__main__":
    main()
