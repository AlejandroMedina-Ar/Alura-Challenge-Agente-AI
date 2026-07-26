# 🚀 TechFlow AI - Deployment Guide

**Complete guide for deploying TechFlow AI RAG Agent**

---

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Considerations](#production-considerations)
6. [Monitoring](#monitoring)
7. [Backup & Recovery](#backup--recovery)
8. [Scaling](#scaling)

---

## Deployment Options

### Option 1: Local Deployment
- **Pros:** Simple, no Docker needed, direct access
- **Cons:** Manual setup, OS-dependent
- **Best for:** Development, testing, single-user

### Option 2: Docker
- **Pros:** Consistent environment, easy deployment, portable
- **Cons:** Requires Docker, slight overhead
- **Best for:** Production, multi-environment, reproducible

### Option 3: Streamlit Community Cloud
- **Pros:** Free hosting, automatic deployment, HTTPS
- **Cons:** Public repository required, limited resources
- **Best for:** Demos, public projects, free tier

### Option 4: Cloud VM (AWS, GCP, Azure)
- **Pros:** Full control, scalable, secure
- **Cons:** Costs money, requires DevOps knowledge
- **Best for:** Enterprise, production, high availability

### Option 5: Kubernetes
- **Pros:** Highly scalable, resilient, cloud-native
- **Cons:** Complex setup, overkill for small apps
- **Best for:** Large-scale, multi-instance deployments

---

## Local Deployment

### Prerequisites

- Python 3.9 or higher
- pip package manager
- 2GB RAM minimum
- 1GB free disk space

### Step-by-Step

```bash
# 1. Clone repository
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run setup
python setup.py

# 6. Start application
python run.py
# or: streamlit run src/app.py
```

### Access

Open browser at: **http://localhost:8501**

### Stopping

Press `Ctrl+C` in terminal

---

## Docker Deployment

### Prerequisites

- Docker installed
- Docker Compose (optional but recommended)
- 4GB RAM minimum

### Quick Start with Docker Compose

```bash
# 1. Clone repository
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 3. Build and start
docker-compose up -d

# 4. Check logs
docker-compose logs -f

# 5. Access application
# Open http://localhost:8501
```

### Using Docker Directly

```bash
# Build image
docker build -t techflow-ai:latest .

# Run container
docker run -d \
  --name techflow-ai \
  -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  -e COHERE_API_KEY=your_key \
  -e ADMIN_PASSWORD=secure_password \
  -v $(pwd)/data:/app/data \
  techflow-ai:latest

# Check logs
docker logs -f techflow-ai

# Stop container
docker stop techflow-ai

# Remove container
docker rm techflow-ai
```

### Docker Management

```bash
# List running containers
docker ps

# View logs
docker logs techflow-ai

# Access container shell
docker exec -it techflow-ai bash

# Restart container
docker restart techflow-ai

# Stop all
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Data Persistence

Data is persisted in Docker volumes:
- ChromaDB: `./data/chromadb`
- Documents: `./data/knowledge_library`
- Logs: `./data/logs`
- Config: `./data/config.json`

---

## Cloud Deployment

### Streamlit Community Cloud

**Free hosting for Streamlit apps**

#### Prerequisites
- GitHub account
- Public repository (or paid Streamlit plan)
- API keys

#### Steps

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

3. **Deploy App:**
   - Click "New app"
   - Select repository
   - Branch: `main`
   - Main file: `src/app.py`

4. **Configure Secrets:**
   - Click "Advanced settings"
   - Add secrets in TOML format:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   COHERE_API_KEY = "your_key_here"
   ADMIN_PASSWORD = "secure_password"
   ```

5. **Deploy:**
   - Click "Deploy"
   - Wait for build (3-5 minutes)
   - Access your app at: `https://your-app.streamlit.app`

#### Limitations
- 1GB RAM limit
- CPU throttling
- Public by default
- Limited to 3 apps on free tier

### AWS EC2

**Deploy on Amazon EC2 instance**

#### Launch Instance

```bash
# 1. Launch EC2 instance
# - Ubuntu 22.04 LTS
# - t2.medium (4GB RAM)
# - 20GB storage
# - Allow HTTP (80), HTTPS (443), Custom TCP (8501)

# 2. Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Update system
sudo apt update && sudo apt upgrade -y

# 4. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 5. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 6. Clone repository
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 7. Configure
nano .env
# Add your API keys

# 8. Deploy
docker-compose up -d

# 9. Setup reverse proxy (optional, for HTTPS)
# See Nginx section below
```

#### Access
- HTTP: `http://your-ec2-ip:8501`
- HTTPS: Configure Nginx + Let's Encrypt (see below)

### Google Cloud Platform (GCP)

**Deploy on Google Compute Engine**

```bash
# 1. Create VM instance
gcloud compute instances create techflow-ai \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --tags=http-server

# 2. SSH into instance
gcloud compute ssh techflow-ai --zone=us-central1-a

# 3. Follow same steps as AWS EC2 (Docker installation)
```

### Azure

**Deploy on Azure VM**

```bash
# 1. Create VM
az vm create \
  --resource-group techflow-rg \
  --name techflow-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys

# 2. Open port 8501
az vm open-port --port 8501 --resource-group techflow-rg --name techflow-vm

# 3. SSH and deploy
ssh azureuser@your-vm-ip
# Follow Docker deployment steps
```

---

## Production Considerations

### Security

#### 1. Use Strong Passwords
```bash
# Generate secure password
openssl rand -base64 32

# Set in .env
ADMIN_PASSWORD=your_generated_password
```

#### 2. HTTPS with Nginx + Let's Encrypt

**Install Nginx:**
```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

**Configure Nginx:**
```nginx
# /etc/nginx/sites-available/techflow
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/techflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Get SSL certificate:**
```bash
sudo certbot --nginx -d your-domain.com
```

#### 3. Firewall Configuration

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Only allow Streamlit from localhost if using Nginx
sudo ufw deny 8501/tcp
```

#### 4. Environment Variables

**Never commit `.env` to git!**

Use secret management:
- AWS Secrets Manager
- GCP Secret Manager
- Azure Key Vault
- HashiCorp Vault

#### 5. API Key Rotation

Rotate API keys regularly:
```bash
# 1. Generate new keys from provider
# 2. Update .env
# 3. Restart application
docker-compose restart
```

### Performance

#### 1. Resource Allocation

**Minimum:**
- 2GB RAM
- 2 CPU cores
- 10GB storage

**Recommended:**
- 4GB RAM
- 4 CPU cores
- 50GB storage

#### 2. Optimize Docker

```dockerfile
# Use multi-stage builds (already in Dockerfile)
# Minimize layers
# Use .dockerignore
```

#### 3. Database Optimization

```python
# ChromaDB settings in src/rag/vector_store.py
# Adjust batch sizes for large datasets
```

### Reliability

#### 1. Auto-restart

**Docker Compose:**
```yaml
restart: unless-stopped
```

**Systemd Service:**
```ini
# /etc/systemd/system/techflow.service
[Unit]
Description=TechFlow AI RAG Agent
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/Alura-Challenge-Agente-AI
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable techflow
sudo systemctl start techflow
```

#### 2. Health Checks

Already configured in Docker:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

## Monitoring

### Application Logs

**Docker:**
```bash
docker logs -f techflow-ai
```

**Local:**
```bash
tail -f data/logs/application.log
```

### System Monitoring

**Install monitoring tools:**
```bash
# htop for resource monitoring
sudo apt install htop

# Docker stats
docker stats techflow-ai
```

### Application Metrics

Check in Admin Panel → Dashboard:
- Total documents
- Indexed documents
- Vector store size
- Storage used

### Log Aggregation

**Option 1: Loki + Grafana (Advanced)**
```bash
# Setup Loki for log aggregation
# Setup Grafana for visualization
```

**Option 2: CloudWatch (AWS)**
```bash
# Configure CloudWatch agent
# Send logs to CloudWatch
```

---

## Backup & Recovery

### What to Backup

1. **Vector Database:** `data/chromadb/`
2. **Documents:** `data/knowledge_library/`
3. **Configuration:** `data/config.json`
4. **Environment:** `.env` file (keep secure!)

### Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/techflow-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup data
cp -r data/chromadb "$BACKUP_DIR/"
cp -r data/knowledge_library "$BACKUP_DIR/"
cp data/config.json "$BACKUP_DIR/"

# Create archive
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Backup created: $BACKUP_DIR.tar.gz"
```

### Automated Backups

**Cron job:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /home/ubuntu/backup.sh
```

### Recovery

```bash
# 1. Stop application
docker-compose down

# 2. Extract backup
tar -xzf backup-20260725-020000.tar.gz

# 3. Restore data
cp -r backup-20260725-020000/chromadb data/
cp -r backup-20260725-020000/knowledge_library data/
cp backup-20260725-020000/config.json data/

# 4. Start application
docker-compose up -d
```

---

## Scaling

### Vertical Scaling

**Increase resources:**
- More RAM
- More CPU cores
- Faster disk (SSD)

**Docker resource limits:**
```yaml
services:
  techflow-ai:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

### Horizontal Scaling

**Not recommended for this application:**
- ChromaDB is not distributed
- Session state is local
- File storage is local

**For horizontal scaling, need:**
- Distributed vector database (Pinecone, Weaviate)
- Shared session storage (Redis)
- Shared file storage (S3, NFS)

### Load Balancing

**If horizontal scaling:**
```nginx
upstream techflow {
    server 10.0.1.10:8501;
    server 10.0.1.11:8501;
    server 10.0.1.12:8501;
}

server {
    listen 80;
    location / {
        proxy_pass http://techflow;
    }
}
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs techflow-ai

# Check if port is in use
sudo lsof -i :8501

# Rebuild image
docker-compose up -d --build
```

### Out of memory

```bash
# Check memory usage
docker stats

# Increase Docker memory limit
# Docker Desktop: Settings → Resources
```

### Slow performance

- Reduce top-k value
- Increase server resources
- Use SSD for storage
- Check internet connection

---

## Cost Estimates

### Streamlit Community Cloud
- **Cost:** Free (limited resources)

### AWS EC2 (t2.medium)
- **Cost:** ~$30-40/month
- 4GB RAM, 2 vCPUs

### GCP (e2-medium)
- **Cost:** ~$25-35/month
- 4GB RAM, 2 vCPUs

### Azure (B2s)
- **Cost:** ~$30-40/month
- 4GB RAM, 2 vCPUs

### Additional Costs
- Domain name: ~$10-15/year
- SSL certificate: Free (Let's Encrypt)
- Backup storage: ~$1-5/month

---

## Best Practices

✅ **Do:**
- Use HTTPS in production
- Backup data regularly
- Monitor logs
- Update dependencies
- Use strong passwords
- Rotate API keys
- Set up health checks

❌ **Don't:**
- Expose port 8501 directly (use reverse proxy)
- Commit secrets to git
- Run as root in Docker
- Skip backups
- Ignore security updates
- Use default passwords

---

**Need help with deployment?** Check [FAQ](FAQ.md) or open an issue on GitHub.

**Version:** 1.0.0-beta  
**Last Updated:** 2026-07-25
