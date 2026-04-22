#!/usr/bin/env bash
set -euo pipefail

echo ">>> Updating apt and installing prerequisites..."
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg python3-pip python3-venv iproute2 iptables netcat-openbsd

echo ">>> Installing Docker..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo ">>> Adding current user to docker group..."
sudo usermod -aG docker "$USER"

echo ">>> Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

echo ">>> Setup complete! PLEASE LOG OUT AND LOG BACK IN for Docker permissions to take effect."
