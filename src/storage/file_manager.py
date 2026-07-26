"""
File Manager Module

This module handles all file system operations for document storage.
Provides safe file operations with proper error handling.

Author: TechFlow Solutions Project
License: MIT
"""

import shutil
from pathlib import Path
from typing import Optional, BinaryIO

from src.config import get_paths
from src.utils import (
    get_logger,
    FileNotFoundError,
    WriteError,
    ReadError,
    DeleteError,
    calculate_file_checksum,
    calculate_content_checksum,
    sanitize_filename,
    generate_unique_filename
)


logger = get_logger()


class FileManager:
    """
    Manages file operations for knowledge library documents.
    
    Features:
    - Safe file saving with duplicate handling
    - File reading with error handling
    - File deletion with verification
    - File moving/renaming
    - Checksum calculation
    - Filename sanitization
    
    All file operations are logged for audit trail.
    """
    
    def __init__(self):
        """Initialize file manager with paths configuration."""
        self.paths = get_paths()
        logger.debug("FileManager initialized")
    
    def save_file(
        self,
        content: bytes,
        filename: str,
        allow_duplicates: bool = False
    ) -> Path:
        """
        Save file content to documents directory.
        
        Args:
            content: File content as bytes
            filename: Desired filename
            allow_duplicates: If True, generate unique name for duplicates
        
        Returns:
            Path: Full path to saved file
        
        Raises:
            WriteError: If file cannot be saved
        
        Example:
            >>> fm = FileManager()
            >>> content = b'PDF content...'
            >>> path = fm.save_file(content, 'document.pdf')
            >>> print(path)
            WindowsPath('d:/techflow-rag-agent/data/knowledge_library/documents/document.pdf')
        """
        try:
            # Sanitize filename
            safe_filename = sanitize_filename(filename)
            
            # Handle duplicates
            if allow_duplicates:
                existing_files = [f.name for f in self.paths.DOCUMENTS_DIR.iterdir()]
                safe_filename = generate_unique_filename(safe_filename, existing_files)
            
            # Get full path
            file_path = self.paths.get_document_path(safe_filename)
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            file_path.write_bytes(content)
            
            # Calculate checksum for verification
            checksum = calculate_content_checksum(content)
            
            logger.info(
                f"File saved successfully",
                filename=safe_filename,
                size=len(content),
                checksum=checksum[:16]
            )
            
            return file_path
            
        except OSError as e:
            logger.error(f"Failed to save file: {filename}", exc_info=True)
            raise WriteError(filename, str(e))
    
    def read_file(self, filename: str) -> bytes:
        """
        Read file content from documents directory.
        
        Args:
            filename: Name of the file to read
        
        Returns:
            bytes: File content
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ReadError: If file cannot be read
        
        Example:
            >>> fm = FileManager()
            >>> content = fm.read_file('document.pdf')
            >>> print(len(content))
            1048576
        """
        file_path = self.paths.get_document_path(filename)
        
        if not file_path.exists():
            logger.warning(f"File not found: {filename}")
            raise FileNotFoundError(filename)
        
        try:
            content = file_path.read_bytes()
            logger.debug(f"File read successfully", filename=filename, size=len(content))
            return content
            
        except OSError as e:
            logger.error(f"Failed to read file: {filename}", exc_info=True)
            raise ReadError(str(file_path), str(e))
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete file from documents directory.
        
        Args:
            filename: Name of the file to delete
        
        Returns:
            bool: True if file was deleted
        
        Raises:
            FileNotFoundError: If file doesn't exist
            DeleteError: If file cannot be deleted
        
        Example:
            >>> fm = FileManager()
            >>> fm.delete_file('document.pdf')
            True
        """
        file_path = self.paths.get_document_path(filename)
        
        if not file_path.exists():
            logger.warning(f"Cannot delete, file not found: {filename}")
            raise FileNotFoundError(filename)
        
        try:
            file_path.unlink()
            logger.info(f"File deleted successfully", filename=filename)
            return True
            
        except OSError as e:
            logger.error(f"Failed to delete file: {filename}", exc_info=True)
            raise DeleteError(str(file_path), str(e))
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if file exists in documents directory.
        
        Args:
            filename: Name of the file to check
        
        Returns:
            bool: True if file exists
        
        Example:
            >>> fm = FileManager()
            >>> fm.file_exists('document.pdf')
            True
        """
        file_path = self.paths.get_document_path(filename)
        return file_path.exists()
    
    def get_file_size(self, filename: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            filename: Name of the file
        
        Returns:
            int: File size in bytes
        
        Raises:
            FileNotFoundError: If file doesn't exist
        
        Example:
            >>> fm = FileManager()
            >>> size = fm.get_file_size('document.pdf')
            >>> print(size)
            1048576
        """
        file_path = self.paths.get_document_path(filename)
        
        if not file_path.exists():
            raise FileNotFoundError(filename)
        
        return file_path.stat().st_size
    
    def get_file_checksum(self, filename: str) -> str:
        """
        Calculate checksum of a file.
        
        Args:
            filename: Name of the file
        
        Returns:
            str: SHA256 checksum (hexadecimal)
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ReadError: If checksum calculation fails
        
        Example:
            >>> fm = FileManager()
            >>> checksum = fm.get_file_checksum('document.pdf')
            >>> print(checksum)
            'a3f5b2c1d4e5f6...'
        """
        file_path = self.paths.get_document_path(filename)
        
        if not file_path.exists():
            raise FileNotFoundError(filename)
        
        try:
            return calculate_file_checksum(file_path)
        except Exception as e:
            raise ReadError(str(file_path), f"checksum calculation failed: {e}")
    
    def move_file(self, old_filename: str, new_filename: str) -> Path:
        """
        Move/rename file within documents directory.
        
        Args:
            old_filename: Current filename
            new_filename: New filename
        
        Returns:
            Path: New file path
        
        Raises:
            FileNotFoundError: If source file doesn't exist
            WriteError: If file cannot be moved
        
        Example:
            >>> fm = FileManager()
            >>> new_path = fm.move_file('old.pdf', 'new.pdf')
            >>> print(new_path)
            WindowsPath('.../documents/new.pdf')
        """
        old_path = self.paths.get_document_path(old_filename)
        new_path = self.paths.get_document_path(sanitize_filename(new_filename))
        
        if not old_path.exists():
            raise FileNotFoundError(old_filename)
        
        try:
            old_path.rename(new_path)
            logger.info(
                f"File moved/renamed",
                old_name=old_filename,
                new_name=new_filename
            )
            return new_path
            
        except OSError as e:
            logger.error(
                f"Failed to move file: {old_filename} -> {new_filename}",
                exc_info=True
            )
            raise WriteError(new_filename, str(e))
    
    def copy_file(self, filename: str, new_filename: str) -> Path:
        """
        Copy file within documents directory.
        
        Args:
            filename: Source filename
            new_filename: Destination filename
        
        Returns:
            Path: New file path
        
        Raises:
            FileNotFoundError: If source file doesn't exist
            WriteError: If file cannot be copied
        
        Example:
            >>> fm = FileManager()
            >>> copy_path = fm.copy_file('original.pdf', 'copy.pdf')
        """
        src_path = self.paths.get_document_path(filename)
        dst_path = self.paths.get_document_path(sanitize_filename(new_filename))
        
        if not src_path.exists():
            raise FileNotFoundError(filename)
        
        try:
            shutil.copy2(src_path, dst_path)
            logger.info(
                f"File copied",
                source=filename,
                destination=new_filename
            )
            return dst_path
            
        except OSError as e:
            logger.error(
                f"Failed to copy file: {filename} -> {new_filename}",
                exc_info=True
            )
            raise WriteError(new_filename, str(e))
    
    def list_files(self, pattern: str = "*") -> list[Path]:
        """
        List all files in documents directory.
        
        Args:
            pattern: Glob pattern (default: "*" for all files)
        
        Returns:
            list[Path]: List of file paths
        
        Example:
            >>> fm = FileManager()
            >>> files = fm.list_files("*.pdf")
            >>> for file in files:
            ...     print(file.name)
            document1.pdf
            document2.pdf
        """
        try:
            files = list(self.paths.DOCUMENTS_DIR.glob(pattern))
            # Filter only files (not directories)
            files = [f for f in files if f.is_file()]
            logger.debug(f"Listed {len(files)} files", pattern=pattern)
            return files
        except Exception as e:
            logger.error(f"Failed to list files", exc_info=True, pattern=pattern)
            return []
    
    def get_file_count(self) -> int:
        """
        Get total number of files in documents directory.
        
        Returns:
            int: Number of files
        
        Example:
            >>> fm = FileManager()
            >>> count = fm.get_file_count()
            >>> print(count)
            42
        """
        return len(self.list_files())
    
    def get_total_size(self) -> int:
        """
        Get total size of all files in documents directory.
        
        Returns:
            int: Total size in bytes
        
        Example:
            >>> fm = FileManager()
            >>> total = fm.get_total_size()
            >>> print(f"{total / (1024*1024):.2f} MB")
            125.50 MB
        """
        total = 0
        for file_path in self.list_files():
            try:
                total += file_path.stat().st_size
            except OSError:
                continue
        return total
    
    def clear_all_files(self) -> int:
        """
        Delete all files from documents directory.
        
        **WARNING:** This is destructive and cannot be undone!
        
        Returns:
            int: Number of files deleted
        
        Example:
            >>> fm = FileManager()
            >>> deleted = fm.clear_all_files()
            >>> print(f"Deleted {deleted} files")
        """
        files = self.list_files()
        deleted = 0
        
        for file_path in files:
            try:
                file_path.unlink()
                deleted += 1
            except OSError as e:
                logger.error(f"Failed to delete file during clear", file=file_path.name)
                continue
        
        logger.warning(f"Cleared all files from documents directory", count=deleted)
        return deleted


# Convenience: Allow direct import
__all__ = [
    'FileManager',
]
