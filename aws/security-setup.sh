#!/bin/bash

################################################################################
# TechFlow RAG Agent - Security Configuration Script
# 
# Configures fail2ban, SSH hardening, and automatic security updates
#
# Usage: sudo bash security-setup.sh
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root: sudo bash security-setup.sh${NC}"
    exit 1
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  TechFlow RAG Agent - Security Setup${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. Configure Fail2Ban
echo -e "${BLUE}Configuring Fail2Ban...${NC}"

cat > /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
destemail = root@localhost
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
maxretry = 3
bantime = 7200

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2
EOF

systemctl restart fail2ban
systemctl enable fail2ban

echo -e "${GREEN}✓ Fail2Ban configured${NC}"
echo ""

# 2. SSH Hardening
echo -e "${BLUE}Hardening SSH configuration...${NC}"

# Backup original config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Apply hardening
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config
sed -i 's/#MaxAuthTries 6/MaxAuthTries 3/' /etc/ssh/sshd_config
sed -i 's/#ClientAliveInterval 0/ClientAliveInterval 300/' /etc/ssh/sshd_config
sed -i 's/#ClientAliveCountMax 3/ClientAliveCountMax 2/' /etc/ssh/sshd_config

# Add AllowUsers if not present
if ! grep -q "AllowUsers" /etc/ssh/sshd_config; then
    echo "AllowUsers ubuntu" >> /etc/ssh/sshd_config
fi

systemctl restart sshd

echo -e "${GREEN}✓ SSH hardened${NC}"
echo ""

# 3. Enable Automatic Security Updates
echo -e "${BLUE}Enabling automatic security updates...${NC}"

apt-get install -y unattended-upgrades

cat > /etc/apt/apt.conf.d/50unattended-upgrades <<'EOF'
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF

cat > /etc/apt/apt.conf.d/20auto-upgrades <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

systemctl restart unattended-upgrades

echo -e "${GREEN}✓ Automatic updates enabled${NC}"
echo ""

# 4. Setup Log Rotation for Application
echo -e "${BLUE}Configuring log rotation...${NC}"

cat > /etc/logrotate.d/techflow-rag <<'EOF'
/home/ubuntu/techflow-rag-agent/data/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0644 ubuntu ubuntu
    postrotate
        systemctl reload techflow-rag > /dev/null 2>&1 || true
    endscript
}
EOF

echo -e "${GREEN}✓ Log rotation configured${NC}"
echo ""

# 5. Set File Permissions
echo -e "${BLUE}Setting secure file permissions...${NC}"

chown -R ubuntu:ubuntu /home/ubuntu/techflow-rag-agent
chmod 600 /home/ubuntu/techflow-rag-agent/.env 2>/dev/null || true
chmod 700 /home/ubuntu/techflow-rag-agent/data

echo -e "${GREEN}✓ File permissions set${NC}"
echo ""

# Summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Security Configuration Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Applied configurations:"
echo "  ✓ Fail2Ban protection against brute force"
echo "  ✓ SSH hardening (no root login, key auth only)"
echo "  ✓ Automatic security updates"
echo "  ✓ Log rotation for application logs"
echo "  ✓ Secure file permissions"
echo ""
echo -e "${YELLOW}⚠  Important: Make sure you have SSH key authentication set up!${NC}"
echo "   Password authentication is now disabled."
echo ""
echo "Check fail2ban status: sudo fail2ban-client status"
echo "Check banned IPs: sudo fail2ban-client status sshd"
