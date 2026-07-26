"""
Chat Module

This module implements the chat interface for user interactions.
Handles message display, streaming responses, and conversation history.

Author: TechFlow AI Project
License: MIT
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
    Render main chat page.
    
    Example:
        >>> render_chat_page()
    """
    render_header("💬 Chat", "Ask questions about your knowledge library")
    
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
    Check if knowledge library has indexed documents.
    
    Returns:
        bool: True if ready for chat
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
    Render empty state when no documents are indexed.
    """
    render_empty_state(
        icon="📚",
        title="Knowledge Library is Empty",
        message="Upload and index documents to start chatting",
        action_label="Go to Knowledge Library",
        action_callback=lambda: st.session_state.update({'current_page': 'Knowledge'})
    )


def initialize_chat_history() -> None:
    """
    Initialize chat history in session state.
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        logger.debug("Chat history initialized")


def display_chat_messages() -> None:
    """
    Display all chat messages from history.
    """
    for message in st.session_state.chat_history:
        role = message['role']
        content = message['content']
        
        with st.chat_message(role):
            st.markdown(content)


def handle_chat_input() -> None:
    """
    Handle chat input and response generation.
    """
    # Chat input
    user_input = st.chat_input("Ask a question about your documents...")
    
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
                error_msg = "⚠️ Knowledge library is empty. Please upload documents first."
                response_placeholder.error(error_msg)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_msg
                })
            
            except LLMError as e:
                error_msg = f"❌ LLM Error: {str(e)}"
                response_placeholder.error(error_msg)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_msg
                })
                logger.error(f"LLM error in chat", error=str(e))
            
            except Exception as e:
                error_msg = f"❌ An error occurred: {str(e)}"
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
    Generate streaming response from chat service.
    
    Args:
        user_input: User query
        placeholder: Streamlit placeholder for response
    
    Returns:
        str: Complete response text
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
    Render chat control buttons (clear, export, etc.).
    """
    with st.sidebar:
        st.markdown("### 💬 Chat Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
                clear_chat_history()
        
        with col2:
            if st.button("💾 Export", use_container_width=True, key="export_chat"):
                export_chat_history()
        
        # Chat statistics
        if st.session_state.get('chat_history'):
            message_count = len(st.session_state.chat_history)
            st.caption(f"Messages: {message_count}")


def clear_chat_history() -> None:
    """
    Clear chat history.
    """
    st.session_state.chat_history = []
    logger.info("Chat history cleared")
    st.rerun()


def export_chat_history() -> None:
    """
    Export chat history to text file.
    """
    if not st.session_state.get('chat_history'):
        st.warning("No chat history to export")
        return
    
    # Format chat history as text
    export_text = "# TechFlow AI - Chat Export\n\n"
    
    for message in st.session_state.chat_history:
        role = message['role'].upper()
        content = message['content']
        export_text += f"## {role}\n{content}\n\n"
    
    # Create download button
    st.download_button(
        label="📥 Download Chat",
        data=export_text,
        file_name="techflow_chat_export.txt",
        mime="text/plain",
        key="download_chat"
    )
    
    logger.info("Chat history exported")


def render_chat_with_controls() -> None:
    """
    Render chat page with sidebar controls.
    
    Complete chat interface with controls.
    
    Example:
        >>> render_chat_with_controls()
    """
    # Render controls in sidebar
    render_chat_controls()
    
    # Render main chat interface
    render_chat_page()


def get_chat_statistics() -> dict:
    """
    Get chat statistics.
    
    Returns:
        dict: Chat statistics
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
    Render chat information panel.
    
    Shows RAG status and chat capabilities.
    """
    with st.expander("ℹ️ About this Chat", expanded=False):
        st.markdown("""
        ### How it works
        
        1. **Ask a question** about your uploaded documents
        2. **RAG Pipeline** retrieves relevant context
        3. **AI responds** based on your knowledge library
        
        ### Features
        - 🔍 Context-aware responses
        - 📚 Multi-document search
        - 💬 Conversation history
        - ⚡ Streaming responses
        
        ### Tips
        - Be specific in your questions
        - Reference document names if needed
        - Use clear, concise language
        """)
        
        # Display current RAG stats
        chat_service = get_chat_service()
        stats = chat_service.get_chat_stats()
        
        st.markdown("### Current Configuration")
        st.text(f"Provider: {stats['primary_provider']}")
        st.text(f"Temperature: {stats['temperature']}")
        st.text(f"Top-K: {stats['top_k']}")
        st.text(f"Vector Store: {stats['vector_store_count']} chunks")


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
