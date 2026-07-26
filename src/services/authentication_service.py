"""
Authentication Service Module

This module provides business logic for authentication operations.
Coordinates between auth module and session management.

Author: TechFlow AI Project
License: MIT
"""

from src.auth import get_authenticator, get_session_manager
from src.utils import (
    get_logger,
    InvalidCredentialsError,
    NotAuthenticatedError
)


logger = get_logger()


class AuthenticationService:
    """
    Service for authentication business logic.
    
    Features:
    - Login/logout operations
    - Session management
    - Authentication checks
    - User info retrieval
    """
    
    def __init__(self):
        """Initialize authentication service."""
        self.authenticator = get_authenticator()
        self.session_manager = get_session_manager()
        logger.debug("AuthenticationService initialized")
    
    def login(self, password: str) -> dict:
        """
        Authenticate admin user and create session.
        
        Args:
            password: Admin password
        
        Returns:
            dict: User info with authentication status
        
        Raises:
            InvalidCredentialsError: If password is incorrect
        
        Example:
            >>> service = AuthenticationService()
            >>> try:
            ...     user_info = service.login("admin_password")
            ...     print(f"Welcome {user_info['username']}")
            ... except InvalidCredentialsError:
            ...     print("Invalid password")
        """
        try:
            # Authenticate
            user_info = self.authenticator.login_admin(password)
            
            # Create session
            self.session_manager.login(user_info)
            
            logger.info("User logged in successfully", username=user_info.get('username'))
            
            return user_info
            
        except InvalidCredentialsError:
            logger.warning("Login failed - invalid credentials")
            raise
    
    def logout(self) -> None:
        """
        Log out current user and clear session.
        
        Example:
            >>> service = AuthenticationService()
            >>> service.logout()
        """
        username = self.session_manager.get_username()
        self.session_manager.logout()
        logger.info("User logged out", username=username)
    
    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated.
        
        Returns:
            bool: True if authenticated
        
        Example:
            >>> service = AuthenticationService()
            >>> if service.is_authenticated():
            ...     print("User is logged in")
        """
        return self.session_manager.is_authenticated()
    
    def require_authentication(self) -> None:
        """
        Require authentication, raise error if not authenticated.
        
        Use this to protect admin-only operations.
        
        Raises:
            NotAuthenticatedError: If not authenticated
        
        Example:
            >>> service = AuthenticationService()
            >>> service.require_authentication()  # Raises if not logged in
            >>> # Protected operation here
        """
        self.session_manager.require_authentication()
    
    def require_admin(self) -> None:
        """
        Require admin privileges.
        
        Raises:
            NotAuthenticatedError: If not authenticated or not admin
        
        Example:
            >>> service = AuthenticationService()
            >>> service.require_admin()  # Raises if not admin
            >>> # Admin-only operation here
        """
        self.session_manager.require_admin()
    
    def get_current_user(self) -> dict:
        """
        Get current user information.
        
        Returns:
            dict: User info or None if not authenticated
        
        Example:
            >>> service = AuthenticationService()
            >>> user = service.get_current_user()
            >>> if user:
            ...     print(f"Current user: {user['username']}")
        """
        return self.session_manager.get_user_info()
    
    def get_session_duration(self) -> str:
        """
        Get current session duration.
        
        Returns:
            str: Duration string or None
        
        Example:
            >>> service = AuthenticationService()
            >>> duration = service.get_session_duration()
            >>> print(f"Session active for: {duration}")
        """
        return self.session_manager.get_session_duration()
    
    def is_password_configured(self) -> bool:
        """
        Check if admin password is configured.
        
        Returns:
            bool: True if password is set
        
        Example:
            >>> service = AuthenticationService()
            >>> if not service.is_password_configured():
            ...     print("Warning: No admin password set!")
        """
        return self.authenticator.is_password_set()


# Singleton instance
_auth_service_instance = None


def get_authentication_service() -> AuthenticationService:
    """
    Get singleton AuthenticationService instance.
    
    Returns:
        AuthenticationService: Singleton instance
    
    Example:
        >>> from src.services import get_authentication_service
        >>> auth_service = get_authentication_service()
        >>> auth_service.login("password")
    """
    global _auth_service_instance
    
    if _auth_service_instance is None:
        _auth_service_instance = AuthenticationService()
        logger.debug("AuthenticationService singleton created")
    
    return _auth_service_instance


# Convenience: Allow direct import
__all__ = [
    'AuthenticationService',
    'get_authentication_service',
]
