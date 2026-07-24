# Architecture.md

# TechFlow AI Corporate Knowledge Agent

## Software Architecture Document (SAD)

Version: 1.0

Status: Draft

Project: Alura Challenge Agente AI

Author: Oscar Alejandro Medina

---

# 1. Overview

## Purpose

This document describes the software architecture of the TechFlow AI Corporate Knowledge Agent.

The application is based on a Retrieval-Augmented Generation (RAG) architecture that allows users to ask questions about company documentation using natural language.

The objective is to provide a simple, modular and maintainable architecture while keeping deployment and operational costs close to zero by using free-tier technologies.

---

# 2. Architectural Goals

The architecture has been designed to satisfy the following principles:

- Simplicity over complexity
- Clean architecture
- Modular components
- Easy maintenance
- Easy deployment
- Easy migration to commercial AI providers
- Minimal infrastructure
- Local execution support
- Cloud deployment support

---

# 3. High Level Architecture

```
                        User

                          │

                  Streamlit Web UI

                ┌─────────┴─────────┐

                │                   │

            Chat Interface      Admin Panel

                │                   │

                └─────────┬─────────┘

                          │

                    Application Core

          ┌───────────────┼────────────────┐

          │               │                │

     Chat Service   Document Service   Authentication

          │               │

          └───────────────┬───────────────┘

                          │

                    Vector Database

                      ChromaDB

                          │

                    Embedding Model

                          │

                  Document Processing

                          │

 PDF • DOCX • TXT • CSV • MD • JSON • HTML

```

---

# 4. Architectural Style

The project follows a modular monolithic architecture.

Reasons:

- Small application
- Easy deployment
- Simple maintenance
- Fast development
- Minimal configuration
- Perfect fit for Streamlit

No microservices are required.

No distributed architecture is required.

---

# 5. Main Components

## Streamlit UI

Responsible for:

- User interface
- Chat window
- File upload
- Admin authentication
- Sidebar
- Displaying references
- Status messages

---

## Chat Service

Responsible for:

- Receiving user questions
- Preparing prompts
- Sending requests to the LLM
- Returning formatted answers

This module never accesses documents directly.

---

## Document Service

Responsible for:

- Uploading files
- Validating formats
- Loading documents
- Chunking
- Generating embeddings
- Updating ChromaDB

---

## Authentication

A lightweight administrator authentication system.

The application does not implement user accounts.

Only one administrator password is required.

Administrator permissions:

- Upload documents
- Delete documents
- Rebuild Vector Database

Regular users can only:

- Ask questions

---

## Vector Database

Technology:

ChromaDB

Responsibilities:

- Store embeddings
- Persist vectors
- Similarity search
- Metadata storage

Persistence is automatic.

---

## Embedding Service

Responsible for converting document chunks into vector representations.

Initially local HuggingFace embeddings will be used.

This component should be replaceable without modifying the rest of the application.

---

## LLM Provider

The architecture abstracts the language model provider.

Initial provider:

OpenRouter

The project should support changing providers simply by editing environment variables.

Future compatible providers:

- OpenAI
- Gemini
- Claude
- Cohere
- Groq
- Local Ollama

---

# 6. Document Processing Pipeline

When an administrator uploads documents, the following workflow is executed:

```
Upload Files

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

↓

Ready
```

---

# 7. Question Answering Pipeline

```
User Question

↓

Retriever

↓

Relevant Chunks

↓

Prompt Builder

↓

LLM

↓

Answer

↓

Display Sources
```

---

# 8. Supported File Formats

The system will support:

- PDF
- DOCX
- TXT
- CSV
- Markdown
- JSON
- HTML

The architecture should allow new loaders to be added without changing existing modules.

---

# 9. Security

The application is public.

Only the document management area is protected.

Authentication is based on a password stored as an environment variable.

No user database is required.

No session persistence is required.

---

# 10. Error Handling

The system should gracefully handle:

- Invalid files
- Unsupported formats
- Empty documents
- Corrupted documents
- LLM failures
- Embedding failures
- ChromaDB failures

The user should always receive friendly error messages.

---

# 11. Logging

The application should generate logs for:

- Uploaded documents
- Deleted documents
- Index creation
- User questions
- LLM responses
- Errors

The objective is debugging, not auditing.

---

# 12. Scalability

Although this project is intentionally simple, the architecture should support:

- More document types
- Larger document collections
- Better embedding models
- Different vector databases
- Different LLM providers

without major code changes.

---

# 13. Deployment

The application should run identically in:

- Local development
- Streamlit Community Cloud
- Render

The deployment process must only require environment variables.

---

# 14. Directory Responsibilities

```
src/

    app/

        ui/

        services/

        rag/

        loaders/

        embeddings/

        llm/

        auth/

        config/

        utils/

```

Each module must have a single responsibility.

---

# 15. Design Principles

The project follows:

- KISS (Keep It Simple, Stupid)
- DRY (Don't Repeat Yourself)
- Separation of Concerns
- Low Coupling
- High Cohesion
- Configuration over Hardcoding

---

# 16. Future Improvements

Possible future enhancements:

- User accounts

- Role Based Access

- Conversation history

- Document versioning

- OCR support

- Image processing

- Voice interaction

- Agentic workflows

These features are intentionally excluded from the current version.

---

# 17. Out of Scope

The following features are intentionally excluded:

- Multi-agent systems
- SQL databases
- Docker orchestration
- Kubernetes
- Authentication providers
- Payment systems
- Analytics dashboards
- REST API
- React frontend

The goal is to keep the project focused, maintainable and suitable for the requirements.

---

# 18. Success Criteria

The architecture will be considered successful if:

- The application answers questions accurately.
- Documents can be uploaded dynamically.
- The vector database updates correctly.
- The administrator area is protected.
- Deployment works in cloud services.
- Switching LLM providers requires only configuration changes.
- The codebase remains simple and understandable.
