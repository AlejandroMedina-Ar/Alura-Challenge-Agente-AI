# Architecture.md

# TechFlow AI Corporate Knowledge Agent

## Software Architecture Document (SAD)

**Version:** 1.0

**Status:** Draft

**Project:** Alura Challenge Agente AI

**Author:** Oscar Alejandro Medina

---

# 1. Purpose

This document defines the software architecture of the TechFlow AI Corporate Knowledge Agent.

Its objective is to describe how the application is organized internally, how its modules interact, and which architectural decisions guide the implementation.

Project objectives, business scope and functional requirements are defined in **specs/000-project-overview.md**.

---

# 2. Architectural Principles

The architecture follows the following principles:

- Keep It Simple (KISS)
- Separation of Concerns
- Single Responsibility Principle
- Low Coupling
- High Cohesion
- Configuration over Hardcoding
- Modular Monolith
- AI Provider Agnostic
- Maintainability First

Every module should have one clear responsibility.

---

# 3. High-Level Architecture

```
                         User

                           │

                   Streamlit Interface

                           │

                    Application Layer

        ┌────────────┬─────────────┬────────────┐

        │            │             │

   Authentication   Chat      Knowledge Base

        │            │             │

        └────────────┴─────────────┘

                     RAG Pipeline

        ┌────────────┬─────────────┬────────────┐

        │            │             │

   Embeddings   ChromaDB     LLM Provider

```

The application is implemented as a modular monolith.

Each layer communicates only with the services directly below it.

---

# 4. Layer Responsibilities

## Presentation Layer

Responsible for:

- User Interface
- Navigation
- Forms
- Chat
- Theme Management
- Status Messages

Technology:

- Streamlit

---

## Application Layer

Responsible for:

- Business workflows
- Session state (temporary in-memory conversation context during active session only)
- Service orchestration
- Request routing

This layer contains no UI code.

**Note:** "Session state" refers to temporary conversation memory during the current active session using Streamlit session state. It does NOT include persistent conversation history across sessions, which is explicitly out of scope for v1.

---

## RAG Layer

Responsible for:

- Query Embeddings
- Similarity Search
- Prompt Construction
- Context Assembly
- Response Generation

The RAG pipeline should remain independent of any specific LLM provider.

---

## Infrastructure Layer

Responsible for:

- ChromaDB
- Embedding Models
- LLM Providers
- File Storage
- Environment Configuration

Infrastructure components should be replaceable without affecting higher layers.

---

# 5. Component Architecture

The system is organized into independent services.

```
techflow-rag-agent/

├── src/

│   ├── app.py

│   ├── ui/

│   │   ├── chat.py

│   │   ├── sidebar.py

│   │   ├── admin_panel.py

│   │   ├── settings_panel.py

│   │   ├── components.py

│   │   └── theme.py

│   │

│   ├── services/

│   │   ├── authentication_service.py

│   │   ├── chat_service.py

│   │   ├── knowledge_library_service.py

│   │   ├── indexing_service.py

│   │   └── configuration_service.py

│   │

│   ├── rag/

│   │   ├── pipeline.py

│   │   ├── retriever.py

│   │   ├── chunker.py

│   │   ├── embedding_service.py

│   │   ├── vector_store.py

│   │   └── prompt_builder.py

│   │

│   ├── llm/

│   │   ├── base_provider.py

│   │   ├── gemini_provider.py

│   │   └── cohere_provider.py

│   │

│   ├── storage/

│   │   ├── document_repository.py

│   │   ├── metadata_repository.py

│   │   ├── config_repository.py

│   │   └── file_manager.py

│   │

│   ├── auth/

│   │   ├── authentication.py

│   │   └── session.py

│   │

│   ├── config/

│   │   ├── settings.py

│   │   ├── constants.py

│   │   └── paths.py

│   │

│   └── utils/

│       ├── logger.py

│       ├── helpers.py

│       ├── validators.py

│       └── exceptions.py

│

├── assets/

│   ├── css/

│   └── images/

│

├── data/

│   ├── knowledge_library/

│   ├── chromadb/

│   ├── logs/

│   └── config.json

│

├── specs/

├── architecture/

├── prompts/

└── requirements.txt
```

Each service owns a single business responsibility.

---

# 6. Data Flow

## Knowledge Indexing

```
Knowledge Asset

↓

Validation

↓

Document Loader

↓

Chunking

↓

Embeddings

↓

ChromaDB
```

---

## Question Answering

```
User Question

↓

Embedding

↓

Similarity Search

↓

Context Retrieval

↓

Prompt Builder

↓

LLM

↓

Answer

↓

Source Attribution
```

Both workflows remain independent.

---

# 7. Module Dependencies

Dependency direction should always be:

```
UI

↓

Application

↓

Services

↓

Infrastructure
```

Lower layers must never depend on higher layers.

For example:

✓ Chat → LLM

✓ Chat → Retrieval

✗ ChromaDB → UI

✗ Embeddings → Streamlit

---

# 8. Configuration Strategy

Application behavior should be configurable.

Secrets:

- Environment Variables (.env)

Runtime Preferences:

- config.json

No configuration should be hardcoded.

---

# 9. Extension Points

The architecture intentionally supports future replacement of:

LLM Provider

- Google Gemini (default, v1)
- Cohere (fallback, v1)
- Future providers (not supported in v1): OpenAI, Claude, Groq, Ollama

Vector Database

- ChromaDB (default, v1)
- Future alternatives (not supported in v1): Pinecone, Weaviate, Qdrant

Embedding Models

- HuggingFace Sentence Transformers (default: intfloat/multilingual-e5-base, v1)
- Future alternatives (not supported in v1): intfloat/multilingual-e5-large, OpenAI embeddings, Nomic

Document Loaders

- Additional file formats (future)

These replacements should require minimal code changes.

---

# 10. Design Decisions

The following architectural decisions are considered stable.

### Modular Monolith

The application remains a single deployable unit.

### Streamlit

The UI is implemented exclusively with Streamlit.

### ChromaDB

The default vector database.

### LangChain

Used for orchestration and document processing.

### Environment-based Configuration

Sensitive information must never be hardcoded.

### Local Embeddings

Embeddings are generated locally whenever possible using multilingual models optimized for Spanish.

### Dual LLM Provider Strategy

Google Gemini is the primary LLM provider with Cohere as automatic fallback.

---

# 11. Error Isolation

Each service should manage its own exceptions.

Errors should propagate only as friendly application-level messages.

Internal exceptions should never be exposed directly to users.

---

# 12. Logging Strategy

Logging responsibilities are distributed.

Examples:

Authentication

Knowledge Library

Indexing

Retrieval

LLM Requests

Application Errors

Logging should support debugging rather than auditing.

---

# 13. Scalability Strategy

Although Version 1 is intentionally simple, the architecture supports future growth.

Potential extensions include:

- Additional document formats
- Larger Knowledge Libraries
- Multiple LLM providers
- Better embedding models
- Metadata filtering
- Hybrid search
- Reranking
- OCR

These extensions should require minimal architectural changes.

---

# 14. Architecture Constraints

The architecture intentionally avoids:

- Microservices
- Distributed systems
- SQL databases
- REST APIs
- Docker orchestration
- Kubernetes
- Message brokers
- Event sourcing

These technologies are unnecessary for Version 1.

---

# 15. Relationship with Specifications

This document describes **how the system is organized**.

The detailed behavior of each module is defined in:

- specs/000-project-overview.md
- specs/001-chat-interface.md
- specs/002-knowledge-base-management.md
- specs/003-authentication.md
- specs/004-rag-pipeline.md
- specs/005-configuration.md
- specs/006-deployment.md

If a conflict exists, the individual specification takes precedence over this document.

For terminology and naming conventions, refer to:

- architecture/Glossary.md

---

# 16. Final Notes

The architecture intentionally favors simplicity over sophistication.

Every architectural decision should contribute to one or more of the following goals:

- Readability
- Maintainability
- Modularity
- Ease of deployment
- Ease of extension

The objective is to provide a clean and professional foundation suitable for an educational AI project while remaining flexible enough for future enhancements.
