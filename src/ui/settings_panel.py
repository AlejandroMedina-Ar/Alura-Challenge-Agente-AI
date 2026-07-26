"""
Módulo de Panel de Configuración

Este módulo implementa la interfaz de configuración.
Permite configuración de LLM, RAG y ajustes de UI.

Autor: TechFlow Solutions Project
Licencia: MIT
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
    Renderiza la página principal del panel de configuración.
    
    Ejemplo:
        >>> render_settings_panel()
    """
    render_header("⚙️ Configuración", "Configura LLM, RAG y preferencias de UI")
    
    # Render tabs
    tabs = render_tabs([
        "🤖 Configuración LLM",
        "🔍 Configuración RAG",
        "🎨 Configuración UI",
        "📋 Configuración"
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
    Renderiza la pestaña de configuración de LLM.
    """
    st.markdown("### 🤖 Configuración de LLM")
    
    config_service = get_configuration_service()
    current_config = config_service.get_llm_config()
    
    # Provider selection
    st.markdown("#### Proveedor")
    
    provider = render_select_box(
        label="Proveedor de LLM",
        options=['gemini', 'cohere'],
        default_index=0 if current_config.get('provider') == 'gemini' else 1,
        help_text="Proveedor de LLM primario (respaldo automático habilitado)",
        key="llm_provider_select"
    )
    
    st.info("💡 Respaldo: Si el primario falla, el sistema cambia automáticamente al otro proveedor")
    
    st.divider()
    
    # Model selection
    st.markdown("#### Modelo")
    
    if provider == 'gemini':
        model_options = ['gemini-1.5-flash', 'gemini-1.5-pro']
        default_model = current_config.get('model', 'gemini-1.5-flash')
    else:
        model_options = ['command-r', 'command-r-plus']
        default_model = current_config.get('model', 'command-r')
    
    model = render_select_box(
        label="Modelo",
        options=model_options,
        default_index=model_options.index(default_model) if default_model in model_options else 0,
        help_text=f"Modelos disponibles para {provider}",
        key="llm_model_select"
    )
    
    st.divider()
    
    # API Key
    st.markdown("#### Clave API")
    
    current_key = current_config.get('api_key', '')
    masked_key = f"{'*' * 20}{current_key[-4:]}" if current_key else ""
    
    api_key = render_text_input(
        label="Clave API",
        placeholder=masked_key or "Ingresa tu clave API",
        help_text="Tu clave API del proveedor LLM (almacenada de forma segura)",
        password=True,
        key="llm_api_key_input"
    )
    
    st.caption("⚠️ Las claves API se almacenan en la configuración local")
    
    st.divider()
    
    # Save button
    if render_button("💾 Guardar Configuración LLM", button_type="primary"):
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
    Guarda la configuración de LLM.
    
    Args:
        config_service: Instancia de ConfigurationService
        provider: Nombre del proveedor
        model: Nombre del modelo
        api_key: Clave API (opcional)
    """
    try:
        success = config_service.update_llm_config(
            provider=provider,
            model=model,
            api_key=api_key
        )
        
        if success:
            render_info_message("✅ Configuración LLM guardada exitosamente", "success")
            logger.info(f"LLM settings updated", provider=provider, model=model)
            st.rerun()
        else:
            render_info_message("❌ Fallo al guardar configuración LLM", "error")
            
    except Exception as e:
        render_info_message(f"❌ Error: {str(e)}", "error")
        logger.error(f"Failed to save LLM settings", error=str(e))


def render_rag_settings_tab() -> None:
    """
    Renderiza la pestaña de configuración de RAG.
    """
    st.markdown("### 🔍 Configuración de RAG")
    
    config_service = get_configuration_service()
    current_config = config_service.get_rag_config()
    
    # Chunking settings
    with render_expander("📄 Configuración de Fragmentación", expanded=True):
        chunk_size = render_number_input(
            label="Tamaño de Fragmento",
            min_value=128,
            max_value=2048,
            value=current_config.get('chunk_size', 512),
            step=64,
            help_text="Tamaño de los fragmentos de texto (128-2048 caracteres)",
            key="chunk_size_input"
        )
        
        chunk_overlap = render_number_input(
            label="Superposición de Fragmentos",
            min_value=0,
            max_value=512,
            value=current_config.get('chunk_overlap', 50),
            step=10,
            help_text="Superposición entre fragmentos (0-512 caracteres)",
            key="chunk_overlap_input"
        )
        
        st.caption(f"💡 Fragmento efectivo: {chunk_size} caracteres con {chunk_overlap} de superposición")
    
    st.divider()
    
    # Retrieval settings
    with render_expander("🔍 Configuración de Recuperación", expanded=True):
        top_k = render_number_input(
            label="Top K",
            min_value=1,
            max_value=20,
            value=current_config.get('top_k', 5),
            step=1,
            help_text="Número de fragmentos a recuperar (1-20)",
            key="top_k_input"
        )
        
        st.caption(f"💡 Recuperará los {top_k} fragmentos más relevantes por consulta")
    
    st.divider()
    
    # LLM generation settings
    with render_expander("🤖 Configuración de Generación", expanded=True):
        temperature = render_slider(
            label="Temperatura",
            min_value=0.0,
            max_value=2.0,
            value=float(current_config.get('temperature', 0.7)),
            step=0.1,
            help_text="Nivel de creatividad (0.0=enfocado, 2.0=creativo)",
            key="temperature_input"
        )
        
        st.caption(f"💡 Actual: {temperature} ({'Enfocado' if temperature < 0.5 else 'Equilibrado' if temperature < 1.0 else 'Creativo'})")
    
    st.divider()
    
    # Save button
    if render_button("💾 Guardar Configuración RAG", button_type="primary"):
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
    Guarda la configuración de RAG.
    
    Args:
        config_service: Instancia de ConfigurationService
        chunk_size: Tamaño del fragmento
        chunk_overlap: Superposición del fragmento
        top_k: Valor Top K
        temperature: Valor de temperatura
    """
    try:
        success = config_service.update_rag_config(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            top_k=top_k,
            temperature=temperature
        )
        
        if success:
            render_info_message("✅ Configuración RAG guardada exitosamente", "success")
            logger.info(f"RAG settings updated")
            st.rerun()
        else:
            render_info_message("❌ Fallo al guardar configuración RAG", "error")
            
    except ConfigurationError as e:
        render_info_message(f"❌ Error de validación: {str(e)}", "error")
        logger.error(f"RAG settings validation failed", error=str(e))
    
    except Exception as e:
        render_info_message(f"❌ Error: {str(e)}", "error")
        logger.error(f"Failed to save RAG settings", error=str(e))


def render_ui_settings_tab() -> None:
    """
    Renderiza la pestaña de configuración de UI.
    """
    st.markdown("### 🎨 Preferencias de UI")
    
    config_service = get_configuration_service()
    current_theme = config_service.get_theme()
    
    # Theme selection
    st.markdown("#### Tema")
    
    theme = render_select_box(
        label="Tema de Color",
        options=['light', 'dark'],
        default_index=0 if current_theme == 'light' else 1,
        help_text="Tema de color de la aplicación",
        key="theme_select"
    )
    
    st.caption(f"Tema actual: {current_theme.title()} {'☀️' if current_theme == 'light' else '🌙'}")
    
    st.divider()
    
    # Save button
    if render_button("💾 Guardar Configuración UI", button_type="primary"):
        save_ui_settings(config_service, theme)


def save_ui_settings(config_service, theme: str) -> None:
    """
    Guarda la configuración de UI.
    
    Args:
        config_service: Instancia de ConfigurationService
        theme: Nombre del tema
    """
    try:
        success = config_service.set_theme(theme)
        
        if success:
            render_info_message("✅ Configuración UI guardada exitosamente", "success")
            logger.info(f"UI settings updated", theme=theme)
            st.rerun()
        else:
            render_info_message("❌ Fallo al guardar configuración UI", "error")
            
    except Exception as e:
        render_info_message(f"❌ Error: {str(e)}", "error")


def render_configuration_tab() -> None:
    """
    Renderiza la pestaña de gestión de configuración.
    """
    st.markdown("### 📋 Gestión de Configuración")
    
    config_service = get_configuration_service()
    
    # Validation
    st.markdown("#### ✅ Validación")
    
    if render_button("🔍 Validar Configuración", use_container_width=True):
        is_valid, errors = config_service.validate_configuration()
        
        if is_valid:
            render_info_message("✅ La configuración es válida", "success")
        else:
            render_info_message("❌ La configuración tiene errores:", "error")
            for error in errors:
                st.error(f"• {error}")
    
    st.divider()
    
    # Export
    st.markdown("#### 📥 Exportar Configuración")
    
    st.caption("Exportar configuración actual (las claves API serán censuradas)")
    
    if render_button("📥 Exportar Config", use_container_width=True):
        export_configuration(config_service)
    
    st.divider()
    
    # Reset
    st.markdown("#### 🔄 Restablecer Configuración")
    
    st.warning("⚠️ Esto restablecerá todos los ajustes a sus valores predeterminados")
    
    if render_button("🔄 Restablecer a Predeterminados", use_container_width=True):
        reset_configuration(config_service)


def export_configuration(config_service) -> None:
    """
    Exporta la configuración a JSON.
    
    Args:
        config_service: Instancia de ConfigurationService
    """
    import json
    
    config = config_service.export_configuration()
    config_json = json.dumps(config, indent=2)
    
    st.download_button(
        label="💾 Descargar config.json",
        data=config_json,
        file_name="techflow_config_export.json",
        mime="application/json"
    )
    
    render_info_message("✅ Configuración exportada", "success")


def reset_configuration(config_service) -> None:
    """
    Restablece la configuración a valores predeterminados.
    
    Args:
        config_service: Instancia de ConfigurationService
    """
    st.warning("¿Estás seguro? Esto no se puede deshacer.")
    
    if st.button("Confirmar Restablecimiento"):
        try:
            success = config_service.reset_to_defaults()
            
            if success:
                render_info_message("✅ Configuración restablecida a valores predeterminados", "success")
                logger.warning("Configuration reset to defaults")
                st.rerun()
            else:
                render_info_message("❌ Fallo al restablecer configuración", "error")
                
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
