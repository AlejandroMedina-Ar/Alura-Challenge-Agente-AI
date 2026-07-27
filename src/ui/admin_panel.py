"""
Módulo de Panel de Administración

Este módulo implementa la interfaz del panel de administración.
Proporciona gestión de documentos, controles de indexación y estadísticas del sistema.

Autor: TechFlow Solutions Project
Licencia: MIT
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
    Renderiza la página principal del panel de administración.
    
    Ejemplo:
        >>> render_admin_panel()
    """
    render_header("🔧 Panel de Administración", "Administra documentos y visualiza estadísticas del sistema")
    
    # Render tabs
    tabs = render_tabs([
        "📊 Dashboard",
        "📚 Documentos",
        "⚡ Indexación",
        "🧪 Pruebas"
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
    Renderiza el dashboard con estadísticas del sistema.
    """
    st.markdown("### 📊 Vista General del Sistema")
    
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
            label="Total de Documentos",
            value=str(storage_stats['total_documents']),
            help_text="Total de documentos subidos"
        )
    
    with cols[1]:
        render_metric_card(
            label="Documentos Indexados",
            value=str(storage_stats['indexed_documents']),
            help_text="Documentos indexados y listos"
        )
    
    with cols[2]:
        render_metric_card(
            label="Total de Fragmentos",
            value=str(indexing_stats['total_chunks']),
            help_text="Total de fragmentos indexados"
        )
    
    with cols[3]:
        render_metric_card(
            label="Almacenamiento Usado",
            value=f"{storage_stats['total_size_mb']:.2f} MB",
            help_text="Almacenamiento total usado"
        )
    
    st.divider()
    
    # System status
    st.markdown("### ⚙️ Estado del Sistema")
    
    cols = render_columns(2)
    
    with cols[0]:
        st.markdown("**Pipeline RAG**")
        if chat_stats['rag_ready']:
            st.success("✅ Listo")
        else:
            st.warning("⚠️ Sin documentos indexados")
        
        st.caption(f"Vector Store: {chat_stats['vector_store_count']} fragmentos")
        st.caption(f"Dim. Embedding: {indexing_stats['embedding_dimension']}")
    
    with cols[1]:
        st.markdown("**Configuración de LLM**")
        st.info(f"🤖 Proveedor: {chat_stats['primary_provider'].title()}")
        st.caption(f"Temperatura: {chat_stats['temperature']}")
        st.caption(f"Top-K: {chat_stats['top_k']}")


def render_documents_tab() -> None:
    """
    Renderiza la pestaña de gestión de documentos.
    """
    st.markdown("### 📚 Gestión de Documentos")
    
    kl_service = get_knowledge_library_service()
    
    # Upload section
    st.markdown("#### ⬆️ Subir Documento")
    
    uploaded_file = render_file_uploader(
        label="Selecciona un documento",
        accepted_types=['txt', 'pdf', 'md', 'docx'],
        help_text="Soportados: TXT, PDF, MD, DOCX (Máx 10MB)",
        key="admin_file_upload"
    )
    
    if uploaded_file:
        handle_file_upload(uploaded_file, kl_service)
    
    st.divider()
    
    # Documents list
    st.markdown("#### 📄 Documentos Subidos")
    
    documents = kl_service.list_documents()
    
    if not documents:
        render_empty_state(
            icon="📄",
            title="Sin Documentos",
            message="Sube tu primer documento para comenzar"
        )
    else:
        render_documents_table(documents, kl_service)


def handle_file_upload(uploaded_file, kl_service) -> None:
    """
    Maneja el proceso de carga de archivos.
    
    Args:
        uploaded_file: Archivo subido de Streamlit
        kl_service: Instancia de KnowledgeLibraryService
    """
    filename = uploaded_file.name
    file_size = uploaded_file.size
    file_type = uploaded_file.type
    
    # Upload (el servicio ya verifica si existe)
    with render_spinner(f"Subiendo {filename}..."):
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
                f"✅ ¡Documento '{filename}' subido exitosamente!",
                "success"
            )
            
            logger.info(f"Document uploaded via admin panel", filename=filename)
            
            st.rerun()
            
        except DocumentAlreadyExistsError:
            render_info_message(
                f"El documento '{filename}' ya existe",
                "warning"
            )
        
        except InvalidDocumentError as e:
            render_info_message(
                f"❌ Documento inválido: {str(e)}",
                "error"
            )
        
        except Exception as e:
            render_info_message(
                f"❌ Carga fallida: {str(e)}",
                "error"
            )
            logger.error(f"Upload failed", filename=filename, error=str(e))


def render_documents_table(documents: list[dict], kl_service) -> None:
    """
    Renderiza tabla de documentos con acciones.
    
    Args:
        documents: Lista de metadatos de documentos
        kl_service: Instancia de KnowledgeLibraryService
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
                st.caption(f"Tamaño: {file_size / 1024:.1f} KB | Subido: {upload_date}")
                
                if indexed:
                    st.success(f"✅ Indexado ({chunk_count} fragmentos)")
                else:
                    st.warning("⚠️ No indexado")
            
            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{doc_id}"):
                    handle_document_delete(doc_id, filename, kl_service)
            
            with col3:
                if not indexed:
                    if st.button("⚡ Indexar", key=f"index_{doc_id}"):
                        handle_document_index(doc_id, filename)
                else:
                    if st.button("🔄 Re-indexar", key=f"reindex_{doc_id}"):
                        handle_document_reindex(doc_id, filename)
            
            st.divider()


def handle_document_delete(doc_id: str, filename: str, kl_service) -> None:
    """
    Maneja la eliminación de documentos.
    
    Args:
        doc_id: ID del documento
        filename: Nombre del archivo del documento
        kl_service: Instancia de KnowledgeLibraryService
    """
    with render_spinner(f"Eliminando {filename}..."):
        try:
            # Remove from index first
            indexing_service = get_indexing_service()
            indexing_service.remove_document_from_index(doc_id)
            
            # Delete document
            kl_service.delete_document(doc_id)
            
            render_info_message(
                f"✅ Documento '{filename}' eliminado exitosamente",
                "success"
            )
            
            logger.info(f"Document deleted", filename=filename)
            
            st.rerun()
            
        except Exception as e:
            render_info_message(
                f"❌ Eliminación fallida: {str(e)}",
                "error"
            )
            logger.error(f"Delete failed", filename=filename, error=str(e))


def handle_document_index(doc_id: str, filename: str) -> None:
    """
    Maneja la indexación de documentos.
    
    Args:
        doc_id: ID del documento
        filename: Nombre del archivo del documento
    """
    with render_spinner(f"Indexando {filename}..."):
        try:
            indexing_service = get_indexing_service()
            result = indexing_service.index_document(doc_id, filename)
            
            render_info_message(
                f"✅ Indexados {result['chunk_count']} fragmentos de '{filename}'",
                "success"
            )
            
            logger.info(f"Document indexed", filename=filename, chunks=result['chunk_count'])
            
            st.rerun()
            
        except Exception as e:
            render_info_message(
                f"❌ Indexación fallida: {str(e)}",
                "error"
            )
            logger.error(f"Indexing failed", filename=filename, error=str(e))


def handle_document_reindex(doc_id: str, filename: str) -> None:
    """
    Maneja la re-indexación de documentos.
    
    Args:
        doc_id: ID del documento
        filename: Nombre del archivo del documento
    """
    with render_spinner(f"Re-indexando {filename}..."):
        try:
            indexing_service = get_indexing_service()
            result = indexing_service.reindex_document(doc_id, filename)
            
            render_info_message(
                f"✅ Re-indexados {result['chunk_count']} fragmentos de '{filename}'",
                "success"
            )
            
            logger.info(f"Document re-indexed", filename=filename)
            
            st.rerun()
            
        except Exception as e:
            render_info_message(
                f"❌ Re-indexación fallida: {str(e)}",
                "error"
            )


def render_indexing_tab() -> None:
    """
    Renderiza la pestaña de operaciones de indexación.
    """
    st.markdown("### ⚡ Operaciones de Indexación")
    
    indexing_service = get_indexing_service()
    
    # Indexing statistics
    stats = indexing_service.get_indexing_stats()
    
    cols = render_columns(3)
    
    with cols[0]:
        st.metric("Indexados", stats['indexed_documents'])
    
    with cols[1]:
        st.metric("Pendientes", stats['pending_documents'])
    
    with cols[2]:
        st.metric("Total Fragmentos", stats['total_chunks'])
    
    st.divider()
    
    # Batch operations
    st.markdown("#### 🔄 Operaciones por Lotes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚡ Indexar Todos los Pendientes", type="primary", use_container_width=True):
            handle_batch_index_all()
    
    with col2:
        if st.button("🗑️ Limpiar Todos los Índices", use_container_width=True):
            handle_clear_all_indexes()
    
    st.divider()
    
    # Pending documents
    pending = indexing_service.get_pending_documents()
    
    if pending:
        st.markdown(f"#### ⏳ Documentos Pendientes ({len(pending)})")
        
        for doc in pending:
            st.text(f"📄 {doc['filename']}")
    else:
        st.success("✅ Todos los documentos están indexados")


def handle_batch_index_all() -> None:
    """
    Maneja la indexación por lotes de todos los documentos pendientes.
    """
    indexing_service = get_indexing_service()
    pending = indexing_service.get_pending_documents()
    
    if not pending:
        render_info_message("No hay documentos pendientes para indexar", "info")
        return
    
    with render_spinner(f"Indexando {len(pending)} documentos..."):
        try:
            docs_to_index = [
                {'doc_id': doc['doc_id'], 'filename': doc['filename']}
                for doc in pending
            ]
            
            result = indexing_service.batch_index_documents(docs_to_index)
            
            render_info_message(
                f"✅ Indexados {result['success_count']}/{result['total']} documentos",
                "success" if result['failed_count'] == 0 else "warning"
            )
            
            if result['errors']:
                with st.expander("Mostrar Errores"):
                    for error in result['errors']:
                        st.error(error)
            
            logger.info(f"Batch indexing completed", result=result)
            
            st.rerun()
            
        except Exception as e:
            render_info_message(f"❌ Indexación por lotes fallida: {str(e)}", "error")


def handle_clear_all_indexes() -> None:
    """
    Maneja la limpieza de todos los índices.
    """
    st.warning("⚠️ ¡Esto eliminará todos los fragmentos del vector store!")
    
    if st.button("Confirmar Limpiar Todo"):
        with render_spinner("Limpiando todos los índices..."):
            try:
                indexing_service = get_indexing_service()
                indexing_service.clear_all_indexes()
                
                render_info_message("✅ Todos los índices limpiados", "success")
                logger.warning("All indexes cleared via admin panel")
                
                st.rerun()
                
            except Exception as e:
                render_info_message(f"❌ Limpieza fallida: {str(e)}", "error")


def render_testing_tab() -> None:
    """
    Renderiza la pestaña de pruebas para proveedores de LLM.
    """
    st.markdown("### 🧪 Prueba de Proveedores")
    
    chat_service = get_chat_service()
    
    st.markdown("Prueba la conectividad de proveedores de LLM:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Probar Gemini", type="primary", use_container_width=True):
            test_provider_connectivity('gemini', chat_service)
    
    with col2:
        if st.button("🧪 Probar Cohere", use_container_width=True):
            test_provider_connectivity('cohere', chat_service)


def test_provider_connectivity(provider: str, chat_service) -> None:
    """
    Prueba la conectividad del proveedor de LLM.
    
    Args:
        provider: Nombre del proveedor
        chat_service: Instancia de ChatService
    """
    with render_spinner(f"Probando {provider}..."):
        result = chat_service.test_provider(provider)
        
        if result['success']:
            render_info_message(
                f"✅ ¡{provider.title()} está funcionando! (Tiempo de respuesta: {result['response_time']:.2f}s)",
                "success"
            )
            
            with st.expander("Mostrar Respuesta"):
                st.text(result['response'])
        else:
            render_info_message(
                f"❌ Prueba de {provider.title()} falló: {result['message']}",
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
