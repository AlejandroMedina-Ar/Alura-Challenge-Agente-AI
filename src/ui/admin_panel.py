"""
Admin Panel Module

This module implements the admin panel interface.
Provides document management, indexing controls, and system statistics.

Author: TechFlow AI Project
License: MIT
"""

import streamlit as st
from datetime import datetime

from src.services import (
    get_knowledge_library_service,
    get_indexing_service,
    get_chat_service
)
from src.ui.components import (
    render_header,
    render_metric_card,
    render_file_uploader,
    render_button,
    render_info_message,
    render_empty_state,
    render_spinner,
    render_columns,
    render_tabs,
    render_data_table
)
from src.utils import (
    get_logger,
    DocumentAlreadyExistsError,
    InvalidDocumentError
)


logger = get_logger()


def render_admin_panel() -> None:
    """
    Render main admin panel page.
    
    Example:
        >>> render_admin_panel()
    """
    render_header("🔧 Admin Panel", "Manage documents and view system stats")
    
    # Render tabs
    tabs = render_tabs([
        "📊 Dashboard",
        "📚 Documents",
        "⚡ Indexing",
        "🧪 Testing"
    ])
    
    with tabs[0]:
        render_dashboard_tab()
    
    with tabs[1]:
        render_documents_tab()
    
    with tabs[2]:
        render_indexing_tab()
    
    with tabs[3]:
        render_testing_tab()


def render_dashboard_tab() -> None:
    """
    Render dashboard with system statistics.
    """
    st.markdown("### 📊 System Overview")
    
    kl_service = get_knowledge_library_service()
    indexing_service = get_indexing_service()
    chat_service = get_chat_service()
    
    # Get statistics
    storage_stats = kl_service.get_storage_stats()
    indexing_stats = indexing_service.get_indexing_stats()
    chat_stats = chat_service.get_chat_stats()
    
    # Metrics row 1
    cols = render_columns(4)
    
    with cols[0]:
        render_metric_card(
            label="Total Documents",
            value=str(storage_stats['total_documents']),
            help_text="Total uploaded documents"
        )
    
    with cols[1]:
        render_metric_card(
            label="Indexed Documents",
            value=str(storage_stats['indexed_documents']),
            help_text="Documents indexed and ready"
        )
    
    with cols[2]:
        render_metric_card(
            label="Total Chunks",
            value=str(indexing_stats['total_chunks']),
            help_text="Total indexed chunks"
        )
    
    with cols[3]:
        render_metric_card(
            label="Storage Used",
            value=f"{storage_stats['total_size_mb']:.2f} MB",
            help_text="Total storage used"
        )
    
    st.divider()
    
    # System status
    st.markdown("### ⚙️ System Status")
    
    cols = render_columns(2)
    
    with cols[0]:
        st.markdown("**RAG Pipeline**")
        if chat_stats['rag_ready']:
            st.success("✅ Ready")
        else:
            st.warning("⚠️ No documents indexed")
        
        st.caption(f"Vector Store: {chat_stats['vector_store_count']} chunks")
        st.caption(f"Embedding Dim: {indexing_stats['embedding_dimension']}")
    
    with cols[1]:
        st.markdown("**LLM Configuration**")
        st.info(f"🤖 Provider: {chat_stats['primary_provider'].title()}")
        st.caption(f"Temperature: {chat_stats['temperature']}")
        st.caption(f"Top-K: {chat_stats['top_k']}")


def render_documents_tab() -> None:
    """
    Render documents management tab.
    """
    st.markdown("### 📚 Document Management")
    
    kl_service = get_knowledge_library_service()
    
    # Upload section
    st.markdown("#### ⬆️ Upload Document")
    
    uploaded_file = render_file_uploader(
        label="Choose a document",
        accepted_types=['txt', 'pdf', 'md', 'docx'],
        help_text="Supported: TXT, PDF, MD, DOCX (Max 10MB)",
        key="admin_file_upload"
    )
    
    if uploaded_file:
        handle_file_upload(uploaded_file, kl_service)
    
    st.divider()
    
    # Documents list
    st.markdown("#### 📄 Uploaded Documents")
    
    documents = kl_service.list_documents()
    
    if not documents:
        render_empty_state(
            icon="📄",
            title="No Documents",
            message="Upload your first document to get started"
        )
    else:
        render_documents_table(documents, kl_service)


def handle_file_upload(uploaded_file, kl_service) -> None:
    """
    Handle file upload process.
    
    Args:
        uploaded_file: Streamlit uploaded file
        kl_service: KnowledgeLibraryService instance
    """
    filename = uploaded_file.name
    file_size = uploaded_file.size
    file_type = uploaded_file.type
    
    # Check if exists
    if kl_service.document_exists(filename):
        render_info_message(
            f"Document '{filename}' already exists",
            "warning"
        )
        return
    
    # Upload
    with render_spinner(f"Uploading {filename}..."):
        try:
            # Save uploaded file temporarily
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Upload to knowledge library
            metadata = kl_service.upload_document(
                file_path=tmp_path,
                filename=filename,
                file_type=file_type,
                file_size=file_size
            )
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            render_info_message(
                f"✅ Document '{filename}' uploaded successfully!",
                "success"
            )
            
            logger.info(f"Document uploaded via admin panel", filename=filename)
            
            st.rerun()
            
        except DocumentAlreadyExistsError:
            render_info_message(
                f"Document '{filename}' already exists",
                "warning"
            )
        
        except InvalidDocumentError as e:
            render_info_message(
                f"❌ Invalid document: {str(e)}",
                "error"
            )
        
        except Exception as e:
            render_info_message(
                f"❌ Upload failed: {str(e)}",
                "error"
            )
            logger.error(f"Upload failed", filename=filename, error=str(e))


def render_documents_table(documents: list[dict], kl_service) -> None:
    """
    Render documents table with actions.
    
    Args:
        documents: List of document metadata
        kl_service: KnowledgeLibraryService instance
    """
    for doc in documents:
        doc_id = doc['doc_id']
        filename = doc['filename']
        file_size = doc['file_size']
        indexed = doc.get('indexed', False)
        chunk_count = doc.get('chunk_count', 0)
        upload_date = doc.get('upload_date', 'Unknown')
        
        # Document card
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**📄 {filename}**")
                st.caption(f"Size: {file_size / 1024:.1f} KB | Uploaded: {upload_date}")
                
                if indexed:
                    st.success(f"✅ Indexed ({chunk_count} chunks)")
                else:
                    st.warning("⚠️ Not indexed")
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{doc_id}"):
                    handle_document_delete(doc_id, filename, kl_service)
            
            with col3:
                if not indexed:
                    if st.button("⚡ Index", key=f"index_{doc_id}"):
                        handle_document_index(doc_id, filename)
                else:
                    if st.button("🔄 Re-index", key=f"reindex_{doc_id}"):
                        handle_document_reindex(doc_id, filename)
            
            st.divider()


def handle_document_delete(doc_id: str, filename: str, kl_service) -> None:
    """
    Handle document deletion.
    
    Args:
        doc_id: Document ID
        filename: Document filename
        kl_service: KnowledgeLibraryService instance
    """
    with render_spinner(f"Deleting {filename}..."):
        try:
            # Remove from index first
            indexing_service = get_indexing_service()
            indexing_service.remove_document_from_index(doc_id)
            
            # Delete document
            kl_service.delete_document(doc_id)
            
            render_info_message(
                f"✅ Document '{filename}' deleted successfully",
                "success"
            )
            
            logger.info(f"Document deleted", filename=filename)
            
            st.rerun()
            
        except Exception as e:
            render_info_message(
                f"❌ Delete failed: {str(e)}",
                "error"
            )
            logger.error(f"Delete failed", filename=filename, error=str(e))


def handle_document_index(doc_id: str, filename: str) -> None:
    """
    Handle document indexing.
    
    Args:
        doc_id: Document ID
        filename: Document filename
    """
    with render_spinner(f"Indexing {filename}..."):
        try:
            indexing_service = get_indexing_service()
            result = indexing_service.index_document(doc_id, filename)
            
            render_info_message(
                f"✅ Indexed {result['chunk_count']} chunks from '{filename}'",
                "success"
            )
            
            logger.info(f"Document indexed", filename=filename, chunks=result['chunk_count'])
            
            st.rerun()
            
        except Exception as e:
            render_info_message(
                f"❌ Indexing failed: {str(e)}",
                "error"
            )
            logger.error(f"Indexing failed", filename=filename, error=str(e))


def handle_document_reindex(doc_id: str, filename: str) -> None:
    """
    Handle document re-indexing.
    
    Args:
        doc_id: Document ID
        filename: Document filename
    """
    with render_spinner(f"Re-indexing {filename}..."):
        try:
            indexing_service = get_indexing_service()
            result = indexing_service.reindex_document(doc_id, filename)
            
            render_info_message(
                f"✅ Re-indexed {result['chunk_count']} chunks from '{filename}'",
                "success"
            )
            
            logger.info(f"Document re-indexed", filename=filename)
            
            st.rerun()
            
        except Exception as e:
            render_info_message(
                f"❌ Re-indexing failed: {str(e)}",
                "error"
            )


def render_indexing_tab() -> None:
    """
    Render indexing operations tab.
    """
    st.markdown("### ⚡ Indexing Operations")
    
    indexing_service = get_indexing_service()
    
    # Indexing statistics
    stats = indexing_service.get_indexing_stats()
    
    cols = render_columns(3)
    
    with cols[0]:
        st.metric("Indexed", stats['indexed_documents'])
    
    with cols[1]:
        st.metric("Pending", stats['pending_documents'])
    
    with cols[2]:
        st.metric("Total Chunks", stats['total_chunks'])
    
    st.divider()
    
    # Batch operations
    st.markdown("#### 🔄 Batch Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚡ Index All Pending", type="primary", use_container_width=True):
            handle_batch_index_all()
    
    with col2:
        if st.button("🗑️ Clear All Indexes", use_container_width=True):
            handle_clear_all_indexes()
    
    st.divider()
    
    # Pending documents
    pending = indexing_service.get_pending_documents()
    
    if pending:
        st.markdown(f"#### ⏳ Pending Documents ({len(pending)})")
        
        for doc in pending:
            st.text(f"📄 {doc['filename']}")
    else:
        st.success("✅ All documents are indexed")


def handle_batch_index_all() -> None:
    """
    Handle batch indexing of all pending documents.
    """
    indexing_service = get_indexing_service()
    pending = indexing_service.get_pending_documents()
    
    if not pending:
        render_info_message("No pending documents to index", "info")
        return
    
    with render_spinner(f"Indexing {len(pending)} documents..."):
        try:
            docs_to_index = [
                {'doc_id': doc['doc_id'], 'filename': doc['filename']}
                for doc in pending
            ]
            
            result = indexing_service.batch_index_documents(docs_to_index)
            
            render_info_message(
                f"✅ Indexed {result['success_count']}/{result['total']} documents",
                "success" if result['failed_count'] == 0 else "warning"
            )
            
            if result['errors']:
                with st.expander("Show Errors"):
                    for error in result['errors']:
                        st.error(error)
            
            logger.info(f"Batch indexing completed", result=result)
            
            st.rerun()
            
        except Exception as e:
            render_info_message(f"❌ Batch indexing failed: {str(e)}", "error")


def handle_clear_all_indexes() -> None:
    """
    Handle clearing all indexes.
    """
    st.warning("⚠️ This will remove all chunks from the vector store!")
    
    if st.button("Confirm Clear All"):
        with render_spinner("Clearing all indexes..."):
            try:
                indexing_service = get_indexing_service()
                indexing_service.clear_all_indexes()
                
                render_info_message("✅ All indexes cleared", "success")
                logger.warning("All indexes cleared via admin panel")
                
                st.rerun()
                
            except Exception as e:
                render_info_message(f"❌ Clear failed: {str(e)}", "error")


def render_testing_tab() -> None:
    """
    Render testing tab for LLM providers.
    """
    st.markdown("### 🧪 Provider Testing")
    
    chat_service = get_chat_service()
    
    st.markdown("Test LLM provider connectivity:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Test Gemini", type="primary", use_container_width=True):
            test_provider_connectivity('gemini', chat_service)
    
    with col2:
        if st.button("🧪 Test Cohere", use_container_width=True):
            test_provider_connectivity('cohere', chat_service)


def test_provider_connectivity(provider: str, chat_service) -> None:
    """
    Test LLM provider connectivity.
    
    Args:
        provider: Provider name
        chat_service: ChatService instance
    """
    with render_spinner(f"Testing {provider}..."):
        result = chat_service.test_provider(provider)
        
        if result['success']:
            render_info_message(
                f"✅ {provider.title()} is working! (Response time: {result['response_time']:.2f}s)",
                "success"
            )
            
            with st.expander("Show Response"):
                st.text(result['response'])
        else:
            render_info_message(
                f"❌ {provider.title()} test failed: {result['message']}",
                "error"
            )


# Convenience: Allow direct import
__all__ = [
    'render_admin_panel',
    'render_dashboard_tab',
    'render_documents_tab',
    'render_indexing_tab',
    'render_testing_tab',
]
