"""
=============================================================
 TechFlow AI Project Bootstrap
=============================================================

Creates the complete project structure for the
TechFlow AI Corporate Knowledge Agent.

Features:
---------

✓ Safe to execute multiple times
✓ Never overwrites existing files
✓ Creates only missing directories
✓ Creates only missing files
✓ Generates __init__.py automatically
✓ Creates default config.json
✓ Creates .env.example
✓ Prints a detailed execution report

Author:
Oscar Alejandro Medina

Version: 1.0

=============================================================
"""

from pathlib import Path
import json
from datetime import datetime

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

PROJECT_ROOT = Path.cwd()

CREATED_DIRS = 0
CREATED_FILES = 0
SKIPPED = 0

# ------------------------------------------------------------
# Runtime files
# ------------------------------------------------------------

DEFAULT_CONFIG = {
    "theme": "tokyo-night",
    "llm_provider": "openrouter",
    "model": "",
    "temperature": 0.3,
    "top_k": 5,
    "max_tokens": 1500,
    "logging_level": "INFO"
}

DEFAULT_ENV = """# =====================================================
# TechFlow AI
# Environment Variables
# =====================================================

ADMIN_PASSWORD=

OPENROUTER_API_KEY=

OLLAMA_BASE_URL=http://localhost:11434

CHROMA_DB_PATH=data/chromadb

DEFAULT_PROVIDER=openrouter
"""

# ------------------------------------------------------------
# Console helpers
# ------------------------------------------------------------

def print_header():

    print("\n")
    print("=" * 60)
    print(" TechFlow AI Project Bootstrap")
    print("=" * 60)
    print()


def created(message):
    global CREATED_FILES
    CREATED_FILES += 1
    print(f"[CREATE] {message}")


def created_dir(message):
    global CREATED_DIRS
    CREATED_DIRS += 1
    print(f"[CREATE] {message}")


def skipped(message):
    global SKIPPED
    SKIPPED += 1
    print(f"[SKIP]   {message}")


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def create_directory(path: Path):

    if path.exists():
        skipped(f"Directory exists : {path}")
        return

    path.mkdir(parents=True, exist_ok=True)
    created_dir(f"Directory created : {path}")


def create_empty_file(path: Path):

    if path.exists():
        skipped(f"File exists      : {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    path.touch()

    created(f"File created     : {path}")


def create_file_with_content(path: Path, content: str):

    if path.exists():
        skipped(f"File exists      : {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content, encoding="utf-8")

    created(f"File created     : {path}")


def create_json(path: Path, data: dict):

    if path.exists():
        skipped(f"File exists      : {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    created(f"File created     : {path}")
    
    
# ------------------------------------------------------------
# Project Structure
# ------------------------------------------------------------

DIRECTORIES = [

    # --------------------------------------------------------
    # Source Code
    # --------------------------------------------------------

    "src",

    "src/ui",
    "src/services",
    "src/rag",
    "src/llm",
    "src/storage",
    "src/auth",
    "src/config",
    "src/utils",

    # --------------------------------------------------------
    # Runtime Data
    # --------------------------------------------------------

    "data",

    "data/knowledge_library",
    "data/knowledge_library/documents",
    "data/knowledge_library/metadata",

    "data/chromadb",

    "data/logs",

    # --------------------------------------------------------
    # Assets
    # --------------------------------------------------------

    "assets",

    "assets/css",
    "assets/icons",

    # --------------------------------------------------------
    # Documentation
    # --------------------------------------------------------

    "architecture",
    "specs",
    "prompts",
]

# ------------------------------------------------------------
# Python Packages
# ------------------------------------------------------------

PACKAGE_INIT_FILES = [

    "src/ui/__init__.py",
    "src/services/__init__.py",
    "src/rag/__init__.py",
    "src/llm/__init__.py",
    "src/storage/__init__.py",
    "src/auth/__init__.py",
    "src/config/__init__.py",
    "src/utils/__init__.py",

]

# ------------------------------------------------------------
# Source Files
# ------------------------------------------------------------

PYTHON_FILES = [

    # Entry Point

    "src/app.py",

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    "src/ui/chat.py",
    "src/ui/sidebar.py",
    "src/ui/admin_panel.py",
    "src/ui/settings_panel.py",
    "src/ui/theme.py",
    "src/ui/components.py",

    # --------------------------------------------------------
    # Services
    # --------------------------------------------------------

    "src/services/chat_service.py",
    "src/services/knowledge_base_service.py",
    "src/services/authentication_service.py",
    "src/services/configuration_service.py",
    "src/services/indexing_service.py",

    # --------------------------------------------------------
    # RAG
    # --------------------------------------------------------

    "src/rag/pipeline.py",
    "src/rag/retriever.py",
    "src/rag/chunker.py",
    "src/rag/embedding_service.py",
    "src/rag/prompt_builder.py",
    "src/rag/vector_store.py",

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    "src/llm/base_provider.py",
    "src/llm/openrouter_provider.py",
    "src/llm/ollama_provider.py",

    # --------------------------------------------------------
    # Storage
    # --------------------------------------------------------

    "src/storage/document_repository.py",
    "src/storage/metadata_repository.py",
    "src/storage/config_repository.py",
    "src/storage/file_manager.py",

    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------

    "src/auth/authentication.py",
    "src/auth/session.py",

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    "src/config/settings.py",
    "src/config/constants.py",
    "src/config/paths.py",

    # --------------------------------------------------------
    # Utilities
    # --------------------------------------------------------

    "src/utils/logger.py",
    "src/utils/helpers.py",
    "src/utils/validators.py",
    "src/utils/exceptions.py",

]

# ------------------------------------------------------------
# Root Files
# ------------------------------------------------------------

ROOT_FILES = [

    "README.md",
    "requirements.txt",
    ".gitignore",
    ".env.example",

]

# ------------------------------------------------------------
# Documentation Files
# ------------------------------------------------------------

DOCUMENTATION_FILES = [

    # Architecture

    "architecture/Architecture.md",
    "architecture/Source-Code-Structure.md",

    # Specifications

    "specs/000-project-overview.md",
    "specs/001-chat-interface.md",
    "specs/002-knowledge-base-management.md",
    "specs/003-authentication.md",
    "specs/004-rag-pipeline.md",
    "specs/005-configuration.md",
    "specs/006-deployment.md",

    # Prompts

    "prompts/system-prompt.md",
    "prompts/cursor-rules.md",

]

# ------------------------------------------------------------
# Asset Files
# ------------------------------------------------------------

ASSET_FILES = [

    "assets/css/dark.css",
    "assets/css/light.css",

]

# ------------------------------------------------------------
# Runtime Files
# ------------------------------------------------------------

CONFIG_JSON = "data/config.json"

LOG_FILE = "data/logs/application.log"

# ------------------------------------------------------------
# Bootstrap Functions
# ------------------------------------------------------------


def create_directories():

    print("\nCreating directories...\n")

    for directory in DIRECTORIES:
        create_directory(PROJECT_ROOT / directory)


# ------------------------------------------------------------

def create_package_files():

    print("\nCreating package files...\n")

    for file in PACKAGE_INIT_FILES:
        create_empty_file(PROJECT_ROOT / file)


# ------------------------------------------------------------

def create_python_files():

    print("\nCreating Python source files...\n")

    for file in PYTHON_FILES:
        create_empty_file(PROJECT_ROOT / file)


# ------------------------------------------------------------

def create_root_files():

    print("\nCreating root files...\n")

    for file in ROOT_FILES:

        path = PROJECT_ROOT / file

        if file == ".env.example":
            create_file_with_content(path, DEFAULT_ENV)
        else:
            create_empty_file(path)


# ------------------------------------------------------------

def create_documentation_files():

    print("\nCreating documentation files...\n")

    for file in DOCUMENTATION_FILES:
        create_empty_file(PROJECT_ROOT / file)


# ------------------------------------------------------------

def create_asset_files():

    print("\nCreating asset files...\n")

    for file in ASSET_FILES:
        create_empty_file(PROJECT_ROOT / file)


# ------------------------------------------------------------

def create_runtime_files():

    print("\nCreating runtime files...\n")

    create_json(
        PROJECT_ROOT / CONFIG_JSON,
        DEFAULT_CONFIG
    )

    create_empty_file(
        PROJECT_ROOT / LOG_FILE
    )


# ------------------------------------------------------------

def validate_structure():

    print("\nValidating project structure...\n")

    missing = []

    for directory in DIRECTORIES:

        path = PROJECT_ROOT / directory

        if not path.exists():
            missing.append(path)

    for file in PACKAGE_INIT_FILES:

        path = PROJECT_ROOT / file

        if not path.exists():
            missing.append(path)

    for file in PYTHON_FILES:

        path = PROJECT_ROOT / file

        if not path.exists():
            missing.append(path)

    for file in ROOT_FILES:

        path = PROJECT_ROOT / file

        if not path.exists():
            missing.append(path)

    for file in DOCUMENTATION_FILES:

        path = PROJECT_ROOT / file

        if not path.exists():
            missing.append(path)

    for file in ASSET_FILES:

        path = PROJECT_ROOT / file

        if not path.exists():
            missing.append(path)

    runtime_files = [

        PROJECT_ROOT / CONFIG_JSON,
        PROJECT_ROOT / LOG_FILE

    ]

    for file in runtime_files:

        if not file.exists():
            missing.append(file)

    if not missing:

        print("[OK] Project structure is complete.")

        return

    print("[WARNING] Missing items detected:\n")

    for item in missing:
        print(f" - {item}")


# ------------------------------------------------------------

def print_summary():

    print("\n")
    print("=" * 60)

    print(" Bootstrap Completed")

    print("=" * 60)

    print(f"Directories created : {CREATED_DIRS}")
    print(f"Files created       : {CREATED_FILES}")
    print(f"Skipped             : {SKIPPED}")

    print("=" * 60)

    print(
        "\nProject successfully synchronized with the expected "
        "structure."
    )

    print(
        "Existing files were preserved. "
        "No data was overwritten."
    )

    print()
    
    # ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    print_header()

    print("Project Root")
    print("------------------------------")
    print(PROJECT_ROOT)
    print()

    start_time = datetime.now()

    print("Starting project bootstrap...\n")

    # --------------------------------------------------------
    # Create directories
    # --------------------------------------------------------

    create_directories()

    # --------------------------------------------------------
    # Create package files (__init__.py)
    # --------------------------------------------------------

    create_package_files()

    # --------------------------------------------------------
    # Create Python source files
    # --------------------------------------------------------

    create_python_files()

    # --------------------------------------------------------
    # Create root files
    # --------------------------------------------------------

    create_root_files()

    # --------------------------------------------------------
    # Create documentation
    # --------------------------------------------------------

    create_documentation_files()

    # --------------------------------------------------------
    # Create assets
    # --------------------------------------------------------

    create_asset_files()

    # --------------------------------------------------------
    # Create runtime files
    # --------------------------------------------------------

    create_runtime_files()

    # --------------------------------------------------------
    # Validate project structure
    # --------------------------------------------------------

    validate_structure()

    end_time = datetime.now()

    elapsed = end_time - start_time

    print_summary()

    print(f"Execution time : {elapsed.total_seconds():.2f} seconds")
    print()

    print("Bootstrap finished successfully.")
    print()


# ------------------------------------------------------------
# End of File
# ------------------------------------------------------------

# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nBootstrap cancelled by user.")

    except Exception as error:

        print("\nAn unexpected error occurred.")
        print(error)