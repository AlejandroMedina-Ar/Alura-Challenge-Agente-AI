# 🔧 TechFlow Solutions - Technical Documentation

**Complete technical reference for developers**

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Module Reference](#module-reference)
3. [Data Flow](#data-flow)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [Database Schema](#database-schema)
7. [Deployment](#deployment)
8. [Performance](#performance)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit UI Layer                 │
│  (app.py, ui/* - User interface components)        │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                 Services Layer                      │
│  (services/* - Business logic orchestration)       │
│  - ChatService                                      │
│  - KnowledgeLibraryService                         │
│  - IndexingService                                  │
│  - ConfigurationService                            │
│  - AuthenticationService                           │
└─────┬────────┬────────┬────────┬───────────────────┘
      │        │        │        │
┌─────▼──┐ ┌──▼────┐ ┌▼─────┐ ┌▼──────┐
│  RAG   │ │  LLM  │ │ Auth │ │Storage│
│Pipeline│ │Providers│ │     │ │       │
└────┬───┘ └───┬───┘ └──────┘ └───┬───┘
     │         │                   │
┌────▼─────────▼───────────────────▼────┐
│         Infrastructure Layer           │
│  - ChromaDB (vector store)            │
│  - File System (documents)            │
│  - JSON (configuration)               │
│  - Logging (application logs)         │
└───────────────────────────────────────┘
```

### Component Layers

**Layer 1: UI (Streamlit)**
- Handles user interactions
- Renders pages and components
- Manages session state
- Routes user actions to services

**Layer 2: Services**
- Orchestrates business logic
- Coordinates between modules
- Implements workflows
- Handles error management

**Layer 3: Core Modules**
- RAG: Embedding, retrieval, prompting
- LLM: Provider integrations
- Auth: Authentication and sessions
- Storage: Data persistence

**Layer 4: Infrastructure**
- Vector database (ChromaDB)
- File storage
- Configuration management
- Logging

---

## Module Reference

### src/config

**Purpose:** Application configuration and constants

**Files:**
- `constants.py` - Application constants
- `paths.py` - Directory paths
- `settings.py` - Settings management

**Key Exports:**
```python
# Paths
from src.config import (
    PROJECT_ROOT,
    DATA_DIR,
    LOGS_DIR,
    CHROMADB_DIR,
    KNOWLEDGE_LIBRARY_DIR
)

# Constants
from src.config import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_TOP_K,
    DEFAULT_TEMPERATURE
)

# Settings
from src.config import get_settings
```

### src/utils

**Purpose:** Utility functions and helpers

**Files:**
- `exceptions.py` - Custom exceptions
- `helpers.py` - Helper functions
- `logger.py` - Logging setup
- `validators.py` - Input validation

**Key Classes:**
```python
# Exceptions
from src.utils import (
    TechFlowException,
    ConfigurationError,
    AuthenticationError,
    DocumentNotFoundError,
    LLMError,
    RAGError
)

# Functions
from src.utils import (
    get_logger,
    setup_logging,
    validate_chunk_parameters,
    validate_top_k,
    sanitize_filename
)
```

### src/storage

**Purpose:** Data persistence layer

**Files:**
- `config_repository.py` - Configuration storage
- `document_repository.py` - Document tracking
- `metadata_repository.py` - Document metadata
- `file_manager.py` - File operations

**Singletons:**
```python
from src.storage import (
    ConfigRepository,
    DocumentRepository,
    MetadataRepository,
    FileManager
)
```

### src/auth

**Purpose:** Authentication and session management

**Files:**
- `authentication.py` - Password verification
- `session.py` - Session management

**Singletons:**
```python
from src.auth import (
    get_authenticator,
    get_session_manager
)
```

### src/llm

**Purpose:** LLM provider integrations

**Files:**
- `base_provider.py` - Abstract base class
- `gemini_provider.py` - Google Gemini integration
- `cohere_provider.py` - Cohere integration

**Singletons:**
```python
from src.llm import (
    get_gemini_provider,
    get_cohere_provider
)
```

**Usage:**
```python
# Initialize provider
provider = get_gemini_provider()

# Generate response
response = provider.chat_completion(
    messages=[{'role': 'user', 'content': 'Hello'}],
    temperature=0.7
)

# Streaming
for chunk in provider.chat_completion_stream(messages, 0.7):
    print(chunk, end='', flush=True)
```

### src/rag

**Purpose:** RAG pipeline components

**Files:**
- `embedding_service.py` - Text embeddings
- `vector_store.py` - ChromaDB wrapper
- `chunker.py` - Text chunking
- `retriever.py` - Document retrieval
- `prompt_builder.py` - Prompt construction
- `pipeline.py` - RAG orchestration

**Singletons:**
```python
from src.rag import (
    get_embedding_service,
    get_vector_store,
    get_text_chunker,
    get_rag_pipeline
)
```

**RAG Pipeline Usage:**
```python
pipeline = get_rag_pipeline()

# Query with RAG
messages = pipeline.query(
    user_query="What is RAG?",
    top_k=5
)

# Check if ready
if pipeline.is_ready():
    # Has indexed documents
    pass
```

### src/services

**Purpose:** Business logic services

**Files:**
- `authentication_service.py` - Auth operations
- `configuration_service.py` - Config management
- `knowledge_library_service.py` - Document CRUD
- `indexing_service.py` - Document indexing
- `chat_service.py` - Chat with RAG

**Singletons:**
```python
from src.services import (
    get_authentication_service,
    get_configuration_service,
    get_knowledge_library_service,
    get_indexing_service,
    get_chat_service
)
```

**Service Usage:**
```python
# Upload document
kl_service = get_knowledge_library_service()
metadata = kl_service.upload_document(
    file_path="/tmp/upload.pdf",
    filename="doc.pdf",
    file_type="application/pdf",
    file_size=102400
)

# Index document
indexing_service = get_indexing_service()
result = indexing_service.index_document(
    doc_id=metadata['doc_id'],
    filename="doc.pdf"
)

# Chat
chat_service = get_chat_service()
for chunk in chat_service.chat("What is RAG?", stream=True):
    print(chunk, end='')
```

### src/ui

**Purpose:** Streamlit interface components

**Files:**
- `theme.py` - Theme management
- `components.py` - Reusable widgets
- `sidebar.py` - Navigation sidebar
- `chat.py` - Chat interface
- `admin_panel.py` - Admin dashboard
- `settings_panel.py` - Settings UI

**Key Functions:**
```python
from src.ui import (
    apply_theme,
    render_sidebar,
    render_chat_page,
    render_admin_panel,
    render_settings_panel
)
```

---

## Data Flow

### Document Upload Flow

```
User uploads file
      ↓
UI validates file (size, type)
      ↓
KnowledgeLibraryService.upload_document()
      ↓
FileManager.save_document() → Save to data/knowledge_library/documents/
      ↓
MetadataRepository.create_metadata() → Save to data/knowledge_library/metadata/
      ↓
Return document metadata
```

### Document Indexing Flow

```
User clicks "Index"
      ↓
IndexingService.index_document(doc_id, filename)
      ↓
FileManager.read_document() → Load document content
      ↓
TextChunker.chunk_document() → Split into chunks
      ↓
EmbeddingService.generate_embeddings() → Generate vectors (batch)
      ↓
VectorStore.add_documents() → Store in ChromaDB
      ↓
MetadataRepository.update_metadata() → Mark as indexed
```

### Chat Query Flow

```
User sends message
      ↓
ChatService.chat(query, stream=True)
      ↓
RAGPipeline.query(user_query, top_k)
      ↓
  ├─► EmbeddingService.generate_query_embedding()
  ├─► VectorStore.search() → Retrieve top-k chunks
  └─► PromptBuilder.build_prompt() → Construct messages
      ↓
LLMProvider.chat_completion_stream(messages)
  ├─► Try Gemini (primary)
  └─► Fallback to Cohere (if fails)
      ↓
Stream response chunks to user
```

---

## API Reference

### Service APIs

#### AuthenticationService

```python
from src.services import get_authentication_service

auth_service = get_authentication_service()

# Login
user_info = auth_service.login("password")
# Returns: {'username': 'admin', 'role': 'admin'}

# Check authentication
if auth_service.is_authenticated():
    # User is logged in
    pass

# Require authentication (raises if not authenticated)
auth_service.require_authentication()

# Logout
auth_service.logout()
```

#### ConfigurationService

```python
from src.services import get_configuration_service

config_service = get_configuration_service()

# Get LLM config
llm_config = config_service.get_llm_config()
# Returns: {'provider': 'gemini', 'model': '...', 'api_key': '...'}

# Update RAG config
config_service.update_rag_config(
    chunk_size=512,
    chunk_overlap=50,
    top_k=5,
    temperature=0.7
)

# Get theme
theme = config_service.get_theme()  # 'light' or 'dark'

# Validate configuration
is_valid, errors = config_service.validate_configuration()
```

#### KnowledgeLibraryService

```python
from src.services import get_knowledge_library_service

kl_service = get_knowledge_library_service()

# Upload document
metadata = kl_service.upload_document(
    file_path="/tmp/file.pdf",
    filename="doc.pdf",
    file_type="application/pdf",
    file_size=102400
)

# List documents
documents = kl_service.list_documents()
# Returns: [{'doc_id': '...', 'filename': '...', 'indexed': True, ...}, ...]

# Delete document
kl_service.delete_document(doc_id)

# Check if exists
exists = kl_service.document_exists("doc.pdf")
```

#### IndexingService

```python
from src.services import get_indexing_service

indexing_service = get_indexing_service()

# Index single document
result = indexing_service.index_document(doc_id, filename)
# Returns: {'success': True, 'chunk_count': 42, ...}

# Batch index
docs = [
    {'doc_id': 'doc1', 'filename': 'file1.pdf'},
    {'doc_id': 'doc2', 'filename': 'file2.pdf'}
]
result = indexing_service.batch_index_documents(docs)
# Returns: {'total': 2, 'success_count': 2, 'failed_count': 0, ...}

# Get stats
stats = indexing_service.get_indexing_stats()
# Returns: {'total_documents': 10, 'indexed_documents': 8, ...}

# Get pending documents
pending = indexing_service.get_pending_documents()
```

#### ChatService

```python
from src.services import get_chat_service

chat_service = get_chat_service()

# Streaming chat
for chunk in chat_service.chat(
    query="What is RAG?",
    conversation_history=None,
    stream=True
):
    print(chunk, end='', flush=True)

# Non-streaming chat
response = chat_service.chat(
    query="What is RAG?",
    stream=False
)

# Test provider
result = chat_service.test_provider('gemini')
# Returns: {'success': True, 'response_time': 1.23, ...}

# Get stats
stats = chat_service.get_chat_stats()
```

### RAG Pipeline API

```python
from src.rag import get_rag_pipeline

pipeline = get_rag_pipeline()

# Query (returns messages for LLM)
messages = pipeline.query(
    user_query="What is RAG?",
    top_k=5,
    conversation_history=[...],
    metadata_filter={'source': 'doc.pdf'}  # Optional
)

# Check if ready
if pipeline.is_ready():
    # Has documents
    pass

# Get relevant chunks (without prompting)
chunks = pipeline.get_relevant_chunks("query", top_k=3)
# Returns: [{'text': '...', 'metadata': {...}, 'score': 0.12}, ...]

# Update configuration
pipeline.update_top_k(10)
pipeline.update_system_instruction("Custom instruction...")

# Get stats
stats = pipeline.get_stats()
```

---

## Configuration

### Environment Variables (.env)

```bash
# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key

# Authentication
ADMIN_PASSWORD=your_secure_password

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Optional: Override defaults
DEFAULT_CHUNK_SIZE=512
DEFAULT_CHUNK_OVERLAP=50
DEFAULT_TOP_K=5
DEFAULT_TEMPERATURE=0.7
```

### Runtime Configuration (data/config.json)

```json
{
  "llm": {
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "api_key": "encrypted_or_plain"
  },
  "rag": {
    "chunk_size": 512,
    "chunk_overlap": 50,
    "top_k": 5,
    "temperature": 0.7
  },
  "ui": {
    "theme": "light"
  }
}
```

**Configuration Priority:**
1. Runtime config (data/config.json) - highest
2. Environment variables (.env)
3. Hard-coded defaults - lowest

---

## Database Schema

### ChromaDB Collections

**Collection:** `techflow_documents`

**Fields:**
- `id`: string - Chunk ID (format: `{doc_id}_chunk_{index}`)
- `embedding`: float[] - 768-dimensional vector
- `document`: string - Chunk text content
- `metadata`: object - Chunk metadata

**Metadata Structure:**
```json
{
  "source": "document.pdf",
  "doc_id": "uuid",
  "chunk_index": 0,
  "total_chunks": 42
}
```

### Document Metadata (JSON files)

**Location:** `data/knowledge_library/metadata/{doc_id}.json`

**Structure:**
```json
{
  "doc_id": "uuid",
  "filename": "document.pdf",
  "file_type": "application/pdf",
  "file_size": 102400,
  "upload_date": "2026-07-25T10:30:00",
  "indexed": true,
  "chunk_count": 42,
  "last_indexed": "2026-07-25T10:35:00"
}
```

---

## Deployment

### Local Development

```bash
# Setup
python setup.py

# Run tests
python test_integration.py

# Start application
python run.py
```

### Production Deployment

**Requirements:**
- Python 3.9+
- 2GB RAM minimum
- 1GB disk space
- Internet connection (for LLM APIs)

**Environment Setup:**
```bash
# Production .env
ADMIN_PASSWORD=strong_production_password
GEMINI_API_KEY=production_key
COHERE_API_KEY=production_key
LOG_LEVEL=WARNING
```

**Streamlit Configuration:**
Create `.streamlit/config.toml`:
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

**Running:**
```bash
streamlit run src/app.py --server.port=8501
```

---

## Performance

### Optimization Tips

**Indexing Performance:**
- Batch upload documents before indexing
- Use smaller chunk sizes for faster indexing
- Index during off-peak hours

**Query Performance:**
- Reduce top-k for faster retrieval
- Use metadata filters to narrow search
- Keep chunk size balanced (512 recommended)

**Memory Usage:**
- ChromaDB uses ~100MB base + ~1KB per chunk
- Embeddings cached in memory
- Clear browser cache periodically

### Monitoring

**Check Logs:**
```bash
tail -f data/logs/application.log
```

**Key Metrics:**
- Query response time
- Indexing time per document
- Vector store size
- API call latency

---

## Development Guidelines

### Code Style

**Follow:**
- PEP 8 for Python code
- Type hints for all functions
- Docstrings for public APIs
- Single Responsibility Principle

**Example:**
```python
def process_document(
    file_path: str,
    chunk_size: int = 512
) -> dict:
    """
    Process a document for indexing.
    
    Args:
        file_path: Path to document file
        chunk_size: Size of text chunks
    
    Returns:
        dict: Processing results
    
    Raises:
        InvalidDocumentError: If file is invalid
    """
    # Implementation
    pass
```

### Testing

**Unit Tests:**
- Test individual functions
- Mock external dependencies
- Use pytest fixtures

**Integration Tests:**
- Test module interactions
- Use test database
- Clean up after tests

### Logging

**Log Levels:**
- DEBUG: Detailed diagnostic info
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

**Example:**
```python
logger.debug(f"Processing document", filename=filename)
logger.info(f"Document indexed", doc_id=doc_id, chunks=42)
logger.warning(f"API quota low", provider="gemini")
logger.error(f"Indexing failed", error=str(e), exc_info=True)
```

---

## Security Considerations

**API Keys:**
- Never commit API keys to git
- Use environment variables
- Rotate keys regularly

**Authentication:**
- Use strong passwords (bcrypt hashed)
- Implement session timeouts
- Logout on browser close

**Input Validation:**
- Validate all user inputs
- Sanitize filenames
- Check file types and sizes

**Data Privacy:**
- Documents stored locally
- No data sent to third parties (except LLM APIs)
- Review documents before uploading

---

**Version:** 1.0.0-beta  
**Last Updated:** 2026-07-25  
**Maintainer:** TechFlow Solutions Team
