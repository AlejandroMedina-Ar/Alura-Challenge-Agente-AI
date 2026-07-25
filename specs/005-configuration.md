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

# LLM Provider

LLM_PROVIDER=gemini

LLM_MODEL=gemini-2.5-flash

LLM_API_KEY=

# Embeddings

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# Vector Database

CHROMA_DB_PATH=data/chromadb

# Chat

MAX_CONTEXT_CHUNKS=4

TEMPERATURE=0.2

MAX_OUTPUT_TOKENS=1024
```

---

# 5. Supported LLM Providers

Version 1 should support a provider abstraction.

Initially supported providers:

- Google Gemini
- OpenAI
- Ollama

Future providers:

- Anthropic Claude
- Azure OpenAI
- Cohere
- Mistral AI

The active provider should be selected using:

```env
LLM_PROVIDER
```

---

# 6. Provider Configuration

Each provider requires only its own API key.

Example

Google Gemini

```env
LLM_PROVIDER=gemini

LLM_MODEL=gemini-2.5-flash

LLM_API_KEY=xxxxxxxx
```

OpenAI

```env
LLM_PROVIDER=openai

LLM_MODEL=gpt-5.5

LLM_API_KEY=xxxxxxxx
```

Ollama

```env
LLM_PROVIDER=ollama

LLM_MODEL=qwen3-coder:8b

OLLAMA_BASE_URL=http://localhost:11434
```

Switching providers should require changing only the environment variables.

---

# 7. Embedding Configuration

The embedding model should also be configurable.

Default

```env
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

Future models may include:

- bge-base
- e5-small
- nomic-embed-text
- multilingual-e5

Changing the embedding model should not require code changes.

---

# 8. ChromaDB Configuration

Recommended variables

```env
CHROMA_DB_PATH=data/chromadb

CHROMA_COLLECTION=techflow_knowledge_base
```

The application should automatically create the collection if it does not exist.

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

# 10. Streamlit Configuration

The application should configure Streamlit for a clean user experience.

Recommended settings:

- Wide layout
- Expanded sidebar
- Custom page title
- Custom favicon

Theme selection should default to Dark (Tokyo Night) while allowing the user to switch to Light mode from the interface.

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

---

# 12. Administrator Configuration

Administrator credentials should be stored only in the environment.

```env
ADMIN_PASSWORD=my_secure_password
```

No administrator credentials should exist in the source code.

---

# 13. Configuration Validation

On startup, the application should verify that required configuration values are present.

Required values:

- ADMIN_PASSWORD
- LLM_PROVIDER
- LLM_MODEL

If a required value is missing, the application should display a friendly error and stop initialization.

---

# 14. Future Configuration Options

The configuration architecture should support future additions such as:

- Multiple LLM providers
- Cloud vector databases
- External storage
- Multiple embedding models
- Hybrid search
- Streaming responses

These features are outside the scope of Version 1.

---

# 15. Acceptance Criteria

This specification is complete when:

- All configurable values are externalized.
- Providers can be switched without modifying code.
- Models can be changed using environment variables.
- ChromaDB settings are configurable.
- Administrator credentials are externalized.
- Missing configuration is detected during startup.

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
