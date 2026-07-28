# TechFlow AI RAG Agent - Docker Image para Fly.io
# 
# Multi-stage build optimizado para Fly.io
# Base image: Python 3.11 slim

FROM python:3.11-slim as base

# Labels para Fly.io
LABEL fly_launch_runtime="python"
LABEL maintainer="TechFlow Solutions"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8501

# Create app directory
WORKDIR /app

# Install system dependencies (optimizado para Fly.io)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
# En Fly.io, /app/data será montado como volumen persistente
RUN mkdir -p data/chromadb \
    data/knowledge_library/documents \
    data/knowledge_library/metadata \
    data/logs

# Crear archivo de configuración por defecto si no existe
RUN mkdir -p data && \
    if [ ! -f data/config.json ]; then \
        echo '{"llm":{"provider":"gemini","model":"gemini-3.6-flash","api_key":""},"rag":{"chunk_size":1000,"chunk_overlap":200,"top_k":5,"temperature":0.7},"ui":{"theme":"light"}}' > data/config.json; \
    fi

# Expose Streamlit port
EXPOSE 8501

# Health check (Fly.io usa su propio sistema, pero esto es útil localmente)
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set the entrypoint para Fly.io
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]
