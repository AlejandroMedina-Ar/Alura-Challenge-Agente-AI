"""
Módulo de Barra Lateral

Este módulo maneja la navegación de la barra lateral y la visualización de información del usuario.
Proporciona navegación de menú e información de sesión.

Autor: TechFlow Solutions Project
Licencia: MIT
"""

import streamlit as st

from src.services import get_authentication_service, get_configuration_service
from src.ui.theme import get_theme_icon
from src.utils import get_logger


logger = get_logger()


def render_sidebar() -> str:
    """
    Renderiza la barra lateral con menú de navegación.
    
    Retorna:
        str: Página/ítem de menú seleccionado
    
    Ejemplo:
        >>> selected_page = render_sidebar()
        >>> if selected_page == "Chat":
        ...     render_chat_page()
    """
    with st.sidebar:
        # App branding
        st.markdown("# 🤖 TechFlow Solutions")
        st.caption("Agente de Conocimiento con RAG")
        st.divider()
        
        # User info section
        render_user_info()
        st.divider()
        
        # Navigation menu
        st.markdown("### 📋 Menú")
        
        # Check if user is admin
        is_admin = st.session_state.get('is_admin', False)
        
        menu_items = {
            "💬 Chat": "Chat",
            "📚 Biblioteca de Conocimiento": "Knowledge",
            "⚙️ Configuración": "Settings"
        }
        
        # Add Admin panel only for admins
        if is_admin:
            menu_items["🔧 Panel de Administración"] = "Admin"
        
        selected = st.radio(
            label="Navegación",
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
    Renderiza la sección de información del usuario.
    
    Muestra el estado de autenticación y detalles del usuario.
    
    Ejemplo:
        >>> render_user_info()
    """
    auth_service = get_authentication_service()
    
    if auth_service.is_authenticated():
        user = auth_service.get_current_user()
        username = user.get('username', 'Admin')
        role = user.get('role', 'admin')
        
        st.markdown(f"**👤 Usuario:** {username}")
        st.markdown(f"**🔑 Rol:** {role.title()}")
        
        # Session duration
        duration = auth_service.get_session_duration()
        if duration:
            st.caption(f"Sesión: {duration}")
        
        # Logout button
        if st.button("🚪 Cerrar Sesión", key="logout_btn", use_container_width=True):
            auth_service.logout()
            st.rerun()
    else:
        # Guest user mode
        st.markdown("**👤 Usuario:** Invitado")
        st.caption("Acceso de solo lectura")
        
        # Login as admin option
        if st.button("🔐 Login como Admin", key="login_admin_btn", use_container_width=True):
            # Force redirect to login page by clearing any cached state
            st.session_state.clear()
            st.rerun()


def render_theme_toggle() -> None:
    """
    Renderiza la sección de cambio de tema.
    
    Ejemplo:
        >>> render_theme_toggle()
    """
    config_service = get_configuration_service()
    current_theme = config_service.get_theme()
    
    st.markdown("### 🎨 Tema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            f"☀️ Claro",
            key="theme_light",
            disabled=(current_theme == 'light'),
            use_container_width=True
        ):
            config_service.set_theme('light')
            st.rerun()
    
    with col2:
        if st.button(
            f"🌙 Oscuro",
            key="theme_dark",
            disabled=(current_theme == 'dark'),
            use_container_width=True
        ):
            config_service.set_theme('dark')
            st.rerun()
    
    st.caption(f"Actual: {current_theme.title()} {get_theme_icon(current_theme)}")


def render_sidebar_footer() -> None:
    """
    Renderiza el pie de la barra lateral con información de la aplicación.
    
    Ejemplo:
        >>> render_sidebar_footer()
    """
    st.markdown("---")
    st.caption("TechFlow Solutions Agente RAG")
    st.caption("Versión 1.0.0")
    st.caption("© 2026 TechFlow")


def render_admin_sidebar() -> str:
    """
    Renderiza la barra lateral de admin con opciones adicionales de administración.
    
    Retorna:
        str: Página seleccionada
    
    Ejemplo:
        >>> selected = render_admin_sidebar()
    """
    with st.sidebar:
        # App branding
        st.markdown("# 🤖 TechFlow Solutions")
        st.caption("Agente de Conocimiento con RAG")
        st.caption("🛡️ Panel de Admin")
        st.divider()
        
        # User info
        render_user_info()
        st.divider()
        
        # Admin navigation
        st.markdown("### 📋 Menú Admin")
        
        admin_menu = {
            "💬 Chat": "Chat",
            "📚 Biblioteca de Conocimiento": "Knowledge",
            "🔧 Panel de Administración": "Admin",
            "⚙️ Configuración": "Settings"
        }
        
        selected = st.radio(
            label="Navegación",
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
    Renderiza barra lateral compacta para la página de login.
    
    Ejemplo:
        >>> render_compact_sidebar()
    """
    with st.sidebar:
        st.markdown("# 🤖 TechFlow Solutions")
        st.caption("Agente de Conocimiento con RAG")
        st.divider()
        
        st.info("Por favor inicia sesión para continuar")
        
        st.divider()
        render_sidebar_footer()


def get_navigation_state() -> str:
    """
    Obtiene el estado de navegación actual de la sesión.
    
    Retorna:
        str: Página actual
    
    Ejemplo:
        >>> page = get_navigation_state()
        >>> print(page)
        'Chat'
    """
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Chat'
    
    return st.session_state.current_page


def set_navigation_state(page: str) -> None:
    """
    Establece el estado de navegación en la sesión.
    
    Args:
        page: Página a la que navegar
    
    Ejemplo:
        >>> set_navigation_state('Settings')
    """
    st.session_state.current_page = page
    logger.debug(f"Navigation changed", page=page)


def render_quick_stats() -> None:
    """
    Renderiza estadísticas rápidas en la barra lateral.
    
    Ejemplo:
        >>> render_quick_stats()
    """
    from src.services import get_knowledge_library_service, get_indexing_service
    
    try:
        kl_service = get_knowledge_library_service()
        indexing_service = get_indexing_service()
        
        stats = kl_service.get_storage_stats()
        indexing_stats = indexing_service.get_indexing_stats()
        
        st.markdown("### 📊 Estadísticas Rápidas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Documentos",
                value=stats['total_documents']
            )
        
        with col2:
            st.metric(
                label="Fragmentos",
                value=indexing_stats['total_chunks']
            )
        
        st.caption(f"Indexados: {stats['indexed_documents']}/{stats['total_documents']}")
        
    except Exception as e:
        logger.error(f"Failed to render quick stats", error=str(e))
        st.caption("Estadísticas no disponibles")


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
