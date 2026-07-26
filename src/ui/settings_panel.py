"""
Settings Panel Module

This module implements the settings interface.
Allows configuration of LLM, RAG, and UI settings.

Author: TechFlow AI Project
License: MIT
"""

import streamlit as st

from src.services import get_configuration_service
from src.ui.components import (
    render_header,
    render_select_box,
    render_text_input,
    render_slider,
    render_number_input,
    render_button,
    render_info_message,
    render_tabs,
    render_expander
)
from src.utils import get_logger, ConfigurationError


logger = get_logger()


def render_settings_panel() -> None:
    """
    Render main settings panel page.
    
    Example:
        >>> render_settings_panel()
    """
    render_header("⚙️ Settings", "Configure LLM, RAG, and UI preferences")
    
    # Render tabs
    tabs = render_tabs([
        "🤖 LLM Settings",
        "🔍 RAG Settings",
        "🎨 UI Settings",
        "📋 Configuration"
    ])
    
    with tabs[0]:
        render_llm_settings_tab()
    
    with tabs[1]:
        render_rag_settings_tab()
    
    with tabs[2]:
        render_ui_settings_tab()
    
    with tabs[3]:
        render_configuration_tab()


def render_llm_settings_tab() -> None:
    """
    Render LLM settings configuration tab.
    """
    st.markdown("### 🤖 LLM Configuration")
    
    config_service = get_configuration_service()
    current_config = config_service.get_llm_config()
    
    # Provider selection
    st.markdown("#### Provider")
    
    provider = render_select_box(
        label="LLM Provider",
        options=['gemini', 'cohere'],
        default_index=0 if current_config.get('provider') == 'gemini' else 1,
        help_text="Primary LLM provider (automatic fallback enabled)",
        key="llm_provider_select"
    )
    
    st.info("💡 Fallback: If primary fails, system automatically switches to the other provider")
    
    st.divider()
    
    # Model selection
    st.markdown("#### Model")
    
    if provider == 'gemini':
        model_options = ['gemini-1.5-flash', 'gemini-1.5-pro']
        default_model = current_config.get('model', 'gemini-1.5-flash')
    else:
        model_options = ['command-r', 'command-r-plus']
        default_model = current_config.get('model', 'command-r')
    
    model = render_select_box(
        label="Model",
        options=model_options,
        default_index=model_options.index(default_model) if default_model in model_options else 0,
        help_text=f"Available models for {provider}",
        key="llm_model_select"
    )
    
    st.divider()
    
    # API Key
    st.markdown("#### API Key")
    
    current_key = current_config.get('api_key', '')
    masked_key = f"{'*' * 20}{current_key[-4:]}" if current_key else ""
    
    api_key = render_text_input(
        label="API Key",
        placeholder=masked_key or "Enter your API key",
        help_text="Your LLM provider API key (stored securely)",
        password=True,
        key="llm_api_key_input"
    )
    
    st.caption("⚠️ API keys are stored in local configuration")
    
    st.divider()
    
    # Save button
    if render_button("💾 Save LLM Settings", button_type="primary"):
        save_llm_settings(
            config_service,
            provider,
            model,
            api_key if api_key else None
        )


def save_llm_settings(
    config_service,
    provider: str,
    model: str,
    api_key: str = None
) -> None:
    """
    Save LLM settings.
    
    Args:
        config_service: ConfigurationService instance
        provider: Provider name
        model: Model name
        api_key: API key (optional)
    """
    try:
        success = config_service.update_llm_config(
            provider=provider,
            model=model,
            api_key=api_key
        )
        
        if success:
            render_info_message("✅ LLM settings saved successfully", "success")
            logger.info(f"LLM settings updated", provider=provider, model=model)
            st.rerun()
        else:
            render_info_message("❌ Failed to save LLM settings", "error")
            
    except Exception as e:
        render_info_message(f"❌ Error: {str(e)}", "error")
        logger.error(f"Failed to save LLM settings", error=str(e))


def render_rag_settings_tab() -> None:
    """
    Render RAG settings configuration tab.
    """
    st.markdown("### 🔍 RAG Configuration")
    
    config_service = get_configuration_service()
    current_config = config_service.get_rag_config()
    
    # Chunking settings
    with render_expander("📄 Chunking Settings", expanded=True):
        chunk_size = render_number_input(
            label="Chunk Size",
            min_value=128,
            max_value=2048,
            value=current_config.get('chunk_size', 512),
            step=64,
            help_text="Size of text chunks (128-2048 characters)",
            key="chunk_size_input"
        )
        
        chunk_overlap = render_number_input(
            label="Chunk Overlap",
            min_value=0,
            max_value=512,
            value=current_config.get('chunk_overlap', 50),
            step=10,
            help_text="Overlap between chunks (0-512 characters)",
            key="chunk_overlap_input"
        )
        
        st.caption(f"💡 Effective chunk: {chunk_size} chars with {chunk_overlap} overlap")
    
    st.divider()
    
    # Retrieval settings
    with render_expander("🔍 Retrieval Settings", expanded=True):
        top_k = render_number_input(
            label="Top K",
            min_value=1,
            max_value=20,
            value=current_config.get('top_k', 5),
            step=1,
            help_text="Number of chunks to retrieve (1-20)",
            key="top_k_input"
        )
        
        st.caption(f"💡 Will retrieve {top_k} most relevant chunks per query")
    
    st.divider()
    
    # LLM generation settings
    with render_expander("🤖 Generation Settings", expanded=True):
        temperature = render_slider(
            label="Temperature",
            min_value=0.0,
            max_value=2.0,
            value=float(current_config.get('temperature', 0.7)),
            step=0.1,
            help_text="Creativity level (0.0=focused, 2.0=creative)",
            key="temperature_input"
        )
        
        st.caption(f"💡 Current: {temperature} ({'Focused' if temperature < 0.5 else 'Balanced' if temperature < 1.0 else 'Creative'})")
    
    st.divider()
    
    # Save button
    if render_button("💾 Save RAG Settings", button_type="primary"):
        save_rag_settings(
            config_service,
            chunk_size,
            chunk_overlap,
            top_k,
            temperature
        )


def save_rag_settings(
    config_service,
    chunk_size: int,
    chunk_overlap: int,
    top_k: int,
    temperature: float
) -> None:
    """
    Save RAG settings.
    
    Args:
        config_service: ConfigurationService instance
        chunk_size: Chunk size
        chunk_overlap: Chunk overlap
        top_k: Top K value
        temperature: Temperature value
    """
    try:
        success = config_service.update_rag_config(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            top_k=top_k,
            temperature=temperature
        )
        
        if success:
            render_info_message("✅ RAG settings saved successfully", "success")
            logger.info(f"RAG settings updated")
            st.rerun()
        else:
            render_info_message("❌ Failed to save RAG settings", "error")
            
    except ConfigurationError as e:
        render_info_message(f"❌ Validation error: {str(e)}", "error")
        logger.error(f"RAG settings validation failed", error=str(e))
    
    except Exception as e:
        render_info_message(f"❌ Error: {str(e)}", "error")
        logger.error(f"Failed to save RAG settings", error=str(e))


def render_ui_settings_tab() -> None:
    """
    Render UI settings tab.
    """
    st.markdown("### 🎨 UI Preferences")
    
    config_service = get_configuration_service()
    current_theme = config_service.get_theme()
    
    # Theme selection
    st.markdown("#### Theme")
    
    theme = render_select_box(
        label="Color Theme",
        options=['light', 'dark'],
        default_index=0 if current_theme == 'light' else 1,
        help_text="Application color theme",
        key="theme_select"
    )
    
    st.caption(f"Current theme: {current_theme.title()} {'☀️' if current_theme == 'light' else '🌙'}")
    
    st.divider()
    
    # Save button
    if render_button("💾 Save UI Settings", button_type="primary"):
        save_ui_settings(config_service, theme)


def save_ui_settings(config_service, theme: str) -> None:
    """
    Save UI settings.
    
    Args:
        config_service: ConfigurationService instance
        theme: Theme name
    """
    try:
        success = config_service.set_theme(theme)
        
        if success:
            render_info_message("✅ UI settings saved successfully", "success")
            logger.info(f"UI settings updated", theme=theme)
            st.rerun()
        else:
            render_info_message("❌ Failed to save UI settings", "error")
            
    except Exception as e:
        render_info_message(f"❌ Error: {str(e)}", "error")


def render_configuration_tab() -> None:
    """
    Render configuration management tab.
    """
    st.markdown("### 📋 Configuration Management")
    
    config_service = get_configuration_service()
    
    # Validation
    st.markdown("#### ✅ Validation")
    
    if render_button("🔍 Validate Configuration", use_container_width=True):
        is_valid, errors = config_service.validate_configuration()
        
        if is_valid:
            render_info_message("✅ Configuration is valid", "success")
        else:
            render_info_message("❌ Configuration has errors:", "error")
            for error in errors:
                st.error(f"• {error}")
    
    st.divider()
    
    # Export
    st.markdown("#### 📥 Export Configuration")
    
    st.caption("Export current configuration (API keys will be redacted)")
    
    if render_button("📥 Export Config", use_container_width=True):
        export_configuration(config_service)
    
    st.divider()
    
    # Reset
    st.markdown("#### 🔄 Reset Configuration")
    
    st.warning("⚠️ This will reset all settings to default values")
    
    if render_button("🔄 Reset to Defaults", use_container_width=True):
        reset_configuration(config_service)


def export_configuration(config_service) -> None:
    """
    Export configuration to JSON.
    
    Args:
        config_service: ConfigurationService instance
    """
    import json
    
    config = config_service.export_configuration()
    config_json = json.dumps(config, indent=2)
    
    st.download_button(
        label="💾 Download config.json",
        data=config_json,
        file_name="techflow_config_export.json",
        mime="application/json"
    )
    
    render_info_message("✅ Configuration exported", "success")


def reset_configuration(config_service) -> None:
    """
    Reset configuration to defaults.
    
    Args:
        config_service: ConfigurationService instance
    """
    st.warning("Are you sure? This cannot be undone.")
    
    if st.button("Confirm Reset"):
        try:
            success = config_service.reset_to_defaults()
            
            if success:
                render_info_message("✅ Configuration reset to defaults", "success")
                logger.warning("Configuration reset to defaults")
                st.rerun()
            else:
                render_info_message("❌ Failed to reset configuration", "error")
                
        except Exception as e:
            render_info_message(f"❌ Error: {str(e)}", "error")


# Convenience: Allow direct import
__all__ = [
    'render_settings_panel',
    'render_llm_settings_tab',
    'render_rag_settings_tab',
    'render_ui_settings_tab',
    'render_configuration_tab',
]
