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
- Fly.io deployment (recommended)
- VPS/Cloud deployment
- Docker containerization
- Environment variables
- Persistent data
- Deployment requirements
- Backup strategies

This specification does not cover:

- Kubernetes orchestration
- Docker Swarm
- CI/CD pipelines (beyond basic deployment)
- Load balancing across multiple instances
- Advanced auto-scaling

These topics may be addressed in future versions.

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

| Platform          | Status       | Persistence | Recommended For     |
| ----------------- | ------------ | ----------- | ------------------- |
| Local Development | ✅ Supported | Full        | Development, Testing |
| Fly.io            | ✅ Supported | Full        | Production ⭐       |
| VPS/Cloud         | ✅ Supported | Full        | Enterprise          |

**Fly.io** is the recommended production deployment platform due to:
- Persistent volumes (data survives deployments)
- Free tier with 3GB storage
- Global edge network
- Automatic HTTPS
- Simple CLI-based deployment

Future versions may support:
- Docker Compose orchestration
- Railway
- AWS App Runner
- Google Cloud Run
- Azure Container Apps

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

# 9. Fly.io Deployment (Recommended)

The application is optimized for deployment on Fly.io.

Requirements:
- flyctl CLI installed
- Fly.io account (free tier available)
- GitHub repository (for source code)
- API keys for LLM providers

Key Features:
- **Persistent volumes**: Data survives deployments and restarts
- **Automatic HTTPS**: SSL certificates included
- **Global CDN**: Deploy close to users
- **Health checks**: Automatic monitoring
- **Zero-downtime deploys**: Rolling deployment strategy

Configuration files:
- `fly.toml` - Fly.io configuration
- `Dockerfile` - Container image definition
- `.dockerignore` - Build optimization

Deployment workflow:

```
Install flyctl

↓

Authenticate (flyctl auth login)

↓

Create App (flyctl launch --no-deploy)

↓

Create Volume (flyctl volumes create techflow_data --size 3)

↓

Configure Secrets (flyctl secrets set ...)

↓

Deploy (flyctl deploy)

↓

Application Ready at https://app-name.fly.dev
```

Example commands:

```bash
# Initial setup
flyctl launch --no-deploy --name techflow-rag-agent --region mia
flyctl volumes create techflow_data --size 3 --region mia

# Configure secrets
flyctl secrets set GEMINI_API_KEY="your-key"
flyctl secrets set COHERE_API_KEY="your-key"
flyctl secrets set ADMIN_PASSWORD="secure-password"

# Deploy
flyctl deploy

# Monitor
flyctl logs
flyctl status
```

Helper script available:
```bash
./.fly/deploy.sh setup
./.fly/deploy.sh secrets
./.fly/deploy.sh deploy
```

Limitations:
- Free tier: 256MB RAM (upgradable)
- Requires credit card for verification (no charge on free tier)

This deployment target is recommended for production use.

---

# 10. VPS/Cloud Deployment (Alternative)

For organizations requiring full control, deployment on VPS or cloud infrastructure is supported.

Supported Platforms:
- DigitalOcean Droplets
- AWS EC2
- Google Cloud Compute Engine
- Azure Virtual Machines
- Any Linux VPS

Requirements:
- Linux server (Ubuntu 22.04 LTS recommended)
- Python 3.11+
- systemd (for service management)
- Nginx (optional, for reverse proxy and HTTPS)

Recommended settings:

Minimum Resources:
- 2GB RAM
- 2 CPU cores
- 20GB disk space

Runtime:
Python 3.11+

Installation:

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clone repository
git clone <repository>
cd techflow-rag-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Configure environment
nano .env

# Run setup
python setup.py
```

Start Command:

```bash
streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
```

Service Management (systemd):
See `docs/DEPLOYMENT.md` for complete systemd configuration.

This deployment target provides maximum control and is suitable for enterprise deployments.

---

# 11. Docker Support

The application includes Docker support for containerized deployments.

Files:
- `Dockerfile` - Optimized multi-stage build
- `docker-compose.yml` - Local development with Docker
- `.dockerignore` - Build optimization

Docker Image Features:
- Based on Python 3.11-slim
- Health checks included
- Automatic directory creation
- Volume support for data persistence

Local Docker deployment:

```bash
# Build and run with docker-compose
docker-compose up -d

# Or build manually
docker build -t techflow-rag-agent .
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="your-key" \
  -e ADMIN_PASSWORD="password" \
  -v $(pwd)/data:/app/data \
  techflow-rag-agent
```

The Docker image is used by Fly.io for production deployments.

---

# 12. Runtime Configuration

The application should automatically:

- Create missing folders
- Initialize ChromaDB
- Validate configuration
- Load config.json
- Load environment variables

Manual setup should be minimized.

---

# 13. Startup Validation

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

# 14. Logging

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

# 15. Updating the Application

Recommended update workflow:

**Fly.io:**
```
Pull Latest Changes (git pull)

↓

Deploy (flyctl deploy)

↓

Application Updated (data persists automatically)
```

**VPS/Local:**
```
Pull Latest Changes

↓

Install Updated Dependencies

↓

Restart Application
```

Existing Knowledge Assets should remain intact across updates.

On Fly.io, the persistent volume ensures data survival between deployments.

---

# 16. Backup Strategy

Recommended backup targets:

- data/knowledge_library/
- data/chromadb/
- data/config.json

These directories contain all user-generated content.

The source code can always be restored from GitHub.

**Fly.io Backups:**
```bash
# Create volume snapshot
flyctl volumes snapshots create techflow_data

# List snapshots
flyctl volumes snapshots list techflow_data

# Restore from snapshot (create new volume)
flyctl volumes create techflow_data_restored --snapshot-id snap_xxxxx
```

**VPS Backups:**
Use standard backup tools (rsync, tar, etc.) to backup the `data/` directory.

---

# 17. Security Considerations

Deployment should follow these practices:

- Never commit `.env`
- Never expose API keys
- Keep administrator password private
- Validate uploaded files
- Protect administrative features
- Use HTTPS in production (automatic on Fly.io)
- Keep secrets in environment variables, not code
- Rotate API keys periodically

The application is intended for corporate use and small-to-medium scale deployments.

---

# 18. Acceptance Criteria

This specification is complete when:

- The application runs locally
- The application runs on Fly.io with persistent volumes
- The application runs on VPS/cloud infrastructure
- Environment variables are loaded correctly
- Runtime directories are created automatically
- ChromaDB initializes successfully
- Uploaded assets persist correctly across deployments (Fly.io volumes)
- Startup validation detects configuration problems
- The application warns (but continues) if only one LLM provider is configured
- Both Gemini and Cohere providers work correctly
- Docker image builds successfully
- Health checks function properly
- Backups can be created and restored

---

# 19. Notes for AI Development Agents

Implementation Guidelines

Deployment

- Keep deployment simple.
- Avoid platform-specific code.
- Read configuration from the environment.
- Support Docker for containerized deployments.
- Ensure data persistence through volume mounts.

Startup

- Validate configuration before launching.
- Create missing directories automatically.
- Fail gracefully when configuration is incomplete.
- Test health check endpoints.

Maintainability

- Keep deployment logic isolated.
- Avoid hardcoded paths.
- Support multiple deployment targets.
- Document deployment procedures clearly.

---

# 20. Final Notes

The deployment architecture prioritizes production readiness while maintaining simplicity.

The application should be easy to deploy locally for development, on Fly.io for production (with full data persistence), and on VPS for enterprise deployments requiring maximum control.

Version 1 emphasizes:
- **Data persistence**: No data loss between deployments
- **Simplicity**: Easy setup and maintenance
- **Portability**: Multiple deployment options
- **Production-ready**: HTTPS, health checks, monitoring
- **Cost-effective**: Free tier options available

The recommended deployment path is: Local → Fly.io → VPS (as needs grow).
