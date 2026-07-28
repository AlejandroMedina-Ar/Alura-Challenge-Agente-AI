#!/bin/bash

################################################################################
# TechFlow RAG Agent - AWS EC2 Installation Script
# 
# This script automates the complete installation on AWS EC2 (Ubuntu 22.04 LTS)
# Compatible with t2.micro (Free Tier - 1GB RAM)
#
# Usage: bash install.sh
################################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="techflow-rag-agent"
APP_USER="ubuntu"
APP_DIR="/home/ubuntu/techflow-rag-agent"
VENV_DIR="${APP_DIR}/venv"
SERVICE_NAME="techflow-rag"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_error "Do not run this script as root/sudo"
        print_info "Run as regular user: bash install.sh"
        exit 1
    fi
}

################################################################################
# Installation Steps
################################################################################

install_system_dependencies() {
    print_header "Step 1: Installing System Dependencies"
    
    sudo apt-get update -qq
    print_success "Updated package lists"
    
    sudo apt-get install -y -qq \
        python3.11 \
        python3.11-venv \
        python3-pip \
        git \
        curl \
        wget \
        nginx \
        ufw \
        fail2ban \
        htop \
        build-essential \
        python3.11-dev
    
    print_success "System dependencies installed"
    echo ""
}

clone_repository() {
    print_header "Step 2: Cloning Repository"
    
    if [ -d "$APP_DIR" ]; then
        print_warning "Directory already exists, pulling latest changes"
        cd "$APP_DIR"
        git pull origin main
    else
        git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git "$APP_DIR"
        cd "$APP_DIR"
        print_success "Repository cloned"
    fi
    
    print_info "Current directory: $(pwd)"
    echo ""
}

create_virtual_environment() {
    print_header "Step 3: Creating Python Virtual Environment"
    
    cd "$APP_DIR"
    
    if [ -d "$VENV_DIR" ]; then
        print_warning "Virtual environment already exists, removing..."
        rm -rf "$VENV_DIR"
    fi
    
    python3.11 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    
    print_success "Virtual environment created"
    
    # Upgrade pip
    pip install --upgrade pip -q
    print_success "Pip upgraded"
    
    echo ""
}

install_python_dependencies() {
    print_header "Step 4: Installing Python Dependencies"
    
    cd "$APP_DIR"
    source "$VENV_DIR/bin/activate"
    
    print_info "This may take 5-10 minutes on t2.micro..."
    
    # Install with progress
    pip install -r requirements.txt
    
    print_success "Python dependencies installed"
    echo ""
}

create_environment_file() {
    print_header "Step 5: Creating Environment Configuration"
    
    cd "$APP_DIR"
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists, skipping..."
        echo ""
        return
    fi
    
    # Copy example
    cp .env.example .env
    
    print_info "Please configure your API keys:"
    echo ""
    
    # Prompt for API keys
    read -p "Enter your Gemini API Key: " GEMINI_KEY
    read -p "Enter your Cohere API Key (optional, press Enter to skip): " COHERE_KEY
    read -sp "Enter Admin Password: " ADMIN_PASS
    echo ""
    
    # Update .env file
    sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=${GEMINI_KEY}/" .env
    if [ -n "$COHERE_KEY" ]; then
        sed -i "s/COHERE_API_KEY=.*/COHERE_API_KEY=${COHERE_KEY}/" .env
    fi
    sed -i "s/ADMIN_PASSWORD=.*/ADMIN_PASSWORD=${ADMIN_PASS}/" .env
    
    print_success "Environment file configured"
    echo ""
}

setup_directories() {
    print_header "Step 6: Setting Up Data Directories"
    
    cd "$APP_DIR"
    
    mkdir -p data/chromadb
    mkdir -p data/knowledge_library/documents
    mkdir -p data/knowledge_library/metadata
    mkdir -p data/logs
    
    print_success "Data directories created"
    echo ""
}

run_setup() {
    print_header "Step 7: Running Application Setup"
    
    cd "$APP_DIR"
    source "$VENV_DIR/bin/activate"
    
    python setup.py
    
    print_success "Application setup completed"
    echo ""
}

create_systemd_service() {
    print_header "Step 8: Creating Systemd Service"
    
    sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=TechFlow RAG Agent - Streamlit Application
After=network.target

[Service]
Type=simple
User=${APP_USER}
WorkingDirectory=${APP_DIR}
Environment="PATH=${VENV_DIR}/bin"
ExecStart=${VENV_DIR}/bin/streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/techflow-rag-agent/data/logs/application.log
StandardError=append:/home/ubuntu/techflow-rag-agent/data/logs/error.log

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}
    
    print_success "Systemd service created and enabled"
    echo ""
}

configure_firewall() {
    print_header "Step 9: Configuring Firewall (UFW)"
    
    sudo ufw --force enable
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow 8501/tcp comment 'Streamlit'
    sudo ufw allow 80/tcp comment 'HTTP'
    sudo ufw allow 443/tcp comment 'HTTPS'
    
    print_success "Firewall configured"
    sudo ufw status
    echo ""
}

configure_nginx() {
    print_header "Step 10: Configuring Nginx (Reverse Proxy)"
    
    sudo tee /etc/nginx/sites-available/${APP_NAME} > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    location /_stcore/stream {
        proxy_pass http://localhost:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF
    
    sudo ln -sf /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo nginx -t
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    
    print_success "Nginx configured and started"
    echo ""
}

start_application() {
    print_header "Step 11: Starting Application"
    
    sudo systemctl start ${SERVICE_NAME}
    sleep 5
    
    if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
        print_success "Application started successfully!"
    else
        print_error "Application failed to start"
        print_info "Check logs: sudo journalctl -u ${SERVICE_NAME} -n 50"
        exit 1
    fi
    
    echo ""
}

show_summary() {
    print_header "Installation Complete!"
    
    # Get public IP
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "Unable to detect")
    
    echo -e "${GREEN}✓ TechFlow RAG Agent is now running!${NC}"
    echo ""
    echo "📍 Access your application:"
    echo "   http://${PUBLIC_IP}"
    echo ""
    echo "🔧 Useful commands:"
    echo "   Check status:  sudo systemctl status ${SERVICE_NAME}"
    echo "   View logs:     sudo journalctl -u ${SERVICE_NAME} -f"
    echo "   Restart:       sudo systemctl restart ${SERVICE_NAME}"
    echo "   Stop:          sudo systemctl stop ${SERVICE_NAME}"
    echo ""
    echo "📂 Application directory: ${APP_DIR}"
    echo "📝 Logs directory: ${APP_DIR}/data/logs/"
    echo ""
    echo "⚠️  Remember to configure AWS Security Group to allow:"
    echo "   - Port 22 (SSH)"
    echo "   - Port 80 (HTTP)"
    echo "   - Port 443 (HTTPS - optional)"
    echo ""
    print_info "Installation log saved to: /tmp/techflow-install.log"
}

################################################################################
# Main Installation Flow
################################################################################

main() {
    clear
    print_header "TechFlow RAG Agent - AWS EC2 Installation"
    
    echo "This script will install TechFlow RAG Agent on your EC2 instance."
    echo "Compatible with: Ubuntu 22.04 LTS (t2.micro Free Tier)"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to cancel..."
    echo ""
    
    check_root
    
    # Run installation steps
    install_system_dependencies
    clone_repository
    create_virtual_environment
    install_python_dependencies
    create_environment_file
    setup_directories
    run_setup
    create_systemd_service
    configure_firewall
    configure_nginx
    start_application
    show_summary
}

# Execute main function
main 2>&1 | tee /tmp/techflow-install.log
