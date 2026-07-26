"""
Session Management Module

This module manages user sessions using Streamlit session_state.
Handles authentication state, user info, and session lifecycle.

Author: TechFlow AI Project
License: MIT
"""

from typing import Optional
from datetime import datetime

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

from src.config import SessionKey
from src.utils import (
    get_logger,
    NotAuthenticatedError
)


logger = get_logger()


class SessionManager:
    """
    Manages user session state in Streamlit.
    
    Features:
    - Initialize session state
    - Login/logout operations
    - Check authentication status
    - Get current user info
    - Session state management
    
    All session data is stored in Streamlit's session_state.
    """
    
    def __init__(self):
        """
        Initialize session manager.
        
        Note: Requires Streamlit to be available.
        """
        if not STREAMLIT_AVAILABLE:
            logger.warning("Streamlit not available - SessionManager will not work")
        
        logger.debug("SessionManager initialized")
    
    def initialize_session(self) -> None:
        """
        Initialize session state with default values.
        
        Sets up all required session keys if they don't exist.
        This should be called at app startup.
        
        Example:
            >>> session = SessionManager()
            >>> session.initialize_session()
        """
        if not STREAMLIT_AVAILABLE:
            return
        
        # Authentication state
        if SessionKey.AUTHENTICATED not in st.session_state:
            st.session_state[SessionKey.AUTHENTICATED] = False
        
        if SessionKey.IS_ADMIN not in st.session_state:
            st.session_state[SessionKey.IS_ADMIN] = False
        
        # User info
        if 'user_info' not in st.session_state:
            st.session_state['user_info'] = None
        
        # Session metadata
        if 'session_start' not in st.session_state:
            st.session_state['session_start'] = datetime.now().isoformat()
        
        if 'last_activity' not in st.session_state:
            st.session_state['last_activity'] = datetime.now().isoformat()
        
        logger.debug("Session state initialized")
    
    def login(self, user_info: dict) -> None:
        """
        Log in a user and update session state.
        
        Args:
            user_info: User information dict (username, role, etc.)
        
        Example:
            >>> session = SessionManager()
            >>> user_info = {
            ...     'username': 'admin',
            ...     'role': 'admin',
            ...     'authenticated': True
            ... }
            >>> session.login(user_info)
        """
        if not STREAMLIT_AVAILABLE:
            return
        
        st.session_state[SessionKey.AUTHENTICATED] = True
        st.session_state[SessionKey.IS_ADMIN] = user_info.get('role') == 'admin'
        st.session_state['user_info'] = user_info
        st.session_state['login_time'] = datetime.now().isoformat()
        st.session_state['last_activity'] = datetime.now().isoformat()
        
        logger.info(f"User logged in", username=user_info.get('username'))
    
    def logout(self) -> None:
        """
        Log out current user and clear session state.
        
        Example:
            >>> session = SessionManager()
            >>> session.logout()
        """
        if not STREAMLIT_AVAILABLE:
            return
        
        username = self.get_username()
        
        # Clear authentication
        st.session_state[SessionKey.AUTHENTICATED] = False
        st.session_state[SessionKey.IS_ADMIN] = False
        st.session_state['user_info'] = None
        
        # Clear login metadata
        if 'login_time' in st.session_state:
            del st.session_state['login_time']
        
        logger.info(f"User logged out", username=username)
    
    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated.
        
        Returns:
            bool: True if user is authenticated
        
        Example:
            >>> session = SessionManager()
            >>> if session.is_authenticated():
            ...     print("User is logged in")
            ... else:
            ...     print("User is not logged in")
        """
        if not STREAMLIT_AVAILABLE:
            return False
        
        return st.session_state.get(SessionKey.AUTHENTICATED, False)
    
    def is_admin(self) -> bool:
        """
        Check if current user is an admin.
        
        Returns:
            bool: True if user is admin
        
        Example:
            >>> session = SessionManager()
            >>> if session.is_admin():
            ...     print("Admin access granted")
        """
        if not STREAMLIT_AVAILABLE:
            return False
        
        return st.session_state.get(SessionKey.IS_ADMIN, False)
    
    def get_user_info(self) -> Optional[dict]:
        """
        Get current user information.
        
        Returns:
            dict: User info or None if not authenticated
        
        Example:
            >>> session = SessionManager()
            >>> user = session.get_user_info()
            >>> if user:
            ...     print(f"Current user: {user['username']}")
        """
        if not STREAMLIT_AVAILABLE:
            return None
        
        return st.session_state.get('user_info')
    
    def get_username(self) -> Optional[str]:
        """
        Get current username.
        
        Returns:
            str: Username or None if not authenticated
        
        Example:
            >>> session = SessionManager()
            >>> username = session.get_username()
            >>> print(username)
            'admin'
        """
        user_info = self.get_user_info()
        return user_info.get('username') if user_info else None
    
    def require_authentication(self) -> None:
        """
        Require authentication, raise exception if not authenticated.
        
        Use this to protect admin-only operations.
        
        Raises:
            NotAuthenticatedError: If user is not authenticated
        
        Example:
            >>> session = SessionManager()
            >>> session.require_authentication()  # Raises if not logged in
            >>> # Protected code here...
        """
        if not self.is_authenticated():
            raise NotAuthenticatedError("admin panel")
    
    def require_admin(self) -> None:
        """
        Require admin privileges.
        
        Raises:
            NotAuthenticatedError: If user is not authenticated or not admin
        
        Example:
            >>> session = SessionManager()
            >>> session.require_admin()  # Raises if not admin
            >>> # Admin-only code here...
        """
        self.require_authentication()
        
        if not self.is_admin():
            raise NotAuthenticatedError("admin features")
    
    def update_activity(self) -> None:
        """
        Update last activity timestamp.
        
        Call this on user interactions to track activity.
        
        Example:
            >>> session = SessionManager()
            >>> session.update_activity()
        """
        if not STREAMLIT_AVAILABLE:
            return
        
        st.session_state['last_activity'] = datetime.now().isoformat()
    
    def get_session_duration(self) -> Optional[str]:
        """
        Get session duration since login.
        
        Returns:
            str: Duration string (e.g., "1h 23m") or None if not logged in
        
        Example:
            >>> session = SessionManager()
            >>> duration = session.get_session_duration()
            >>> print(f"Session duration: {duration}")
            'Session duration: 45m 12s'
        """
        if not STREAMLIT_AVAILABLE or not self.is_authenticated():
            return None
        
        login_time_str = st.session_state.get('login_time')
        if not login_time_str:
            return None
        
        try:
            login_time = datetime.fromisoformat(login_time_str)
            duration = datetime.now() - login_time
            
            seconds = int(duration.total_seconds())
            if seconds < 60:
                return f"{seconds}s"
            
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            
            if minutes < 60:
                return f"{minutes}m {remaining_seconds}s"
            
            hours = minutes // 60
            remaining_minutes = minutes % 60
            
            return f"{hours}h {remaining_minutes}m"
            
        except Exception:
            return None
    
    def clear_all(self) -> None:
        """
        Clear all session state.
        
        **WARNING:** This clears ALL session state, not just auth.
        
        Example:
            >>> session = SessionManager()
            >>> session.clear_all()
        """
        if not STREAMLIT_AVAILABLE:
            return
        
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        logger.warning("All session state cleared")


# Singleton instance
_session_manager_instance = None


def get_session_manager() -> SessionManager:
    """
    Get singleton SessionManager instance.
    
    Returns:
        SessionManager: Singleton instance
    
    Example:
        >>> from src.auth import get_session_manager
        >>> session = get_session_manager()
        >>> if session.is_authenticated():
        ...     print("User is logged in")
    """
    global _session_manager_instance
    
    if _session_manager_instance is None:
        _session_manager_instance = SessionManager()
        logger.debug("SessionManager singleton created")
    
    return _session_manager_instance


# Convenience: Allow direct import
__all__ = [
    'SessionManager',
    'get_session_manager',
]
