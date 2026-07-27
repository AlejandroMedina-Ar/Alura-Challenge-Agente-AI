# 🔧 Documentación Técnica - TechFlow Solutions RAG Agent

**Referencia técnica completa para desarrolladores**

---

## 📑 Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Estructura de Módulos](#estructura-de-módulos)
3. [Flujos de Datos](#flujos-de-datos)
4. [Referencia de APIs](#referencia-de-apis)
5. [Configuración](#configuración)
6. [Base de Datos](#base-de-datos)
7. [Despliegue](#despliegue)
8. [Rendimiento](#rendimiento)

---

## 🏗️ Arquitectura del Sistema

### Vista General

```
┌──────────────────────────────────────────────┐
│         Interfaz Web (Streamlit)             │
│  app.py + ui/* - Componentes de interfaz    │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│            Capa de Servicios                 │
│  services/* - Lógica de negocio             │
│  • ChatService                                │
│  • KnowledgeLibraryService                   │
│  • IndexingService                           │
│  • ConfigurationService                      │
│  • AuthenticationService                     │
└──┬──────┬──────┬──────┬──────────────────────┘
   │      │      │      │
┌──▼──┐ ┌▼────┐ ┌▼──┐ ┌▼──────┐
│RAG  │ │ LLM │ │Auth│ │Storage│
│Pipeline│ │Provs│ │   │ │       │
└──┬──┘ └──┬──┘ └────┘ └───┬───┘
   │       │                │
┌──▼───────▼────────────────▼──────┐
│      Capa de Infraestructura      │
│  • ChromaDB (vector store)       │
│  • File System (documentos)      │
│  • JSON (configuración)          │
│  • Logging (logs)                │
└──────────────────────────────────┘
```

### Capas del Sistema

**Capa 1: UI (Streamlit)**
- Maneja interacciones del usuario
- Renderiza páginas y componentes
- Gestiona estado de sesión
- Enruta acciones a servicios

**Capa 2: Servicios**
- Orquesta lógica de negocio
- Coordina entre módulos
- Implementa workflows
- Maneja gestión de errores

**Capa 3: Módulos Core**
- RAG: Embeddings, retrieval, prompting
- LLM: Integraciones de proveedores
- Auth: Autenticación y sesiones
- Storage: Persistencia de datos

**Capa 4: Infraestructura**
- Base de datos vectorial (ChromaDB)
- Almacenamiento de archivos
- Gestión de configuración
- Sistema de logging

---

## 📦 Estructura de Módulos

### src/config

**Propósito:** Configuración y constantes de la aplicación

**Archivos:**
- `constants.py` - Constantes de la aplicación
- `paths.py` - Rutas de directorios
- `settings.py` - Gestión de configuración

**Exportaciones Clave:**
```python
from src.config import (
    # Constantes RAG
    DEFAULT_CHUNK_SIZE,      # 1000
    DEFAULT_CHUNK_OVERLAP,   # 200
    DEFAULT_TOP_K,           # 5
    DEFAULT_TEMPERATURE,     # 0.7
    
    # Enums
    FileFormat,
    LLMProvider,
    Theme,
    SessionKey,
    MetadataField
)
```

### src/utils

**Propósito:** Funciones utilitarias

**Archivos:**
- `exceptions.py` - Excepciones personalizadas
- `helpers.py` - Funciones auxiliares
- `logger.py` - Configuración de logging
- `validators.py` - Validación de entrada

**Excepciones:**
```python
from src.utils import (
    ConfigurationError,
    AuthenticationError,
    DocumentNotFoundError,
    InvalidDocumentError,
    LLMError,
    RAGError
)
```

### src/storage

**Propósito:** Capa de persistencia

**Archivos:**
- `config_repository.py` - Almacenamiento de configuración
- `document_repository.py` - Seguimiento de documentos
- `metadata_repository.py` - Metadata de documentos
- `file_manager.py` - Operaciones de archivos

**Singletons:**
```python
from src.storage import (
    get_config_repository,
    get_document_repository,
    get_metadata_repository,
    get_file_manager
)
```

### src/auth

**Propósito:** Autenticación y gestión de sesiones

**Archivos:**
- `authentication.py` - Verificación de contraseñas
- `session.py` - Gestión de sesiones

**Uso:**
```python
from src.auth import get_authenticator, get_session_manager

auth = get_authenticator()
session = get_session_manager()
```

### src/llm

**Propósito:** Integraciones de proveedores LLM

**Archivos:**
- `base_provider.py` - Clase base abstracta
- `gemini_provider.py` - Google Gemini 3.6 Flash
- `cohere_provider.py` - Cohere Command-R (fallback)

**Uso:**
```python
from src.llm import get_gemini_provider, get_cohere_provider

# Usar Gemini
provider = get_gemini_provider()
response = provider.chat_completion(
    messages=[{'role': 'user', 'content': 'Hello'}],
    temperature=0.7
)

# Streaming
for chunk in provider.chat_completion_stream(messages, 0.7):
    print(chunk, end='', flush=True)
```

### src/rag

**Propósito:** Componentes del pipeline RAG

**Archivos:**
- `embedding_service.py` - Embeddings con Sentence Transformers
- `vector_store.py` - Wrapper de ChromaDB
- `chunker.py` - Fragmentación de texto
- `retriever.py` - Recuperación de documentos
- `prompt_builder.py` - Construcción de prompts
- `pipeline.py` - Orquestación RAG

**Pipeline RAG:**
```python
from src.rag import get_rag_pipeline

pipeline = get_rag_pipeline()

# Consultar con RAG
messages = pipeline.query(
    user_query="¿Qué es RAG?",
    top_k=5
)

# Verificar si está listo
if pipeline.is_ready():
    # Tiene documentos indexados
    pass
```

### src/services

**Propósito:** Servicios de lógica de negocio

**Archivos:**
- `authentication_service.py` - Operaciones de autenticación
- `configuration_service.py` - Gestión de configuración
- `knowledge_library_service.py` - CRUD de documentos
- `indexing_service.py` - Indexación de documentos
- `chat_service.py` - Chat con RAG

**Uso de Servicios:**
```python
from src.services import (
    get_authentication_service,
    get_knowledge_library_service,
    get_indexing_service,
    get_chat_service
)

# Subir documento
kl_service = get_knowledge_library_service()
metadata = kl_service.upload_document(
    file_path="/tmp/upload.pdf",
    filename="doc.pdf",
    file_type="application/pdf",
    file_size=102400
)

# Indexar
indexing_service = get_indexing_service()
result = indexing_service.index_document(
    doc_id=metadata['doc_id'],
    filename="doc.pdf"
)

# Chat
chat_service = get_chat_service()
for chunk in chat_service.chat("¿Qué es RAG?", stream=True):
    print(chunk, end='')
```

### src/ui

**Propósito:** Componentes de interfaz Streamlit

**Archivos:**
- `theme.py` - Gestión de temas (claro/oscuro)
- `components.py` - Widgets reutilizables
- `sidebar.py` - Navegación lateral
- `chat.py` - Interfaz de chat
- `admin_panel.py` - Panel de administración
- `settings_panel.py` - Interfaz de configuración

---

## 🔄 Flujos de Datos

### Flujo de Subida de Documentos

```
Usuario sube archivo
      ↓
UI valida archivo (tamaño, tipo)
      ↓
KnowledgeLibraryService.upload_document()
      ↓
FileManager.save_document()
  → Guarda en data/knowledge_library/documents/
      ↓
DocumentRepository.create_document()
  → Guarda metadata
      ↓
Retorna metadata del documento
```

### Flujo de Indexación

```
Usuario click "Indexar"
      ↓
IndexingService.index_document(doc_id, filename)
      ↓
FileManager.read_document()
  → Carga contenido
      ↓
TextChunker.chunk_document()
  → Divide en fragmentos (chunk_size=1000, overlap=200)
      ↓
EmbeddingService.generate_embeddings()
  → Genera embeddings (multilingual-e5-base, 768d)
      ↓
VectorStore.add_documents()
  → Almacena en ChromaDB
      ↓
MetadataRepository.update_metadata()
  → Marca como indexado
```

### Flujo de Consulta en Chat

```
Usuario envía mensaje
      ↓
ChatService.chat(query, stream=True)
      ↓
RAGPipeline.query(user_query, top_k)
      ↓
  ├─► EmbeddingService.generate_query_embedding()
  │    → Genera embedding de la consulta
  ├─► VectorStore.search()
  │    → Recupera top-k fragmentos por similitud
  └─► PromptBuilder.build_prompt()
       → Construye mensajes con contexto
      ↓
LLMProvider.chat_completion_stream(messages)
  ├─► Intenta Gemini 3.6 Flash (principal)
  └─► Fallback a Cohere Command-R (si falla)
      ↓
Stream de respuesta al usuario
```

---

## 📚 Referencia de APIs

### AuthenticationService

```python
from src.services import get_authentication_service

auth_service = get_authentication_service()

# Login
auth_service.login("password")

# Verificar autenticación
if auth_service.is_authenticated():
    # Usuario está logueado
    pass

# Requerir autenticación (raise si no autenticado)
auth_service.require_authentication()

# Logout
auth_service.logout()
```

### KnowledgeLibraryService

```python
from src.services import get_knowledge_library_service

kl_service = get_knowledge_library_service()

# Subir documento
metadata = kl_service.upload_document(
    file_path="/tmp/file.pdf",
    filename="doc.pdf",
    file_type="application/pdf",
    file_size=102400
)

# Listar documentos
documents = kl_service.list_documents()
# Retorna: [{'doc_id': '...', 'filename': '...', 'indexed': True}, ...]

# Eliminar documento
kl_service.delete_document(doc_id)

# Verificar existencia
exists = kl_service.document_exists("doc.pdf")

# Obtener estadísticas
stats = kl_service.get_storage_stats()
# Retorna: {'total_documents': 10, 'indexed_documents': 8, 'total_size': ...}
```

### IndexingService

```python
from src.services import get_indexing_service

indexing_service = get_indexing_service()

# Indexar documento único
result = indexing_service.index_document(doc_id, filename)
# Retorna: {'success': True, 'chunk_count': 42, ...}

# Indexación por lotes
docs = [
    {'doc_id': 'doc1', 'filename': 'file1.pdf'},
    {'doc_id': 'doc2', 'filename': 'file2.pdf'}
]
result = indexing_service.batch_index_documents(docs)
# Retorna: {'total': 2, 'success_count': 2, 'failed_count': 0, ...}

# Obtener estadísticas
stats = indexing_service.get_indexing_stats()
# Retorna: {'total_documents': 10, 'indexed_documents': 8, 'pending_documents': 2, ...}

# Obtener documentos pendientes
pending = indexing_service.get_pending_documents()
# Retorna: [{'document_name': 'doc.pdf', 'file_size': ..., 'indexed': False}, ...]
```

### ChatService

```python
from src.services import get_chat_service

chat_service = get_chat_service()

# Chat con streaming
for chunk in chat_service.chat(
    query="¿Qué es RAG?",
    conversation_history=None,
    stream=True
):
    print(chunk, end='', flush=True)

# Chat sin streaming
response = chat_service.chat(
    query="¿Qué es RAG?",
    stream=False
)

# Probar proveedor
result = chat_service.test_provider('gemini')
# Retorna: {'success': True, 'response_time': 1.23, 'response': '...'}
```

### RAGPipeline

```python
from src.rag import get_rag_pipeline

pipeline = get_rag_pipeline()

# Consultar (retorna mensajes para LLM)
messages = pipeline.query(
    user_query="¿Qué es RAG?",
    top_k=5,
    conversation_history=[...],  # Opcional
    metadata_filter={'source': 'doc.pdf'}  # Opcional
)

# Verificar si está listo
if pipeline.is_ready():
    # Tiene documentos indexados
    pass

# Obtener fragmentos relevantes (sin prompting)
chunks = pipeline.get_relevant_chunks("query", top_k=3)
# Retorna: [{'text': '...', 'metadata': {...}, 'score': 0.12}, ...]

# Actualizar configuración
pipeline.update_top_k(10)

# Obtener estadísticas
stats = pipeline.get_stats()
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# API Keys de LLM (al menos una requerida)
GEMINI_API_KEY=tu_api_key_de_gemini
COHERE_API_KEY=tu_api_key_de_cohere

# Modelo a usar (opcional, default: gemini-3.6-flash)
GEMINI_MODEL=gemini-3.6-flash
COHERE_MODEL=command-r7b-12-2024

# Autenticación
ADMIN_PASSWORD=tu_contraseña_segura

# Logging (opcional)
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Parámetros RAG (opcional, sobreescribe defaults)
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
DEFAULT_TOP_K=5
DEFAULT_TEMPERATURE=0.7
```

### Configuración en Tiempo de Ejecución (data/config.json)

```json
{
  "llm": {
    "provider": "gemini",
    "model": "gemini-3.6-flash",
    "api_key": ""
  },
  "rag": {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "top_k": 5,
    "temperature": 0.7
  },
  "ui": {
    "theme": "light"
  }
}
```

**Prioridad de Configuración:**
1. Configuración en runtime (data/config.json) - más alta
2. Variables de entorno (.env)
3. Defaults hard-coded - más baja

---

## 🗄️ Base de Datos

### ChromaDB

**Colección:** `techflow_documents`

**Campos:**
- `id`: string - ID del fragmento (formato: `{doc_id}_chunk_{index}`)
- `embedding`: float[] - Vector de 768 dimensiones (multilingual-e5-base)
- `document`: string - Contenido de texto del fragmento
- `metadata`: object - Metadata del fragmento

**Estructura de Metadata:**
```json
{
  "source": "document.pdf",
  "doc_id": "uuid",
  "chunk_index": 0,
  "total_chunks": 42,
  "file_type": "pdf"
}
```

### Metadata de Documentos (JSON)

**Ubicación:** `data/knowledge_library/metadata/{document_name}.json`

**Estructura:**
```json
{
  "document_name": "document.pdf",
  "upload_date": "2026-07-25T10:30:00",
  "file_size": 102400,
  "file_format": "pdf",
  "checksum": "sha256_hash",
  "indexed": true,
  "index_date": "2026-07-25T10:35:00",
  "chunk_count": 42,
  "tags": [],
  "description": ""
}
```

**Campos Clave:**
- `document_name` - Nombre del archivo (ID único)
- `indexed` - Boolean (false = pendiente de indexar)
- `chunk_count` - Número de fragmentos generados
- `checksum` - SHA-256 para detección de duplicados

---

## 🚀 Despliegue

### Desarrollo Local

```bash
# Configuración inicial
python setup.py

# Tests de integración
python test_integration.py

# Iniciar aplicación
python run.py
```

### Producción

**Requisitos:**
- Python 3.11+
- 2GB RAM mínimo
- 1GB espacio en disco
- Conexión a internet (para APIs de LLM)

**Configuración de Entorno:**
```bash
# .env de producción
ADMIN_PASSWORD=contraseña_produccion_segura
GEMINI_API_KEY=key_produccion
COHERE_API_KEY=key_produccion
LOG_LEVEL=WARNING
```

**Configuración de Streamlit:**
Crear `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
base = "light"
```

**Ejecutar:**
```bash
streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0
```

### Streamlit Cloud

**Variables de Entorno (Secrets):**
```toml
GEMINI_API_KEY = "tu-api-key"
COHERE_API_KEY = "tu-api-key"
ADMIN_PASSWORD = "tu-password"
GEMINI_MODEL = "gemini-3.6-flash"
```

**Consideraciones:**
- ChromaDB se reinicia con cada redeploy
- Para persistencia, considera vector store externo (Pinecone, Weaviate)

---

## ⚡ Rendimiento

### Optimización de Indexación

**Mejores Prácticas:**
- Subir múltiples documentos antes de indexar
- Usar chunk sizes más pequeños para indexación más rápida
- Indexar durante horas de bajo uso

**Tiempos Típicos:**
- Documento 1MB (PDF): ~10-30 segundos
- Generación de embeddings: ~100 chunks/segundo
- Almacenamiento en ChromaDB: ~500 chunks/segundo

### Optimización de Consultas

**Mejores Prácticas:**
- Reducir top-k para retrieval más rápido (3-5 recomendado)
- Mantener chunk size balanceado (1000 caracteres)
- Usar metadata filters para búsquedas más específicas

**Tiempos Típicos:**
- Embedding de consulta: ~50ms
- Búsqueda en ChromaDB: ~100-500ms (depende del tamaño)
- Generación LLM: ~1-3 segundos (streaming)

### Uso de Memoria

**Consumo Típico:**
- ChromaDB: ~100MB base + ~1KB por chunk
- Embeddings en caché: ~300MB
- Streamlit UI: ~50-100MB
- **Total:** ~500MB-1GB para 10,000 chunks

### Monitoreo

**Revisar Logs:**
```bash
tail -f data/logs/application.log
```

**Métricas Clave:**
- Tiempo de respuesta de consultas
- Tiempo de indexación por documento
- Tamaño del vector store
- Latencia de llamadas API

---

## 🛠️ Guías de Desarrollo

### Estilo de Código

**Seguir:**
- PEP 8 para código Python
- Type hints para todas las funciones
- Docstrings para APIs públicas
- Principio de Responsabilidad Única

**Ejemplo:**
```python
def process_document(
    file_path: str,
    chunk_size: int = 1000
) -> dict:
    """
    Procesa un documento para indexación.
    
    Args:
        file_path: Ruta al archivo del documento
        chunk_size: Tamaño de fragmentos de texto
    
    Returns:
        dict: Resultados del procesamiento
    
    Raises:
        InvalidDocumentError: Si el archivo es inválido
    """
    # Implementación
    pass
```

### Logging

**Niveles de Log:**
```python
logger.debug(f"Processing document", filename=filename)
logger.info(f"Document indexed", doc_id=doc_id, chunks=42)
logger.warning(f"API quota low", provider="gemini")
logger.error(f"Indexing failed", error=str(e), exc_info=True)
```

### Testing

**Unit Tests:**
```bash
pytest tests/unit/
```

**Integration Tests:**
```bash
python test_integration.py
```

---

## 🔒 Consideraciones de Seguridad

**API Keys:**
- Nunca commitear API keys a git
- Usar variables de entorno
- Rotar keys regularmente

**Autenticación:**
- Usar contraseñas fuertes (hasheadas con bcrypt)
- Implementar timeouts de sesión
- Logout al cerrar navegador

**Validación de Entrada:**
- Validar todas las entradas de usuario
- Sanitizar nombres de archivo
- Verificar tipos y tamaños de archivo

**Privacidad de Datos:**
- Documentos almacenados localmente
- No se envían datos a terceros (excepto APIs de LLM)
- Revisar documentos antes de subir

---

## 📝 Stack Tecnológico

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| **LLM Principal** | Google Gemini | 3.6 Flash | Generación de respuestas |
| **LLM Fallback** | Cohere Command-R | command-r7b-12-2024 | Backup automático |
| **Embeddings** | Sentence Transformers | multilingual-e5-base | Embeddings locales (768d) |
| **Vector Store** | ChromaDB | 1.0.16 | Base de datos vectorial |
| **Framework RAG** | LangChain | 0.3.27 | Orquestación |
| **UI Framework** | Streamlit | 1.47.1 | Interfaz web |
| **PDF Parser** | PyMuPDF | 1.23+ | Extracción de texto |
| **Auth** | bcrypt | 5.0+ | Hash de contraseñas |
| **Python** | Python | 3.11+ | Lenguaje base |

---

**Versión:** 1.0.0  
**Última Actualización:** Julio 2026  
**Mantenido por:** TechFlow Solutions
