# Source Code Structure

## TechFlow AI Corporate Knowledge Agent

Version: 1.0

Status: Draft

---

# 1. Purpose

This document defines the physical organization of the project's source code.

Its purpose is to establish a consistent and maintainable directory structure before implementation begins.

Every source file should belong to a clearly defined module with a single responsibility.

This document complements:

- `architecture/Architecture.md`
- `specs/000-project-overview.md`

It does not redefine the project architecture or functional specifications.

---

# 2. Design Principles

The source code organization follows these principles:

- Single Responsibility Principle
- Separation of Concerns
- Low Coupling
- High Cohesion
- Readability
- Simplicity
- Modularity

The objective is to make the project easy to understand, maintain and extend.

---

# 3. Source Tree

```text
src/

│

├── app.py

│

├── ui/

├── services/

├── rag/

├── llm/

├── storage/

├── auth/

├── config/

└── utils/
```

Each directory has a single responsibility.

---

# 4. Module Responsibilities

## app.py

Application entry point.

Responsibilities:

- Initialize Streamlit.
- Load configuration.
- Initialize services.
- Configure application state.
- Launch the user interface.

Must never contain:

- business logic
- document processing
- authentication logic
- embedding generation
- direct LLM calls

---

## ui/

Contains every Streamlit component.

Example:

```text
ui/

chat.py

sidebar.py

admin_panel.py

settings.py

theme.py
```

Responsibilities:

- Render the interface.
- Collect user input.
- Display responses.
- Display status information.

The UI must never contain business logic.

---

## services/

Contains the application's business logic.

Example:

```text
services/

chat_service.py

knowledge_library_service.py

authentication_service.py

configuration_service.py

indexing_service.py
```

Responsibilities:

- Coordinate workflows
- Validate operations
- Connect UI with lower-level modules

Services should not know how the interface is implemented.

**Note:** Service naming follows the pattern `<domain>_service.py`. `authentication_service.py` acts as an Application Layer facade that uses `auth/authentication.py` for core authentication logic.

---

## rag/

Contains the Retrieval-Augmented Generation pipeline.

Example:

```text
rag/

pipeline.py

retriever.py

chunker.py

embedding_service.py

vector_store.py

prompt_builder.py

document_loader.py
```

Responsibilities:

- Orchestrate RAG workflow (pipeline.py)
- Extract text from documents (document_loader.py - PDF, DOCX, TXT, MD, CSV, JSON, HTML)
- Chunk documents (chunker.py)
- Generate embeddings (embedding_service.py)
- Query ChromaDB (vector_store.py)
- Retrieve context (retriever.py)
- Build prompts with system instructions, context, and user question

The RAG module should remain independent from the UI.

**Note:** `pipeline.py` acts as the primary orchestrator, coordinating embedding_service, retriever, and prompt_builder. It does NOT invoke the LLM directly; that responsibility belongs to chat_service.

---

## llm/

Contains language model integrations.

Example:

```text
llm/

base_provider.py

gemini_provider.py

cohere_provider.py

llm_service.py
```

Responsibilities:

- Define abstract provider interface (base_provider.py)
- Implement Gemini provider (gemini_provider.py)
- Implement Cohere provider (cohere_provider.py)
- Orchestrate fallback logic (llm_service.py)
- Connect to LLM providers (Gemini primary, Cohere fallback)
- Send prompts
- Receive responses
- Handle provider-specific errors and automatic fallback

**llm_service.py** acts as a facade that:
1. Initializes both Gemini and Cohere providers
2. Attempts request with Gemini (primary)
3. Implements retry logic (1 retry with 2s backoff)
4. Automatically falls back to Cohere on failure
5. Logs all fallback events
6. Returns response to chat_service

The rest of the application communicates only through `llm_service.py`, not directly with providers.

---

## storage/

Responsible for filesystem operations.

Example:

```text
storage/

document_repository.py

metadata_repository.py

config_repository.py

file_manager.py
```

Responsibilities:

- Read files from data/knowledge_library/documents/ (document_repository.py)
- Write files to data/knowledge_library/documents/ (document_repository.py)
- Manage asset metadata in data/knowledge_library/metadata/ (metadata_repository.py)
- Persist runtime configuration to data/config.json (config_repository.py - does NOT handle .env)
- General file operations (file_manager.py)

Business logic should never manipulate files directly.

**Note:** `config/settings.py` is responsible for reading `.env` and providing configuration values, but NOT for persisting them.

---

## config/

Contains configuration logic.

Example:

```text
config/

settings.py

constants.py

paths.py
```

Responsibilities:

- Load environment variables from .env (settings.py)
- Provide runtime configuration access (settings.py)
- Define application-wide constants (constants.py)
- Define and manage project paths (paths.py)

No business logic should exist in this module. Configuration should be read-only during runtime (except for config.json persistence via config_repository).

---

## auth/

Responsible for administrator authentication.

Example:

```text
auth/

authentication.py

session.py
```

Responsibilities:

- Password validation.
- Session management.
- Access control.

Only administrator functionality should depend on this module.

---

## config/

Centralized application configuration.

Example:

```text
config/

settings.py

constants.py
```

Responsibilities:

- Load `.env`.
- Load `config.json`.
- Validate configuration.
- Expose configuration values.

No other module should read configuration files directly.

---

## utils/

Shared utilities.

Example:

```text
utils/

logger.py

helpers.py

validators.py
```

Responsibilities:

- Logging.
- Common validation.
- Shared helper functions.

Avoid placing business logic here.

---

# 5. Dependency Rules

Modules should interact according to the following dependency flow:

```text
UI

↓

Services

↓

RAG / Authentication / Storage / LLM

↓

Configuration
```

Higher-level modules may depend on lower-level modules.

Lower-level modules must never depend on higher-level modules.

---

# 6. Import Rules

Allowed:

```text
UI → Services

Services → RAG

Services → Storage

Services → LLM

Services → Auth

RAG → Storage (for document loading)

Authentication Service → Auth (authentication_service.py → auth/authentication.py)

All modules → Config

All modules → Utils
```

Forbidden:

```text
RAG → UI

LLM → UI

Storage → UI

Authentication → UI

Utils → Services
```

This prevents circular dependencies and keeps responsibilities clear.

---

# 7. Runtime Data

No source code should write runtime files outside the `data/` directory.

Runtime files include:

```text
data/

knowledge_library/

chromadb/

logs/

config.json
```

---

# 8. Extensibility

Future features should be added by extending existing modules whenever appropriate.

Examples:

- New LLM providers belong in `llm/`
- New document loaders belong in `rag/`
- New configuration options belong in `config/`

Avoid creating new top-level directories unless absolutely necessary.

---

# 9. Naming Conventions

Use descriptive file names.

Examples:

Good:

```text
chat_service.py

configuration_service.py

vector_store.py

metadata_repository.py
```

Avoid:

```text
chat.py

utils2.py

manager.py

temp.py

misc.py
```

Every filename should clearly communicate its responsibility.

---

# 10. Definition of Done

The source code organization is considered correct when:

- Every module has a single responsibility.
- No business logic exists in the UI.
- Runtime files remain inside `data/`.
- Dependencies follow the defined architecture.
- Configuration is centralized.
- New contributors can understand the project structure quickly.
- The codebase remains simple and maintainable.

---

# References

This document should be read together with:

- `architecture/Architecture.md`
- `specs/000-project-overview.md`
- `prompts/system-prompt.md`
- `prompts/cursor-rules.md`

Together these documents define the project's architectural and implementation guidelines.
