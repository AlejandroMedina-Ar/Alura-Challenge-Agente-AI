# Deployment Specification

**Specification ID:** SPEC-006

**Module:** Deployment

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the deployment strategy for the TechFlow Solutions Corporate Knowledge Agent.

The primary objective is to provide a simple, reliable and reproducible deployment process.

Version 1 prioritizes ease of deployment over scalability.

---

# 2. Scope

This specification covers:

- Local development
- Streamlit Cloud deployment
- Render deployment
- Environment variables
- Persistent data
- Deployment requirements

This specification does not cover:

- Kubernetes
- Docker Swarm
- Docker containers (v1 deploys as native Python applications only)
- CI/CD pipelines
- Load balancing
- Multi-server deployments

These topics are outside the scope of v1.

---

# 3. Deployment Philosophy

The deployment process should follow these principles:

- Simple
- Fast
- Reproducible
- Cloud-ready
- Minimal configuration

The application should be deployable without modifying the source code.

---

# 4. Supported Deployment Targets

Version 1 officially supports:

| Platform                  | Status       |
| ------------------------- | ------------ |
| Local Development         | ✅ Supported |
| Streamlit Community Cloud | ✅ Supported |
| Render                    | ✅ Supported |

Future versions may support:

- Docker (single container, no orchestration)
- Railway
- OCI Cloud Service
- Azure App Service
- AWS
- Google Cloud Run

---

# 5. Local Development

Minimum requirements:

- Python 3.11+
- Git
- Virtual Environment
- Internet connection for cloud LLMs

Installation workflow:

```
Clone Repository

↓

Create Virtual Environment

↓

Install Requirements

↓

Copy .env.example to .env

↓

Configure .env (API keys, passwords)

↓

Run Streamlit

↓

Application Ready
```

Example:

```bash
git clone <repository>

cd techflow-rag-agent

python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

# Edit .env with your API keys and passwords

streamlit run src/app.py
```

---

# 6. Required Project Structure

The deployment expects the following structure:

```
techflow-rag-agent/

├── src/

│   ├── app.py

│   ├── ui/

│   ├── services/

│   ├── rag/

│   ├── llm/

│   ├── storage/

│   ├── auth/

│   ├── config/

│   └── utils/

├── assets/

├── data/  (created at runtime)

├── specs/

├── architecture/

├── prompts/

├── requirements.txt

├── .env.example

└── README.md
```

The application should create missing runtime directories (data/, data/logs/, data/chromadb/, data/knowledge_library/) automatically when possible.

---

# 7. Environment Variables

Deployment depends on environment variables.

Required:

```
ADMIN_PASSWORD

GEMINI_API_KEY (or COHERE_API_KEY - at least one)

EMBEDDING_MODEL
```

Recommended (for full functionality):

```
GEMINI_API_KEY

COHERE_API_KEY

GEMINI_MODEL

COHERE_MODEL
```

Optional:

```
CHROMA_DB_PATH

CHUNK_SIZE

CHUNK_OVERLAP

TEMPERATURE

MAX_CONTEXT_CHUNKS

MAX_OUTPUT_TOKENS

LOG_LEVEL

LOG_FILE
```

Sensitive values should never be committed to Git.

---

# 8. Persistent Data

The application stores runtime data separately from the source code.

Recommended structure:

```
data/

    knowledge_library/

        documents/

        metadata/

    chromadb/

    logs/

    config.json
```

This directory contains:

- Uploaded Knowledge Assets
- ChromaDB persistent storage
- Application logs
- Runtime configuration

**Note:** The `data/` directory is created automatically at runtime if it doesn't exist.

---

# 9. Streamlit Community Cloud

The application should be compatible with Streamlit Community Cloud.

Requirements:

- Public GitHub repository
- requirements.txt
- Environment variables configured through Streamlit Secrets

Limitations:

- Limited persistent storage
- CPU and memory restrictions

This deployment target is recommended for demonstrations.

---

# 10. Render Deployment

Render provides better persistence than Streamlit Cloud.

Requirements:

- GitHub repository
- Python environment
- Environment variables
- Persistent disk (recommended)

Recommended settings:

Runtime:

Python

Build Command:

```
pip install -r requirements.txt
```

Start Command:

```
streamlit run src/app.py --server.port=$PORT --server.address=0.0.0.0
```

---

# 11. Runtime Configuration

The application should automatically:

- Create missing folders
- Initialize ChromaDB
- Validate configuration
- Load config.json
- Load environment variables

Manual setup should be minimized.

---

# 12. Startup Validation

During startup, verify:

- Required directories exist (create if missing: data/, data/logs/, data/chromadb/, data/knowledge_library/)
- Environment variables are valid
- At least one LLM provider key is configured (GEMINI_API_KEY or COHERE_API_KEY)
- ChromaDB is available
- Embedding model can be loaded

If validation fails, display a clear error message.

**Warning conditions (non-blocking):**
- Only one LLM provider configured (warn that fallback is unavailable)
- Optional configuration missing (use defaults)

---

# 13. Logging

Application logs should be stored in:

```
data/logs/
```

Suggested log file:

```
application.log
```

Logging should help diagnose deployment issues.

---

# 14. Updating the Application

Recommended update workflow:

```
Pull Latest Changes

↓

Install Updated Dependencies

↓

Restart Application
```

Existing Knowledge Assets should remain intact.

---

# 15. Backup Strategy

Recommended backup targets:

- data/knowledge_library/
- data/chromadb/
- data/config.json

These directories contain all user-generated content.

The source code can always be restored from GitHub.

---

# 16. Security Considerations

Deployment should follow these practices:

- Never commit `.env`
- Never expose API keys
- Keep administrator password private
- Validate uploaded files
- Protect administrative features

The application is intended for educational use and small-scale deployments.

---

# 17. Acceptance Criteria

This specification is complete when:

- The application runs locally
- The application runs on Streamlit Community Cloud
- The application runs on Render
- Environment variables are loaded correctly
- Runtime directories are created automatically
- ChromaDB initializes successfully
- Uploaded assets persist correctly
- Startup validation detects configuration problems
- The application warns (but continues) if only one LLM provider is configured
- Both Gemini and Cohere providers work correctly

---

# 18. Notes for AI Development Agents

Implementation Guidelines

Deployment

- Keep deployment simple.
- Avoid platform-specific code.
- Read configuration from the environment.

Startup

- Validate configuration before launching.
- Create missing directories automatically.
- Fail gracefully when configuration is incomplete.

Maintainability

- Keep deployment logic isolated.
- Avoid hardcoded paths.
- Support multiple deployment targets.

---

# 19. Final Notes

The deployment architecture is intentionally lightweight.

The application should be easy to deploy locally for development, on Streamlit Community Cloud for demonstrations, and on Render for more stable public hosting.

Version 1 prioritizes simplicity, portability and ease of maintenance while remaining flexible enough to support future deployment targets.
