"""
TechFlow Solutions RAG Agent - Aplicación Principal

Este es el punto de entrada principal para la aplicación Streamlit.
Maneja enrutamiento, autenticación y renderizado de páginas.

Autor: TechFlow Solutions Project
Licencia: MIT
"""

import streamlit as st

from src.services import get_authentication_service, get_configuration_service
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
        initial_sidebar_state="expanded"
    )
    
    # Apply theme
    config_service = get_configuration_service()
    theme = load_theme_from_config(config_service)
    apply_theme(theme)
    
    # Hide default Streamlit elements
    hide_streamlit_elements()
    
    # Check authentication
    auth_service = get_authentication_service()
    
    if not auth_service.is_authenticated():
        render_login_page()
    else:
        render_main_app()


def render_login_page():
    """
    Renderiza la página de inicio de sesión para usuarios no autenticados.
    """
    # Compact sidebar for login
    render_compact_sidebar()
    
    # Formulario de login
    st.title("🤖 TechFlow Solutions")
    st.markdown("### Agente de Conocimiento con RAG")
    st.divider()
    
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
        - 🤖 **Soporte Dual de LLM** - Gemini 1.5 Flash + respaldo Cohere
        - ⚙️ **Configurable** - Personaliza RAG y configuración de LLM
        
        ### Stack Tecnológico
        - **LLM:** Google Gemini 1.5 Flash (principal), Cohere Command-R (respaldo)
        - **Embeddings:** Multilingual E5-base (768 dimensiones)
        - **Vector Store:** ChromaDB (persistente)
        - **Framework:** Streamlit
        
        ### Credenciales por Defecto
        - **Usuario:** admin
        - **Contraseña:** Verifica tu archivo `.env` o usa la configuración por defecto
        """)


def render_main_app():
    """
    Renderiza la aplicación principal con navegación.
    """
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to selected page
    if selected_page == "Chat":
        render_chat_page()
    
    elif selected_page == "Knowledge":
        render_knowledge_page()
    
    elif selected_page == "Admin":
        render_admin_panel()
    
    elif selected_page == "Settings":
        render_settings_panel()
    
    else:
        # Default to chat
        render_chat_page()


def render_knowledge_page():
    """
    Renderiza la página de gestión de la biblioteca de conocimiento.
    
    Esta es una vista simplificada enfocada en la gestión de documentos.
    Para características completas de administración, usa el Panel de Administración.
    """
    st.title("📚 Biblioteca de Conocimiento")
    st.caption("Administra tu colección de documentos")
    st.divider()
    
    # Use the documents tab from admin panel
    render_documents_tab()


def initialize_session_state():
    """
    Inicializa las variables de estado de sesión.
    """
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
