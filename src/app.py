"""
TechFlow Solutions RAG Agent - Aplicación Principal

Este es el punto de entrada principal para la aplicación Streamlit.
Maneja enrutamiento, autenticación y renderizado de páginas.

Autor: TechFlow Solutions Project
Licencia: MIT
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.services import get_authentication_service, get_configuration_service
from src.config import SessionKey
from src.ui import (
    apply_theme,
    load_theme_from_config,
    hide_streamlit_elements,
    render_sidebar,
    render_compact_sidebar,
    render_chat_page,
    render_admin_panel,
    render_settings_panel
)
from src.ui.admin_panel import render_documents_tab
from src.utils import get_logger, NotAuthenticatedError


logger = get_logger()


def main():
    """
    Punto de entrada principal de la aplicación.
    
    Maneja:
    - Configuración de página
    - Aplicación de tema
    - Autenticación
    - Enrutamiento de páginas
    """
    # Configure page
    st.set_page_config(
        page_title="TechFlow Solutions - Agente RAG",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
    
    # Force sidebar to stay open - clear localStorage on every load
    st.markdown("""
        <script>
            // Clear sidebar state from localStorage on every page load
            const keysToRemove = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && (key.includes('sidebar') || key.includes('Sidebar'))) {
                    keysToRemove.push(key);
                }
            }
            keysToRemove.forEach(key => localStorage.removeItem(key));
        </script>
    """, unsafe_allow_html=True)
    
    # Apply theme
    config_service = get_configuration_service()
    theme = load_theme_from_config(config_service)
    apply_theme(theme)
    
    # Hide default Streamlit elements
    hide_streamlit_elements()
    
    # Check authentication
    auth_service = get_authentication_service()
    
    # Check if there are documents in the system
    from src.services import get_knowledge_library_service
    kl_service = get_knowledge_library_service()
    has_documents = kl_service.get_document_count() > 0
    
    # Check if user explicitly requested login (from guest mode)
    force_login = st.session_state.get('force_login', False)
    
    # Check if user explicitly chose guest mode
    guest_mode = st.session_state.get(SessionKey.GUEST_MODE, False)
    
    # Log for debugging
    logger.debug(f"Auth check: authenticated={auth_service.is_authenticated()}, has_documents={has_documents}, guest_mode={guest_mode}, force_login={force_login}")
    
    # Determine access mode with SIMPLIFIED logic:
    # Priority order:
    # 1. If authenticated → Admin mode
    # 2. If force_login → Show login page
    # 3. If has documents → Guest mode (auto-enable)
    # 4. If no documents → Setup mode (login required)
    
    if auth_service.is_authenticated():
        # User is authenticated as admin
        logger.info("Rendering main app as admin")
        # Clear force_login flag
        if 'force_login' in st.session_state:
            del st.session_state['force_login']
        render_main_app(is_admin=True)
    elif force_login:
        # User explicitly requested login from guest mode
        logger.info("User requested admin login from guest mode")
        render_login_page(setup_mode=False)
    elif has_documents:
        # Has documents → ALWAYS allow guest access (auto-enable)
        if not guest_mode:
            st.session_state[SessionKey.GUEST_MODE] = True
            logger.info("Auto-enabled guest mode (documents available)")
        render_main_app(is_admin=False)
    else:
        # No documents → Setup mode (login required)
        logger.info("No documents - requiring admin setup")
        render_login_page(setup_mode=True)


def render_login_page(setup_mode=False):
    """
    Renderiza la página de inicio de sesión para usuarios no autenticados.
    
    Args:
        setup_mode: Si True, indica que se requiere login para setup inicial (sin opción guest)
    """
    # Compact sidebar for login
    render_compact_sidebar()
    
    # Formulario de login
    st.title("🤖 TechFlow Solutions")
    st.markdown("### Agente de Conocimiento con RAG")
    st.divider()
    
    if setup_mode:
        st.info("👋 **Bienvenido!** Se requiere autenticación de administrador para cargar los primeros documentos.")
    else:
        # If NOT setup mode, user can choose to continue as guest
        st.info("💡 **Tip:** Puedes entrar como invitado para consultar documentos, o como admin para gestionar el sistema.")
    
    # Check if we can allow guest access
    from src.services import get_knowledge_library_service
    kl_service = get_knowledge_library_service()
    has_documents = kl_service.get_document_count() > 0
    
    # Option to continue as guest (only if documents exist)
    if has_documents and not setup_mode:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👥 Continuar como Invitado", type="secondary", use_container_width=True):
                # Don't authenticate, just proceed to main app
                logger.info("User entered as guest")
                st.session_state[SessionKey.GUEST_MODE] = True
                st.rerun()
        with col2:
            pass  # Space for alignment
        
        st.markdown("---")
    
    st.markdown("#### 🔐 Inicio de Sesión Admin")
    
    with st.form("login_form"):
        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="Ingresa la contraseña de administrador"
        )
        
        submit = st.form_submit_button("Iniciar Sesión", type="primary", use_container_width=True)
        
        if submit:
            if password:
                try:
                    auth_service = get_authentication_service()
                    auth_service.login(password)
                    st.success("✅ ¡Inicio de sesión exitoso!")
                    logger.info("User logged in via web interface")
                    st.session_state[SessionKey.GUEST_MODE] = False
                    # Clear force_login flag after successful login
                    if 'force_login' in st.session_state:
                        del st.session_state['force_login']
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al iniciar sesión: {str(e)}")
                    logger.warning("Login attempt failed")
            else:
                st.warning("⚠️ Por favor ingresa una contraseña")
    
    st.divider()
    
    # Sección de información
    with st.expander("ℹ️ Acerca de TechFlow Solutions"):
        st.markdown("""
        ### Características
        - 🔍 **Chat con RAG** - Respuestas contextuales desde tus documentos
        - 📚 **Biblioteca de Conocimiento** - Sube y administra documentos
        - ⚡ **Indexación Inteligente** - Fragmentación y embedding automático
        - 🤖 **Soporte Dual de LLM** - Gemini 3.6 Flash + respaldo Cohere
        - ⚙️ **Configurable** - Personaliza RAG y configuración de LLM
        
        ### Stack Tecnológico
        - **LLM:** Google Gemini 3.6 Flash (principal), Cohere Command-R (respaldo)
        - **Embeddings:** Multilingual E5-base (768 dimensiones)
        - **Vector Store:** ChromaDB (persistente)
        - **Framework:** Streamlit
        
        ### Credenciales por Defecto
        - **Usuario:** admin
        - **Contraseña:** Verifica tu archivo `.env` o usa la configuración por defecto
        """)


def render_main_app(is_admin=False):
    """
    Renderiza la aplicación principal con navegación.
    
    Args:
        is_admin: Si True, el usuario tiene privilegios de administrador
    """
    # Store admin status in session state
    st.session_state[SessionKey.IS_ADMIN] = is_admin
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to selected page (with access control)
    if selected_page == "Chat":
        render_chat_page()
    
    elif selected_page == "Knowledge":
        # Allow viewing documents for all users
        render_knowledge_page()
    
    elif selected_page == "Admin":
        # Admin panel only accessible to admins
        if is_admin:
            render_admin_panel()
        else:
            st.warning("🔒 Esta sección requiere autenticación de administrador")
            render_admin_login_link()
    
    elif selected_page == "Settings":
        # Settings accessible to all, but some options require admin
        render_settings_panel()
    
    else:
        # Default to chat
        render_chat_page()


def render_admin_login_link():
    """Renderiza un enlace para que usuarios comunes puedan login como admin."""
    st.markdown("---")
    if st.button("🔐 Iniciar Sesión como Administrador", use_container_width=True):
        # Clear authentication and rerun
        auth_service = get_authentication_service()
        auth_service.logout()
        st.rerun()


def render_knowledge_page():
    """
    Renderiza la página de gestión de la biblioteca de conocimiento.
    
    Solo accesible para administradores. Guests deben usar el chat.
    """
    # Version marker for debugging
    # st.caption("🔍 DEBUG: Version 2024-07-27-v3")  # Descomentar para debug
    
    # Check if user is admin
    from src.config import SessionKey
    is_admin = st.session_state.get(SessionKey.IS_ADMIN, False)
    
    st.title("📚 Biblioteca de Conocimiento")
    
    if not is_admin:
        # Guest view: Limited to statistics only
        st.caption("Estadísticas de la biblioteca")
        st.divider()
        
        st.warning("🔒 **Acceso Restringido:** La gestión de documentos requiere permisos de administrador.")
        st.info("💡 **Como usuario invitado, puedes:**\n- Consultar documentos usando el 💬 Chat\n- Ver estadísticas de la biblioteca abajo")
        
        st.divider()
        
        # Show basic statistics only
        from src.services import get_knowledge_library_service
        kl_service = get_knowledge_library_service()
        stats = kl_service.get_storage_stats()
        
        st.markdown("### 📊 Estadísticas de la Biblioteca")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Documentos", stats['total_documents'])
        with col2:
            st.metric("Documentos Indexados", stats['indexed_documents'])
        with col3:
            st.metric("Tamaño Total", f"{stats['total_size'] / (1024*1024):.1f} MB")
        
        st.divider()
        
        # Show login option
        st.markdown("### 🔐 ¿Necesitas gestionar documentos?")
        if st.button("Iniciar Sesión como Administrador", type="primary", use_container_width=True):
            st.session_state['force_login'] = True
            st.session_state[SessionKey.GUEST_MODE] = False
            st.rerun()
    else:
        # Admin view: Full access
        st.caption("Administra tu colección de documentos")
        st.divider()
        
        # Use the documents tab from admin panel with unique key
        render_documents_tab(key_prefix="knowledge")


def initialize_session_state():
    """
    Inicializa las variables de estado de sesión.
    """
    # Initialize SessionManager first
    from src.auth import get_session_manager
    session_manager = get_session_manager()
    session_manager.initialize_session()
    
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_page = 'Chat'
        logger.debug("Session state initialized")


# Entry point
if __name__ == "__main__":
    try:
        initialize_session_state()
        main()
    except Exception as e:
        logger.error(f"Application error", error=str(e), exc_info=True)
        st.error(f"❌ Ocurrió un error: {str(e)}")
        st.info("Por favor revisa los logs para más detalles")
