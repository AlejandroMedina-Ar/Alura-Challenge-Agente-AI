"""
Authentication Module

This module handles user authentication for the admin panel.
Uses simple password-based authentication with bcrypt hashing.

Author: TechFlow Solutions Project
License: MIT
"""

from src.config import get_settings
from src.utils import (
    get_logger,
    InvalidCredentialsError,
    hash_password,
    verify_password
)


logger = get_logger()


class Authenticator:
    """
    Handles authentication operations.
    
    Features:
    - Password verification against hashed password in .env
    - Login attempts tracking (optional)
    - Simple admin authentication
    
    Authentication is intentionally simple for this demo project.
    """
    
    def __init__(self):
        """Initialize authenticator with settings."""
        self.settings = get_settings()
        logger.debug("Authenticator initialized")
    
    def verify_admin_password(self, password: str) -> bool:
        """
        Verify admin password against stored hash.
        
        Args:
            password: Plain text password to verify
        
        Returns:
            bool: True if password is correct
        
        Raises:
            InvalidCredentialsError: If password is incorrect
        
        Example:
            >>> auth = Authenticator()
            >>> try:
            ...     auth.verify_admin_password('correct_password')
            ...     print("Access granted")
            ... except InvalidCredentialsError:
            ...     print("Access denied")
        """
        # Get hashed password from settings
        stored_hash = self.settings.ADMIN_PASSWORD_HASH
        
        # Verify password
        is_valid = verify_password(password, stored_hash)
        
        if is_valid:
            logger.info("Admin authentication successful")
            return True
        else:
            logger.warning("Admin authentication failed - invalid password")
            raise InvalidCredentialsError()
    
    def login_admin(self, password: str) -> dict:
        """
        Authenticate admin user.
        
        Args:
            password: Plain text password
        
        Returns:
            dict: User info (username, role, authenticated)
        
        Raises:
            InvalidCredentialsError: If credentials are invalid
        
        Example:
            >>> auth = Authenticator()
            >>> user_info = auth.login_admin('my_password')
            >>> print(user_info)
            {
                'username': 'admin',
                'role': 'admin',
                'authenticated': True
            }
        """
        # Verify password
        self.verify_admin_password(password)
        
        # Return user info
        user_info = {
            'username': 'admin',
            'role': 'admin',
            'authenticated': True
        }
        
        logger.info("Admin login successful")
        return user_info
    
    def is_password_set(self) -> bool:
        """
        Check if admin password is configured.
        
        Returns:
            bool: True if password is set in .env
        
        Example:
            >>> auth = Authenticator()
            >>> if not auth.is_password_set():
            ...     print("Warning: No admin password configured!")
        """
        return bool(self.settings.ADMIN_PASSWORD_HASH)
    
    @staticmethod
    def hash_new_password(password: str) -> str:
        """
        Hash a new password for storage in .env.
        
        This is a utility method for initial setup.
        
        Args:
            password: Plain text password
        
        Returns:
            str: Bcrypt hash
        
        Example:
            >>> Authenticator.hash_new_password('my_secure_password')
            '$2b$12$...'
        """
        return hash_password(password)


# Singleton instance
_authenticator_instance = None


def get_authenticator() -> Authenticator:
    """
    Get singleton Authenticator instance.
    
    Returns:
        Authenticator: Singleton instance
    
    Example:
        >>> from src.auth import get_authenticator
        >>> auth = get_authenticator()
        >>> user = auth.login_admin('password')
    """
    global _authenticator_instance
    
    if _authenticator_instance is None:
        _authenticator_instance = Authenticator()
        logger.debug("Authenticator singleton created")
    
    return _authenticator_instance


# Convenience: Allow direct import
__all__ = [
    'Authenticator',
    'get_authenticator',
]
