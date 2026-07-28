#!/bin/bash

################################################################################
# TechFlow RAG Agent - Update Script
# 
# This script updates the application with the latest changes from GitHub
# Preserves data and configuration
#
# Usage: bash update.sh
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

APP_DIR="/home/ubuntu/techflow-rag-agent"
SERVICE_NAME="techflow-rag"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  TechFlow RAG Agent - Update${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Stop the service
echo -e "${BLUE}Stopping application...${NC}"
sudo systemctl stop ${SERVICE_NAME}
echo -e "${GREEN}✓ Service stopped${NC}"
echo ""

# Backup current .env
if [ -f "${APP_DIR}/.env" ]; then
    echo -e "${BLUE}Backing up .env file...${NC}"
    cp ${APP_DIR}/.env ${APP_DIR}/.env.backup
    echo -e "${GREEN}✓ .env backed up${NC}"
fi

# Pull latest changes
cd ${APP_DIR}
echo -e "${BLUE}Pulling latest changes from GitHub...${NC}"
git pull origin main
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

# Restore .env
if [ -f "${APP_DIR}/.env.backup" ]; then
    mv ${APP_DIR}/.env.backup ${APP_DIR}/.env
fi

# Update dependencies
echo -e "${BLUE}Updating Python dependencies...${NC}"
source ${APP_DIR}/venv/bin/activate
pip install -r requirements.txt --upgrade -q
echo -e "${GREEN}✓ Dependencies updated${NC}"
echo ""

# Start the service
echo -e "${BLUE}Starting application...${NC}"
sudo systemctl start ${SERVICE_NAME}
sleep 3

# Check status
if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
    echo -e "${GREEN}✓ Application updated and running!${NC}"
    echo ""
    echo "Check status: sudo systemctl status ${SERVICE_NAME}"
else
    echo -e "${YELLOW}⚠ Application may have issues starting${NC}"
    echo "Check logs: sudo journalctl -u ${SERVICE_NAME} -n 50"
fi
