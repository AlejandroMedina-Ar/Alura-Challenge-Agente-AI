# Project Overview

**Project Name:** TechFlow AI Corporate Knowledge Agent

**Repository:** Alura-Challenge-Agente-AI

**Version:** 1.0

**Status:** Draft

**Author:** Oscar Alejandro Medina

---

# 1. Purpose

This document provides the functional overview of the TechFlow AI Corporate Knowledge Agent.

It defines the project's vision, objectives, scope, constraints and development roadmap.

This document serves as the entry point to the project's documentation.

Detailed software architecture is defined in:

```
architecture/Architecture.md
```

Detailed functional behavior is defined in the individual specifications under the `specs/` directory.

---

# 2. Project Vision

TechFlow AI is an internal corporate knowledge assistant capable of answering natural language questions based exclusively on company documentation.

Instead of forcing employees to manually search dozens of PDF files, Word documents, spreadsheets or internal manuals, the assistant retrieves relevant information and generates contextual answers with references to the original documentation.

The project demonstrates how Retrieval-Augmented Generation (RAG) can transform static documentation into an intelligent conversational knowledge base while remaining simple, maintainable and inexpensive to deploy.

---

# 3. Business Problem

Organizations accumulate large amounts of documentation over time.

Employees frequently waste valuable time searching through multiple documents to locate information.

Typical sources include:

- User manuals
- Internal procedures
- Technical documentation
- Product documentation
- Company policies
- FAQs
- Contracts
- Pricing information

The goal of this project is to centralize that knowledge into an AI assistant capable of answering questions using only the organization's documentation.

---

# 4. Project Goals

## Primary Goals

- Build a fully functional AI-powered knowledge assistant.
- Demonstrate a complete Retrieval-Augmented Generation (RAG) workflow.
- Support dynamic document uploads.
- Deploy the application publicly.
- Produce a professional GitHub repository.

---

## Secondary Goals

- Keep the project simple.
- Minimize infrastructure costs.
- Support free-tier deployment.
- Allow easy migration between LLM providers.
- Demonstrate an AI-assisted software development workflow.

---

# 5. Project Scope

Version 1 includes:

- AI chat interface
- Dynamic Knowledge Library
- Automatic document indexing
- Semantic search
- Source attribution
- Password-protected Administrator Panel
- Cloud deployment
- Dual LLM provider with automatic fallback (Gemini primary, Cohere fallback)

---

# Out of Scope

The following features are intentionally excluded from v1:

- User registration
- Multiple administrator accounts
- Role-based permissions
- OCR
- Voice interaction
- REST API
- Mobile applications
- Docker containers (orchestration or standalone)
- Kubernetes
- Multi-agent systems
- Persistent conversation history (saved chats across sessions)
- Analytics dashboards

**Note on Conversation Memory:** v1 includes session-based conversation memory (current chat only) using Streamlit session state. Persistent conversation history (saved chats across sessions) is explicitly out of scope.

These capabilities may be considered in future versions.

---

# 6. Target Users

The application defines two user profiles.

## Administrator

Responsible for managing the Knowledge Library.

Capabilities:

- Authenticate using an administrator password.
- Upload Knowledge Assets.
- Remove Knowledge Assets.
- Rebuild the Knowledge Library index.
- Monitor indexing status.

---

## Regular User

Responsible only for interacting with the assistant.

Capabilities:

- Ask questions.
- Receive contextual answers.
- View document references.

No authentication is required.

---

# 7. Functional Overview

The application follows a simple business workflow.

```
Administrator

↓

Upload Knowledge Assets

↓

Knowledge Library Updated

↓

Users Ask Questions

↓

Relevant Information Retrieved

↓

AI Generates Contextual Answer

↓

Sources Displayed
```

Implementation details of this workflow are defined in:

- architecture/Architecture.md
- specs/004-rag-pipeline.md

---

# 8. Core Features

Version 1 provides the following functionality.

### AI Chat

Natural language interaction with the Knowledge Library.

---

### Dynamic Knowledge Library

Knowledge Assets can be uploaded or removed without modifying the application's source code.

---

### Automatic Indexing

Uploaded assets are processed and indexed automatically.

---

### Semantic Retrieval

Relevant information is retrieved using vector similarity search.

---

### Source Attribution

Generated answers should reference the Knowledge Assets used whenever possible.

---

### Administrator Panel

Administrative functions are protected by password authentication.

---

### Cloud Deployment

The application can be deployed using free-tier cloud services.

---

### Multi-language Support

Documents in English, Spanish, and Portuguese are supported. Language detection is automatic but does not affect processing in v1 (future enhancement: language-specific embedding models).

---

# 9. Supported Knowledge Assets

Version 1 supports:

- PDF
- DOCX
- TXT
- Markdown
- CSV
- JSON
- HTML

Support for additional formats may be added in future versions.

---

# 10. Technology Stack

| Layer           | Technology                         |
| --------------- | ---------------------------------- |
| Language        | Python                             |
| User Interface  | Streamlit                          |
| AI Framework    | LangChain                          |
| Vector Database | ChromaDB                           |
| Embeddings      | HuggingFace Sentence Transformers  |
| LLM Provider    | Google Gemini (primary), Cohere (fallback) |
| Configuration   | python-dotenv                      |
| Version Control | Git                                |
| Repository      | GitHub                             |
| Deployment      | Streamlit Community Cloud / Render |

The selected stack prioritizes simplicity, maintainability and free-tier compatibility.

---

# 11. Development Philosophy

The project follows a pragmatic software engineering approach.

Core principles include:

- Simplicity over complexity
- Rapid development
- Maintainability
- AI-assisted software engineering
- Free-tier first (Gemini free tier as primary LLM)
- Configuration over hardcoding

Detailed architectural principles are documented in:

```
architecture/Architecture.md
```

---

# 12. Project Constraints

Every technical decision should respect the following constraints.

- Prefer free-tier services.
- Minimize dependencies.
- Avoid unnecessary complexity.
- Prioritize readability.
- Support local execution.
- Support cloud deployment.
- Keep installation simple.

These constraints guide all implementation decisions.

---

# 13. Stable Decisions

v1 intentionally fixes several high-level project decisions.

- Python is the implementation language.
- Streamlit is the user interface.
- LangChain orchestrates the AI workflow.
- ChromaDB stores vector embeddings.
- Google Gemini is the primary LLM provider with Cohere as automatic fallback.
- Knowledge Assets are uploaded dynamically.
- Administrative functions are password protected.

Detailed implementation of these decisions is documented in `architecture/Architecture.md`.

---

# 14. AI Development Workflow

The project is intentionally developed using AI-assisted software engineering.

---

### Cursor

Responsibilities:

- Code generation
- Refactoring
- Bug fixing
- Productivity

---

### GitHub

Responsibilities:

- Version control
- Repository hosting
- Documentation
- Project delivery

---

# 15. Success Criteria

The project will be considered complete when:

- Users can ask questions naturally.
- Knowledge Assets can be uploaded dynamically.
- The Knowledge Library indexes correctly.
- Contextual answers are generated successfully.
- Sources are displayed whenever possible.
- Administrative features are protected.
- The application is publicly deployed.
- Documentation is complete.
- The repository is organized and maintainable.

---

# 16. Development Roadmap

The project is developed incrementally.

| Phase                     | Status       |
| ------------------------- | ------------ |
| Project Planning          | ✅ Completed |
| Architecture              | ✅ Completed |
| Functional Specifications | ✅ Completed |
| Repository Structure      | ✅ Completed |
| Implementation            | ⏳ Pending   |
| Testing                   | ⏳ Pending   |
| Deployment                | ⏳ Pending   |
| Final Documentation       | ⏳ Pending   |

---

# 17. Documentation Structure

The project documentation is organized as follows.

```
README.md

↓

specs/000-project-overview.md

↓

architecture/Architecture.md

↓

specs/

    001-chat-interface.md

    002-knowledge-base-management.md

    003-authentication.md

    004-rag-pipeline.md

    005-configuration.md

    006-deployment.md
```

Each document has a single responsibility.

Project Overview explains **what** the project is.

Architecture explains **how** the system is organized.

Specifications describe **how each module behaves**.

---

# 18. References

This document should be read together with:

- architecture/Architecture.md
- specs/001-chat-interface.md
- specs/002-knowledge-base-management.md
- specs/003-authentication.md
- specs/004-rag-pipeline.md
- specs/005-configuration.md
- specs/006-deployment.md

Together these documents define the complete functional and technical specification of the project.
