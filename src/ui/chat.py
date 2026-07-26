"""
Módulo de Chat

Este módulo implementa la interfaz de chat para interacciones con el usuario.
Maneja la visualización de mensajes, respuestas en streaming e historial de conversación.

Autor: TechFlow AI Project
Licencia: MIT
"""

import streamlit as st
from typing import Generator

from src.services import get_chat_service, get_indexing_service
from src.ui.components import (
    render_header,
    render_text_area,
    render_button,
    render_info_message,
    render_empty_state,
    render_spinner
)
from src.utils import (
    get_logger,
    EmptyKnowledgeLibraryError,
    LLMError
)


logger = get_logger()


def render_chat_page() -> None:
    """
    Renderiza la página principal de chat.
    
    Ejemplo:
        >>> render_chat_page()
    """
    render_header("💬 Chat", "Haz preguntas sobre tu biblioteca de conocimiento")
    
    # Check if knowledge library is ready
    if not is_knowledge_library_ready():
        render_empty_knowledge_library()
        return
    
    # Initialize chat history in session
    initialize_chat_history()
    
    # Display chat messages
    display_chat_messages()
    
    # Chat input and send
    handle_chat_input()


def is_knowledge_library_ready() -> bool:
    """
    Verifica si la biblioteca de conocimiento tiene documentos indexados.
    
    Retorna:
        bool: True si está lista para el chat
    """
    try:
        indexing_service = get_indexing_service()
        stats = indexing_service.get_indexing_stats()
        return stats['indexed_documents'] > 0
    except Exception as e:
        logger.error(f"Failed to check knowledge library status", error=str(e))
        return False


def render_empty_knowledge_library() -> None:
    """
    Renderiza estado vacío cuando no hay documentos indexados.
    """
    render_empty_state(
        icon="📚",
        title="La Biblioteca de Conocimiento está Vacía",
        message="Sube e indexa documentos para comenzar a chatear",
        action_label="Ir a Biblioteca de Conocimiento",
        action_callback=lambda: st.session_state.update({'current_page': 'Knowledge'})
    )


def initialize_chat_history() -> None:
    """
    Inicializa el historial de chat en el estado de sesión.
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        logger.debug("Chat history initialized")


def display_chat_messages() -> None:
    """
    Muestra todos los mensajes de chat del historial.
    """
    for message in st.session_state.chat_history:
        role = message['role']
        content = message['content']
        
        with st.chat_message(role):
            st.markdown(content)


def handle_chat_input() -> None:
    """
    Maneja la entrada de chat y la generación de respuestas.
    """
    # Chat input
    user_input = st.chat_input("Haz una pregunta sobre tus documentos...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Display user message
        with st.chat_message('user'):
            st.markdown(user_input)
        
        # Generate and display assistant response
        with st.chat_message('assistant'):
            response_placeholder = st.empty()
            
            try:
                # Get streaming response
                full_response = generate_streaming_response(
                    user_input,
                    response_placeholder
                )
                
                # Add assistant response to history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': full_response
                })
                
                logger.info(
                    f"Chat interaction completed",
                    user_input_length=len(user_input),
                    response_length=len(full_response)
                )
                
            except EmptyKnowledgeLibraryError:
                error_msg = "⚠️ La biblioteca de conocimiento está vacía. Por favor sube documentos primero."
                response_placeholder.error(error_msg)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_msg
                })
            
            except LLMError as e:
                error_msg = f"❌ Error de LLM: {str(e)}"
                response_placeholder.error(error_msg)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_msg
                })
                logger.error(f"LLM error in chat", error=str(e))
            
            except Exception as e:
                error_msg = f"❌ Ocurrió un error: {str(e)}"
                response_placeholder.error(error_msg)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_msg
                })
                logger.error(f"Unexpected error in chat", error=str(e), exc_info=True)


def generate_streaming_response(
    user_input: str,
    placeholder
) -> str:
    """
    Genera respuesta en streaming desde el servicio de chat.
    
    Args:
        user_input: Consulta del usuario
        placeholder: Placeholder de Streamlit para la respuesta
    
    Retorna:
        str: Texto completo de la respuesta
    """
    chat_service = get_chat_service()
    
    # Get conversation history (exclude system messages)
    conversation_history = [
        msg for msg in st.session_state.chat_history[:-1]  # Exclude current user message
        if msg['role'] in ['user', 'assistant']
    ]
    
    # Generate streaming response
    full_response = ""
    
    try:
        response_stream = chat_service.chat(
            query=user_input,
            conversation_history=conversation_history if conversation_history else None,
            stream=True
        )
        
        for chunk in response_stream:
            full_response += chunk
            placeholder.markdown(full_response + "▌")
        
        # Final display without cursor
        placeholder.markdown(full_response)
        
    except Exception as e:
        logger.error(f"Streaming response failed", error=str(e))
        raise
    
    return full_response


def render_chat_controls() -> None:
    """
    Renderiza botones de control de chat (limpiar, exportar, etc.).
    """
    with st.sidebar:
        st.markdown("### 💬 Controles de Chat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Limpiar", use_container_width=True, key="clear_chat"):
                clear_chat_history()
        
        with col2:
            if st.button("💾 Exportar", use_container_width=True, key="export_chat"):
                export_chat_history()
        
        # Chat statistics
        if st.session_state.get('chat_history'):
            message_count = len(st.session_state.chat_history)
            st.caption(f"Mensajes: {message_count}")


def clear_chat_history() -> None:
    """
    Limpia el historial de chat.
    """
    st.session_state.chat_history = []
    logger.info("Chat history cleared")
    st.rerun()


def export_chat_history() -> None:
    """
    Exporta el historial de chat a un archivo de texto.
    """
    if not st.session_state.get('chat_history'):
        st.warning("No hay historial de chat para exportar")
        return
    
    # Format chat history as text
    export_text = "# TechFlow AI - Exportación de Chat\n\n"
    
    for message in st.session_state.chat_history:
        role = message['role'].upper()
        content = message['content']
        export_text += f"## {role}\n{content}\n\n"
    
    # Create download button
    st.download_button(
        label="📥 Descargar Chat",
        data=export_text,
        file_name="techflow_chat_export.txt",
        mime="text/plain",
        key="download_chat"
    )
    
    logger.info("Chat history exported")


def render_chat_with_controls() -> None:
    """
    Renderiza página de chat con controles en la barra lateral.
    
    Interfaz completa de chat con controles.
    
    Ejemplo:
        >>> render_chat_with_controls()
    """
    # Render controls in sidebar
    render_chat_controls()
    
    # Render main chat interface
    render_chat_page()


def get_chat_statistics() -> dict:
    """
    Obtiene estadísticas del chat.
    
    Retorna:
        dict: Estadísticas del chat
    """
    history = st.session_state.get('chat_history', [])
    
    user_messages = [m for m in history if m['role'] == 'user']
    assistant_messages = [m for m in history if m['role'] == 'assistant']
    
    return {
        'total_messages': len(history),
        'user_messages': len(user_messages),
        'assistant_messages': len(assistant_messages),
        'has_history': len(history) > 0
    }


def render_chat_info_panel() -> None:
    """
    Renderiza panel de información del chat.
    
    Muestra estado de RAG y capacidades del chat.
    """
    with st.expander("ℹ️ Acerca de este Chat", expanded=False):
        st.markdown("""
        ### Cómo funciona
        
        1. **Haz una pregunta** sobre tus documentos subidos
        2. **Pipeline RAG** recupera el contexto relevante
        3. **IA responde** basándose en tu biblioteca de conocimiento
        
        ### Características
        - 🔍 Respuestas contextuales
        - 📚 Búsqueda en múltiples documentos
        - 💬 Historial de conversación
        - ⚡ Respuestas en streaming
        
        ### Consejos
        - Sé específico en tus preguntas
        - Referencias nombres de documentos si es necesario
        - Usa lenguaje claro y conciso
        """)
        
        # Display current RAG stats
        chat_service = get_chat_service()
        stats = chat_service.get_chat_stats()
        
        st.markdown("### Configuración Actual")
        st.text(f"Proveedor: {stats['primary_provider']}")
        st.text(f"Temperatura: {stats['temperature']}")
        st.text(f"Top-K: {stats['top_k']}")
        st.text(f"Vector Store: {stats['vector_store_count']} fragmentos")


# Convenience: Allow direct import
__all__ = [
    'render_chat_page',
    'render_chat_with_controls',
    'render_chat_controls',
    'render_chat_info_panel',
    'clear_chat_history',
    'export_chat_history',
    'get_chat_statistics',
]
