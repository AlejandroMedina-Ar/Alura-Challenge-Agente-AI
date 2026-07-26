"""
Sidebar Module

This module handles sidebar navigation and user info display.
Provides menu navigation and session information.

Author: TechFlow AI Project
License: MIT
"""

import streamlit as st

from src.services import get_authentication_service, get_configuration_service
from src.ui.theme import get_theme_icon
from src.utils import get_logger


logger = get_logger()


def render_sidebar() -> str:
    """
    Render sidebar with navigation menu.
    
    Returns:
        str: Selected page/menu item
    
    Example:
        >>> selected_page = render_sidebar()
        >>> if selected_page == "Chat":
        ...     render_chat_page()
    """
    with st.sidebar:
        # App branding
        st.markdown("# 🤖 TechFlow AI")
        st.caption("RAG-Powered Knowledge Agent")
        st.divider()
        
        # User info section
        render_user_info()
        st.divider()
        
        # Navigation menu
        st.markdown("### 📋 Menu")
        
        menu_items = {
            "💬 Chat": "Chat",
            "📚 Knowledge Library": "Knowledge",
            "⚙️ Settings": "Settings"
        }
        
        selected = st.radio(
            label="Navigation",
            options=list(menu_items.keys()),
            label_visibility="collapsed",
            key="navigation_menu"
        )
        
        # Map display name to page key
        selected_page = menu_items[selected]
        
        st.divider()
        
        # Theme toggle
        render_theme_toggle()
        
        # Footer
        render_sidebar_footer()
        
        return selected_page


def render_user_info() -> None:
    """
    Render user information section.
    
    Shows authentication status and user details.
    
    Example:
        >>> render_user_info()
    """
    auth_service = get_authentication_service()
    
    if auth_service.is_authenticated():
        user = auth_service.get_current_user()
        username = user.get('username', 'Admin')
        role = user.get('role', 'admin')
        
        st.markdown(f"**👤 User:** {username}")
        st.markdown(f"**🔑 Role:** {role.title()}")
        
        # Session duration
        duration = auth_service.get_session_duration()
        if duration:
            st.caption(f"Session: {duration}")
        
        # Logout button
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            auth_service.logout()
            st.rerun()
    else:
        st.info("Not authenticated")


def render_theme_toggle() -> None:
    """
    Render theme toggle section.
    
    Example:
        >>> render_theme_toggle()
    """
    config_service = get_configuration_service()
    current_theme = config_service.get_theme()
    
    st.markdown("### 🎨 Theme")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            f"☀️ Light",
            key="theme_light",
            disabled=(current_theme == 'light'),
            use_container_width=True
        ):
            config_service.set_theme('light')
            st.rerun()
    
    with col2:
        if st.button(
            f"🌙 Dark",
            key="theme_dark",
            disabled=(current_theme == 'dark'),
            use_container_width=True
        ):
            config_service.set_theme('dark')
            st.rerun()
    
    st.caption(f"Current: {current_theme.title()} {get_theme_icon(current_theme)}")


def render_sidebar_footer() -> None:
    """
    Render sidebar footer with app info.
    
    Example:
        >>> render_sidebar_footer()
    """
    st.markdown("---")
    st.caption("TechFlow AI RAG Agent")
    st.caption("Version 1.0.0")
    st.caption("© 2024 TechFlow")


def render_admin_sidebar() -> str:
    """
    Render admin sidebar with additional admin options.
    
    Returns:
        str: Selected page
    
    Example:
        >>> selected = render_admin_sidebar()
    """
    with st.sidebar:
        # App branding
        st.markdown("# 🤖 TechFlow AI")
        st.caption("RAG-Powered Knowledge Agent")
        st.caption("🛡️ Admin Panel")
        st.divider()
        
        # User info
        render_user_info()
        st.divider()
        
        # Admin navigation
        st.markdown("### 📋 Admin Menu")
        
        admin_menu = {
            "💬 Chat": "Chat",
            "📚 Knowledge Library": "Knowledge",
            "🔧 Admin Panel": "Admin",
            "⚙️ Settings": "Settings"
        }
        
        selected = st.radio(
            label="Navigation",
            options=list(admin_menu.keys()),
            label_visibility="collapsed",
            key="admin_navigation_menu"
        )
        
        selected_page = admin_menu[selected]
        
        st.divider()
        
        # Theme toggle
        render_theme_toggle()
        
        # Footer
        render_sidebar_footer()
        
        return selected_page


def render_compact_sidebar() -> None:
    """
    Render compact sidebar for login page.
    
    Example:
        >>> render_compact_sidebar()
    """
    with st.sidebar:
        st.markdown("# 🤖 TechFlow AI")
        st.caption("RAG-Powered Knowledge Agent")
        st.divider()
        
        st.info("Please log in to continue")
        
        st.divider()
        render_sidebar_footer()


def get_navigation_state() -> str:
    """
    Get current navigation state from session.
    
    Returns:
        str: Current page
    
    Example:
        >>> page = get_navigation_state()
        >>> print(page)
        'Chat'
    """
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Chat'
    
    return st.session_state.current_page


def set_navigation_state(page: str) -> None:
    """
    Set navigation state in session.
    
    Args:
        page: Page to navigate to
    
    Example:
        >>> set_navigation_state('Settings')
    """
    st.session_state.current_page = page
    logger.debug(f"Navigation changed", page=page)


def render_quick_stats() -> None:
    """
    Render quick statistics in sidebar.
    
    Example:
        >>> render_quick_stats()
    """
    from src.services import get_knowledge_library_service, get_indexing_service
    
    try:
        kl_service = get_knowledge_library_service()
        indexing_service = get_indexing_service()
        
        stats = kl_service.get_storage_stats()
        indexing_stats = indexing_service.get_indexing_stats()
        
        st.markdown("### 📊 Quick Stats")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Documents",
                value=stats['total_documents']
            )
        
        with col2:
            st.metric(
                label="Chunks",
                value=indexing_stats['total_chunks']
            )
        
        st.caption(f"Indexed: {stats['indexed_documents']}/{stats['total_documents']}")
        
    except Exception as e:
        logger.error(f"Failed to render quick stats", error=str(e))
        st.caption("Stats unavailable")


# Convenience: Allow direct import
__all__ = [
    'render_sidebar',
    'render_user_info',
    'render_theme_toggle',
    'render_sidebar_footer',
    'render_admin_sidebar',
    'render_compact_sidebar',
    'get_navigation_state',
    'set_navigation_state',
    'render_quick_stats',
]
