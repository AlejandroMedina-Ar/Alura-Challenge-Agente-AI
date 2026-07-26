"""
Authentication Package

This package handles authentication and session management.

Modules:
- authentication: Password verification and login
- session: Session state management in Streamlit

Author: TechFlow Solutions Project
License: MIT
"""

from .authentication import (
    Authenticator,
    get_authenticator
)

from .session import (
    SessionManager,
    get_session_manager
)


__all__ = [
    # Classes
    'Authenticator',
    'SessionManager',
    
    # Singletons
    'get_authenticator',
    'get_session_manager',
]
