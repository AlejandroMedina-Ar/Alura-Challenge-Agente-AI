"""
TechFlow AI RAG Agent - Main Application

This is the main entry point for the Streamlit application.
Handles routing, authentication, and page rendering.

Author: TechFlow AI Project
License: MIT
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
    Main application entry point.
    
    Handles:
    - Page configuration
    - Theme application
    - Authentication
    - Page routing
    """
    # Configure page
    st.set_page_config(
        page_title="TechFlow AI - RAG Agent",
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
    Render login page for unauthenticated users.
    """
    # Compact sidebar for login
    render_compact_sidebar()
    
    # Login form
    st.title("🤖 TechFlow AI")
    st.markdown("### RAG-Powered Knowledge Agent")
    st.divider()
    
    st.markdown("#### 🔐 Admin Login")
    
    with st.form("login_form"):
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter admin password"
        )
        
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submit:
            if password:
                try:
                    auth_service = get_authentication_service()
                    auth_service.login(password)
                    st.success("✅ Login successful!")
                    logger.info("User logged in via web interface")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Login failed: {str(e)}")
                    logger.warning("Login attempt failed")
            else:
                st.warning("⚠️ Please enter a password")
    
    st.divider()
    
    # Info section
    with st.expander("ℹ️ About TechFlow AI"):
        st.markdown("""
        ### Features
        - 🔍 **RAG-Powered Chat** - Context-aware responses from your documents
        - 📚 **Knowledge Library** - Upload and manage documents
        - ⚡ **Smart Indexing** - Automatic chunking and embedding
        - 🤖 **Dual LLM Support** - Gemini 1.5 Flash + Cohere fallback
        - ⚙️ **Configurable** - Customize RAG and LLM settings
        
        ### Technology Stack
        - **LLM:** Google Gemini 1.5 Flash (primary), Cohere Command-R (fallback)
        - **Embeddings:** Multilingual E5-base (768 dimensions)
        - **Vector Store:** ChromaDB (persistent)
        - **Framework:** Streamlit
        
        ### Default Credentials
        - **Username:** admin
        - **Password:** Check your `.env` file or use default setup
        """)


def render_main_app():
    """
    Render main application with navigation.
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
    Render knowledge library management page.
    
    This is a simplified view focusing on document management.
    For full admin features, use the Admin Panel.
    """
    st.title("📚 Knowledge Library")
    st.caption("Manage your document collection")
    st.divider()
    
    # Use the documents tab from admin panel
    render_documents_tab()


def initialize_session_state():
    """
    Initialize session state variables.
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
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please check the logs for details")
