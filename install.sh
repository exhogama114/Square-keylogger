#!/bin/bash

# --- Colors ---
G='\033[1;32m'
NC='\033[0m'

echo -e "${G}[+] Updating system and installing dependencies...${NC}"
sudo apt update && sudo apt install -y curl wget python3-pip

# --- Install Cloudflared ---
echo -e "${G}[+] Installing Cloudflared...${NC}"
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
rm cloudflared.deb

# --- Python Setup ---
echo -e "${G}[+] Installing Flask...${NC}"
pip install flask

# --- File Prep ---
echo -e "${G}[+] Preparing log files...${NC}"
touch log.txt link.txt

echo -e "${G}[+] SETUP COMPLETE. Run 'python app.py' to start.${NC}"

