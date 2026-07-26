"""
Path Configuration Module

This module defines all file system paths used by the application.
Paths are resolved relative to the project root and created automatically if needed.

Author: TechFlow AI Project
License: MIT
"""

from pathlib import Path
from typing import Optional


class PathConfigurationError(Exception):
    """Raised when path configuration fails."""
    pass


class Paths:
    """
    Application paths configuration.
    
    All paths are resolved as absolute paths relative to the project root.
    Directories are created automatically on initialization.
    
    Attributes:
        PROJECT_ROOT: Root directory of the project
        SRC_DIR: Source code directory
        DATA_DIR: Data storage directory
        KNOWLEDGE_LIBRARY_DIR: Knowledge library root
        DOCUMENTS_DIR: Uploaded documents storage
        METADATA_DIR: Document metadata storage
        CHROMADB_DIR: ChromaDB vector store
        LOGS_DIR: Application logs
        ASSETS_DIR: Static assets (CSS, images)
        CSS_DIR: CSS stylesheets
        CONFIG_FILE: Runtime configuration JSON file
    """
    
    def __init__(self):
        """Initialize all paths and create directories."""
        self._resolve_paths()
        self._create_directories()
    
    def _resolve_paths(self) -> None:
        """Resolve all application paths relative to project root."""
        
        # Find project root (directory containing src/)
        # Start from this file and go up until we find src/ parent
        current = Path(__file__).resolve().parent  # .../src/config
        self.PROJECT_ROOT = current.parent.parent  # .../techflow-rag-agent
        
        # Validate project root
        if not (self.PROJECT_ROOT / 'src').exists():
            raise PathConfigurationError(
                f"Cannot find project root. Expected 'src' directory in {self.PROJECT_ROOT}"
            )
        
        # === Main Directories ===
        self.SRC_DIR = self.PROJECT_ROOT / 'src'
        self.DATA_DIR = self.PROJECT_ROOT / 'data'
        self.ASSETS_DIR = self.PROJECT_ROOT / 'assets'
        self.SPECS_DIR = self.PROJECT_ROOT / 'specs'
        self.DOCS_DIR = self.PROJECT_ROOT / 'docs'
        
        # === Data Subdirectories ===
        self.KNOWLEDGE_LIBRARY_DIR = self.DATA_DIR / 'knowledge_library'
        self.DOCUMENTS_DIR = self.KNOWLEDGE_LIBRARY_DIR / 'documents'
        self.METADATA_DIR = self.KNOWLEDGE_LIBRARY_DIR / 'metadata'
        self.CHROMADB_DIR = self.DATA_DIR / 'chromadb'
        self.LOGS_DIR = self.DATA_DIR / 'logs'
        
        # === Assets Subdirectories ===
        self.CSS_DIR = self.ASSETS_DIR / 'css'
        self.ICONS_DIR = self.ASSETS_DIR / 'icons'
        self.IMAGES_DIR = self.ASSETS_DIR / 'images'
        
        # === Configuration Files ===
        self.CONFIG_FILE = self.DATA_DIR / 'config.json'
        self.ENV_FILE = self.PROJECT_ROOT / '.env'
        self.ENV_EXAMPLE_FILE = self.PROJECT_ROOT / '.env.example'
        
        # === Logs ===
        self.APPLICATION_LOG = self.LOGS_DIR / 'application.log'
        self.ERROR_LOG = self.LOGS_DIR / 'error.log'
        
        # === CSS Files ===
        self.DARK_CSS = self.CSS_DIR / 'dark.css'
        self.LIGHT_CSS = self.CSS_DIR / 'light.css'
    
    def _create_directories(self) -> None:
        """
        Create all required directories if they don't exist.
        
        This ensures the application has a proper directory structure on first run.
        """
        directories = [
            self.DATA_DIR,
            self.KNOWLEDGE_LIBRARY_DIR,
            self.DOCUMENTS_DIR,
            self.METADATA_DIR,
            self.CHROMADB_DIR,
            self.LOGS_DIR,
            self.ASSETS_DIR,
            self.CSS_DIR,
            self.ICONS_DIR,
            self.IMAGES_DIR,
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise PathConfigurationError(
                    f"Failed to create directory {directory}: {e}"
                )
    
    def get_document_path(self, filename: str) -> Path:
        """
        Get full path for a document in the knowledge library.
        
        Args:
            filename: Name of the document file
        
        Returns:
            Path: Full path to the document
        
        Example:
            >>> paths = Paths()
            >>> doc_path = paths.get_document_path('manual.pdf')
            >>> print(doc_path)
            WindowsPath('d:/techflow-rag-agent/data/knowledge_library/documents/manual.pdf')
        """
        return self.DOCUMENTS_DIR / filename
    
    def get_metadata_path(self, filename: str) -> Path:
        """
        Get full path for document metadata JSON file.
        
        Args:
            filename: Name of the document (metadata will have same name + .json)
        
        Returns:
            Path: Full path to metadata JSON file
        
        Example:
            >>> paths = Paths()
            >>> meta_path = paths.get_metadata_path('manual.pdf')
            >>> print(meta_path)
            WindowsPath('d:/techflow-rag-agent/data/knowledge_library/metadata/manual.pdf.json')
        """
        return self.METADATA_DIR / f"{filename}.json"
    
    def get_relative_to_project(self, absolute_path: Path) -> Optional[Path]:
        """
        Convert absolute path to relative path from project root.
        
        Args:
            absolute_path: Absolute path to convert
        
        Returns:
            Path: Relative path from project root, or None if not under project
        
        Example:
            >>> paths = Paths()
            >>> abs_path = paths.DOCUMENTS_DIR / 'test.pdf'
            >>> rel_path = paths.get_relative_to_project(abs_path)
            >>> print(rel_path)
            PosixPath('data/knowledge_library/documents/test.pdf')
        """
        try:
            return absolute_path.relative_to(self.PROJECT_ROOT)
        except ValueError:
            return None
    
    def is_under_documents_dir(self, path: Path) -> bool:
        """
        Check if path is under documents directory.
        
        Args:
            path: Path to check
        
        Returns:
            bool: True if path is under documents directory
        """
        try:
            path.resolve().relative_to(self.DOCUMENTS_DIR)
            return True
        except ValueError:
            return False
    
    def get_summary(self) -> dict:
        """
        Get a summary of all paths (useful for debugging).
        
        Returns:
            dict: Dictionary with all path values as strings
        """
        return {
            'project_root': str(self.PROJECT_ROOT),
            'src_dir': str(self.SRC_DIR),
            'data_dir': str(self.DATA_DIR),
            'documents_dir': str(self.DOCUMENTS_DIR),
            'metadata_dir': str(self.METADATA_DIR),
            'chromadb_dir': str(self.CHROMADB_DIR),
            'logs_dir': str(self.LOGS_DIR),
            'config_file': str(self.CONFIG_FILE),
            'application_log': str(self.APPLICATION_LOG),
        }
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Paths(project_root={self.PROJECT_ROOT})"


# Global paths instance (singleton pattern)
_paths_instance: Optional[Paths] = None


def get_paths() -> Paths:
    """
    Get the global paths instance (singleton).
    
    Returns:
        Paths: The global paths instance
    
    Example:
        >>> from src.config.paths import get_paths
        >>> paths = get_paths()
        >>> print(paths.DOCUMENTS_DIR)
        WindowsPath('d:/techflow-rag-agent/data/knowledge_library/documents')
    """
    global _paths_instance
    
    if _paths_instance is None:
        _paths_instance = Paths()
    
    return _paths_instance


def reload_paths() -> Paths:
    """
    Reload paths (useful for testing).
    
    Returns:
        Paths: New paths instance
    """
    global _paths_instance
    _paths_instance = Paths()
    return _paths_instance


# Convenience: Allow direct import
__all__ = [
    'Paths',
    'PathConfigurationError',
    'get_paths',
    'reload_paths'
]
