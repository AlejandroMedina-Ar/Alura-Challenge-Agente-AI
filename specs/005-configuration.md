# Configuration Specification

**Specification ID:** SPEC-005

**Module:** Configuration

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the configurable settings used by the TechFlow AI Corporate Knowledge Agent.

The objective is to centralize all application configuration, allowing developers to switch providers, models and deployment environments without modifying the source code.

Configuration should be managed primarily through environment variables.

---

# 2. Scope

This specification covers:

- Environment variables
- LLM provider configuration
- Embedding configuration
- ChromaDB configuration
- Chat parameters
- Streamlit settings
- Logging
- Administrator settings

This specification does not cover deployment-specific infrastructure.

---

# 3. Configuration Principles

The application should follow these principles:

- Configuration over hardcoding
- Environment-driven settings
- Simple defaults
- Easy provider replacement
- Minimal required variables

No credentials should ever be hardcoded.

---

# 4. Environment File

The project should include an `.env.example` file.

Example

```env
# Administrator

ADMIN_PASSWORD=change_me

# LLM Providers (v1 supports Gemini primary, Cohere fallback)

GEMINI_API_KEY=your_gemini_api_key_here

GEMINI_MODEL=gemini-2.0-flash-exp

COHERE_API_KEY=your_cohere_api_key_here

COHERE_MODEL=command-r

# Embeddings

EMBEDDING_MODEL=intfloat/multilingual-e5-base

# Vector Database

CHROMA_DB_PATH=data/chromadb

CHROMA_COLLECTION=techflow_knowledge_base

# Chunking

CHUNK_SIZE=1000

CHUNK_OVERLAP=200

# Chat

MAX_CONTEXT_CHUNKS=4

TEMPERATURE=0.2

MAX_OUTPUT_TOKENS=1024

# Timeouts (seconds)

LLM_REQUEST_TIMEOUT=30

EMBEDDING_TIMEOUT=120

CHROMADB_TIMEOUT=10

# Logging

LOG_LEVEL=INFO

LOG_FILE=data/logs/application.log
```

---

# 5. Supported LLM Providers

v1 implements a dual-provider architecture for reliability and free-tier optimization.

Primary Provider (default):

- Google Gemini (free tier)

Fallback Provider:

- Cohere

Future providers (not supported in v1):

- OpenAI
- Anthropic Claude
- Azure OpenAI
- Groq
- Mistral AI
- Ollama (local)

Provider selection is automatic based on availability and error conditions (see SPEC-004 Section 13.1 for fallback logic).

---

# 6. Provider Configuration

Each provider requires its own API key.

Example

Google Gemini (Primary)

```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

GEMINI_MODEL=gemini-2.0-flash-exp
```

Cohere (Fallback)

```env
COHERE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

COHERE_MODEL=command-r
```

**Note:** v1 uses a dual-provider architecture with automatic fallback. Both `GEMINI_API_KEY` and `COHERE_API_KEY` should be configured for full functionality. If only one is available, the application will function with that provider only (without fallback capability).

---

# 7. Embedding Configuration

The embedding model should also be configurable.

Default

```env
EMBEDDING_MODEL=intfloat/multilingual-e5-base
```

**Model Selection Rationale:** v1 uses `intfloat/multilingual-e5-base` as the default embedding model because:
- **Multilingual Support:** Trained on 100+ languages with excellent Spanish performance
- **Optimized for Retrieval:** Specifically designed for semantic search tasks
- **Free and Local:** Runs locally via HuggingFace without API costs
- **Better Spanish Performance:** Significantly outperforms English-only models (like BAAI/bge-small-en-v1.5) for Spanish document retrieval

**Note:** `EMBEDDING_MODEL` must be a valid HuggingFace Hub identifier (example: `intfloat/multilingual-e5-base`).

Alternative multilingual models for future consideration:

- intfloat/multilingual-e5-large (higher quality, slower)
- sentence-transformers/paraphrase-multilingual-mpnet-base-v2
- hiiamsid/sentence_similarity_spanish_es (Spanish-specific)

Changing the embedding model requires rebuilding the entire Knowledge Base index to maintain consistency between stored vectors and query vectors.

---

# 8. ChromaDB Configuration

Recommended variables

```env
CHROMA_DB_PATH=data/chromadb

CHROMA_COLLECTION=techflow_knowledge_base
```

The application should automatically create the collection if it does not exist.

**ChromaDB Persistence Behavior:** ChromaDB automatically persists data when initialized with a `persist_directory` parameter (mapped to `CHROMA_DB_PATH`). In ChromaDB v0.4.0+, persistence is automatic and continuous - no explicit `.persist()` call is required. The data is written to disk incrementally during operations (add, update, delete). On application restart, ChromaDB automatically loads existing data from the specified path.

**Important:** Ensure `CHROMA_DB_PATH` points to a directory with write permissions and sufficient disk space. If the directory doesn't exist, ChromaDB creates it automatically on first initialization.

---

# 9. Chat Configuration

Recommended variables

```env
TEMPERATURE=0.2

MAX_CONTEXT_CHUNKS=4

MAX_OUTPUT_TOKENS=1024
```

These parameters control answer generation without modifying the application code.

---

# 9.1 Timeout Configuration

To prevent indefinite waits and ensure responsive failure handling, v1 defines timeout limits for external service calls.

Recommended variables

```env
LLM_REQUEST_TIMEOUT=30

EMBEDDING_TIMEOUT=120

CHROMADB_TIMEOUT=10
```

**Timeout Descriptions:**

`LLM_REQUEST_TIMEOUT` (default: 30 seconds)

Maximum wait time for LLM response (Gemini or Cohere). If exceeded, triggers fallback to secondary provider (see SPEC-004 Section 13.1).

`EMBEDDING_TIMEOUT` (default: 120 seconds)

Maximum wait time for embedding generation. Embedding models run locally and may take longer for large documents or batch processing. If exceeded, the operation fails with a user-friendly error.

`CHROMADB_TIMEOUT` (default: 10 seconds)

Maximum wait time for vector database queries. ChromaDB is local and should respond quickly. If exceeded, indicates potential database corruption or resource exhaustion.

All timeout values are in seconds and should be configurable via environment variables.

---

# 10. Streamlit Configuration

The application should configure Streamlit for a clean user experience.

Recommended settings:

- Wide layout
- Expanded sidebar
- Custom page title
- Custom favicon

Theme selection should default to Tokyo Night (Dark) while allowing the user to switch to Light mode from the interface.

---

# 11. Logging Configuration

Logging should be configurable.

Recommended variables

```env
LOG_LEVEL=INFO

LOG_FILE=data/logs/application.log
```

Supported levels:

- DEBUG
- INFO
- WARNING
- ERROR

**Log Rotation Policy:** v1 implements size-based log rotation to prevent disk exhaustion. When `application.log` reaches 10MB, it is rotated (renamed to `application.log.1`, `.2`, etc.). A maximum of 5 log files are retained. Older files are automatically deleted. This ensures logs remain manageable while preserving recent history for debugging.

---

# 12. Administrator Configuration

Administrator credentials should be stored only in the environment.

```env
ADMIN_PASSWORD=admin123
```

**Security Note for v1:** Since this is a demonstration project, if `ADMIN_PASSWORD` is not configured in `.env`, the application uses the default development password `admin123`. This allows rapid local development without setup friction.

⚠️ **CRITICAL WARNING:** The default password must NEVER be used in public deployments. Before deploying to Streamlit Cloud, Render, or any public environment, always configure a strong password in the deployment platform's environment variables/secrets.

No administrator credentials should exist in the source code.

---

# 13. Configuration Validation

On startup, the application should verify that required configuration values are present.

Required values:

- GEMINI_API_KEY (or COHERE_API_KEY - at least one LLM provider)
- EMBEDDING_MODEL

Optional but recommended:

- Both GEMINI_API_KEY and COHERE_API_KEY (for fallback functionality)
- ADMIN_PASSWORD (defaults to "admin123" for local development if not set)

If a critical required value is missing, the application should display a friendly error and stop initialization.

If only one LLM provider key is configured, the application should warn that fallback functionality is unavailable but continue initialization.

**ADMIN_PASSWORD Behavior:** If not configured, the application defaults to `admin123` for local development. This is intentional for v1 to reduce setup friction. A warning should be logged on startup: "Using default ADMIN_PASSWORD. Change this before public deployment."

---

# 14. Future Configuration Options

The configuration architecture should support future additions such as:

- Additional LLM providers (OpenAI, Claude, Ollama)
- Cloud vector databases (Pinecone, Weaviate)
- External storage (S3, Azure Blob)
- Multiple embedding models
- Hybrid search
- Streaming responses
- Request timeouts
- Retry policies

These features are outside the scope of v1.

---

# 15. Acceptance Criteria

This specification is complete when:

- All configurable values are externalized
- LLM provider fallback can be configured via environment variables
- Models can be changed using environment variables
- ChromaDB settings are configurable
- Chunking parameters are configurable
- Administrator credentials are externalized
- Missing configuration is detected during startup
- The application warns (but continues) if only one LLM provider is configured

---

# 16. Notes for AI Development Agents

Implementation Guidelines

- Read configuration from `.env`.
- Never hardcode secrets.
- Validate configuration during application startup.
- Keep provider logic independent from the RAG pipeline.
- Provide sensible defaults whenever possible.

---

# 17. Final Notes

The configuration system provides a simple and flexible mechanism for adapting the application to different environments, LLM providers and deployment targets.

All operational settings should be configurable without requiring changes to the application source code, ensuring portability, maintainability and ease of deployment.
