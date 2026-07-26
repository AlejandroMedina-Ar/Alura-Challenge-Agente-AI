# Implementation Rules

## TechFlow Solutions Corporate Knowledge Agent

Version: 1.0

---

# Purpose

This document defines the implementation rules that the AI coding agent must follow while generating or modifying code for this project.

These rules complement the project specifications and architecture.

They do not replace them.

---

# Required Reading Order

Before implementing any feature, always read:

1. `architecture/Architecture.md`
2. `specs/000-project-overview.md`
3. The corresponding module specification
4. `prompts/system-prompt.md`
5. This document

Never implement features without understanding the relevant specification first.

---

# General Principles

Always follow:

- KISS (Keep It Simple, Stupid)
- DRY (Don't Repeat Yourself)
- SOLID (only when it improves readability)
- Separation of Concerns
- Configuration over Hardcoding

Prefer simple solutions.

Avoid unnecessary abstractions.

Avoid premature optimization.

---

# Python Standards

Use:

- Python 3.12+
- PEP8
- Type hints
- Meaningful variable names
- Descriptive function names

Every function should perform one clear task.

Avoid functions longer than approximately 50 lines whenever practical.

Avoid deeply nested code.

---

# Code Organization

Respect the existing project structure.

Never create new folders unless explicitly requested.

Never duplicate modules.

Reuse existing services whenever possible.

Business logic must never be placed inside Streamlit pages.

---

# Streamlit Rules

The UI is responsible only for:

- displaying information
- collecting user input
- calling services

The UI must never contain:

- RAG logic
- embedding generation
- vector database operations
- authentication logic
- configuration loading

Keep pages clean and lightweight.

---

# UI Implementation Rules

**Technology:** Streamlit-only (Python)

**Strictly Forbidden:**
- Custom HTML generation for navigation or layout
- JavaScript code
- Complex CSS beyond theming
- Custom React components
- iframe embeds

**Allowed:**
- `assets/css/dark.css` - Dark theme styling only
- `assets/css/light.css` - Light theme styling only
- Streamlit native components (`st.sidebar`, `st.chat_message`, etc.)
- Streamlit's hamburger menu (⋮) for settings

**Layout Strategy:**
- **NO custom top navigation bar** - Use Streamlit's native menu
- **Branding in sidebar:** Company logo/name at top of `st.sidebar`
- **System status in sidebar:** Use `st.sidebar.metric()` or `st.sidebar.info()`
- **Settings via Streamlit menu:** Theme selection through built-in settings

**Theme Implementation:**
- Detect Streamlit's theme setting (`st.get_option("theme.base")`)
- Load appropriate CSS file (dark.css or light.css)
- Apply via `st.markdown()` with `unsafe_allow_html=True`
- Default to dark mode (Tokyo Night palette)

**Example:**
```python
# Correct: Use Streamlit native components
st.sidebar.title("🤖 TechFlow Solutions")
st.sidebar.info("✓ System Ready")

# Wrong: Custom HTML navigation
# st.markdown("<div class='topnav'>...</div>", unsafe_allow_html=True)  # FORBIDDEN
```

---

# Services

Business logic belongs inside services.

Examples:

- ChatService
- KnowledgeLibraryService
- AuthenticationService
- ConfigurationService
- IndexingService

Services should not depend on the UI.

**Service Naming Convention:** Use `<domain>_service.py` format consistently (e.g., `authentication_service.py`, not `auth_service.py`).

---

# Configuration

Never hardcode:

- passwords
- API keys
- URLs
- model names
- file paths

Secrets belong only inside:

```
.env
```

Examples:
- ADMIN_PASSWORD
- GEMINI_API_KEY
- COHERE_API_KEY

Runtime settings belong only inside:

```
data/config.json
```

Always use the configuration layer instead of accessing configuration files directly.

---

# File System

Store runtime data only inside:

```
data/
```

Examples:

```
data/

knowledge_library/

chromadb/

logs/

config.json
```

Never write runtime files outside this directory.

---

# Logging

Never use:

```python
print(...)
```

Always use the project logger.

Store logs inside:

```
data/logs/
```

Use appropriate logging levels:

- DEBUG
- INFO
- WARNING
- ERROR

---

# Error Handling

Never expose stack traces to end users.

Catch expected exceptions.

Display friendly messages.

Log technical details.

Never silently ignore errors.

---

# Knowledge Base

Never hardcode documents.

Always use the knowledge library.

Documents:

```
data/knowledge_library/documents/
```

Metadata:

```
data/knowledge_library/metadata/
```

Document processing must remain independent from chat functionality.

**Terminology:** Use "Knowledge Asset" in technical documentation and code, "Document" in user-facing UI.

---

# ChromaDB

Use ChromaDB as the only vector database.

Do not replace it without explicit instructions.

Avoid direct manipulation of vector storage.

Always use the project's vector service.

---

# LLM Providers

The project uses a dual-provider architecture.

Primary provider:

- Google Gemini (free tier)

Fallback provider:

- Cohere

Future compatible providers (not supported in v1):

- OpenAI
- Claude
- Groq
- Ollama (local)

Never write provider-specific code that prevents future migration.

Use an abstraction layer (llm/base_provider.py).

Implement automatic fallback logic as specified in SPEC-004 Section 13.1.

---

# Dependencies

Before introducing a new dependency:

- verify it is really necessary
- prefer actively maintained libraries
- avoid duplicate functionality

Never increase project complexity unnecessarily.

---

# Documentation

Whenever adding:

- modules
- classes
- public functions

Include appropriate docstrings.

Avoid obvious comments.

Explain why, not what.

---

# Naming Conventions

Use descriptive names.

Examples:

Good:

```python
load_documents()

generate_embeddings()

retrieve_context()

build_prompt()

save_configuration()
```

Avoid:

```python
do()

process()

temp()

run()

handle()
```

---

# Imports

Prefer absolute imports.

Avoid circular dependencies.

Group imports according to PEP8.

Remove unused imports.

---

# Performance

Optimize only when necessary.

Prioritize:

1. readability
2. maintainability
3. correctness

before optimization.

---

# Testing During Development

Before considering any implementation complete, verify:

- imports work
- code executes
- configuration loads
- no syntax errors exist

Do not leave placeholder implementations unless explicitly requested.

---

# Git Workflow

Generate small, focused changes.

Avoid modifying unrelated files.

Preserve formatting consistency.

Do not rename files without explicit instructions.

---

# Forbidden Actions

Do not:

- invent requirements
- redesign the architecture
- replace selected technologies
- hardcode secrets
- bypass the service layer
- place business logic inside the UI
- introduce unnecessary frameworks
- duplicate existing code

When in doubt, ask for clarification.

---

# Definition of Done

A task is considered complete only if:

- The implementation matches the specification.
- The architecture remains respected.
- Code is readable.
- No duplicated logic exists.
- Configuration is externalized.
- Logging is implemented where appropriate.
- Errors are handled gracefully.
- Existing functionality is not broken.

---

# Implementation Checklist

Before considering any implementation complete, verify all of the following:

## Architecture

- [ ] The implementation follows `architecture/Architecture.md`.
- [ ] No architectural decisions were modified.

---

## Functional Requirements

- [ ] The corresponding specification has been fully implemented.
- [ ] No undocumented functionality has been added.

---

## Code Quality

- [ ] Code is readable.
- [ ] Code is modular.
- [ ] No duplicated logic exists.
- [ ] Functions have a single responsibility.
- [ ] Naming conventions are respected.

---

## Configuration

- [ ] No secrets are hardcoded.
- [ ] Runtime configuration uses `data/config.json`.
- [ ] Secrets use `.env`.

---

## Logging & Errors

- [ ] Logging has been added where appropriate.
- [ ] Errors are handled gracefully.
- [ ] No stack traces are exposed to users.

---

## Project Structure

- [ ] Files are located in the correct directories.
- [ ] No unnecessary files or folders were created.

---

## Validation

- [ ] Imports are valid.
- [ ] No syntax errors exist.
- [ ] Existing functionality remains unchanged.

---

Only when every item above is satisfied should the task be considered complete.

# Final Rule

The project documentation is the single source of truth.

If implementation decisions conflict with assumptions, always follow:

1. Architecture.md
2. Relevant specification
3. system-prompt.md
4. This document

Never guess requirements.

Implement only what has been specified.
