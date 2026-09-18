#!/bin/bash
# Script to create LXC 168 for VCPnet Config Tool with specific MAC

# Configuration
LXC_ID=168
LXC_HOSTNAME="VCPTools"
TEMPLATE="local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst"  # Template name (let pct find it in available storages)
MAC_ADDRESS="32:36:C3:1A:A8:40"
REPO_URL="https://github.com/Virt1080/vcpnet-config-tool.git"

# Create the LXC container using local-zfs storage for the disk
echo "Creating LXC $LXC_ID with template $TEMPLATE on storage local-zfs..."
if ! 	pct create $LXC_ID $TEMPLATE \
		--hostname $LXC_HOSTNAME \
		--rootfs local-zfs:8 \
		--net0 name=eth0,bridge=vmbr0,hwaddr=$MAC_ADDRESS,ip=dhcp; then

    echo "Error: Failed to create LXC container"
    echo "Tip: Make sure local-zfs storage exists and is configured for container disks"
    echo "You can check available storages with: pvesm status"
    exit 1
fi

# Wait for container to start
echo "Starting container..."
sleep 3
pct start $LXC_ID
sleep 5

# Verify container is running
if ! pct status $LXC_ID | grep -q "running"; then
    echo "Error: Container failed to start properly"
    pct destroy $LXC_ID 2>/dev/null || true
    exit 1
fi

# Set up the application inside the container
echo "Setting up VCPnet Config Tool inside container..."
pct exec $LXC_ID -- bash -c "
  # Update package list
  echo \"Updating package list...\"
  apt-get update >/dev/null 2>&1
  
  # Install dependencies
  echo \"Installing dependencies...\"
  apt-get install -y python3 python3-venv python3-pip git curl >/dev/null 2>&1
  
  # Create app directory
  mkdir -p /opt/vcpnet-config-tool
  cd /opt/vcpnet-config-tool
  
  # Clone the repository
  echo \"Cloning repository...\"
  git clone $REPO_URL . >/dev/null 2>&1
  
  # Create virtual environment
  echo \"Setting up virtual environment...\"
  python3 -m venv venv >/dev/null 2>&1
  source venv/bin/activate
  
  # Install dependencies
  echo \"Installing Python dependencies...\"
  pip install -r requirements.txt >/dev/null 2>&1
  
  # Create update script
  cat > /usr/local/bin/update << 'EO_UPDATE'
#!/bin/bash
cd /opt/vcpnet-config-tool
source venv/bin/activate
echo \"Pulling latest changes...\"
git pull
echo \"Installing/updating dependencies...\"
pip install -r requirements.txt
echo \"Update complete! To restart the application, run: systemctl restart vcpnet (if running as service) or restart uvicorn manually.\"
EO_UPDATE
  chmod +x /usr/local/bin/update
  
  # Create systemd service file
  cat > /etc/systemd/system/vcpnet.service << 'EO_SERVICE'
[Unit]
Description=VCPnet Config Tool
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/vcpnet-config-tool
Environment=PATH=/opt/vcpnet-config-tool/venv/bin
ExecStart=/opt/vcpnet-config-tool/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EO_SERVICE

  # Enable and start the service
  systemctl daemon-reload
  systemctl enable vcpnet
  systemctl start vcpnet
  
# Setup auto-login for LXC console
printf "\033[0;34m[INFO]\033[0m Setting up auto-login for console\n"
# Create override directory for container-getty service
mkdir -p /etc/systemd/system/container-getty@tty1.service.d
cat <<EOF >/etc/systemd/system/container-getty@tty1.service.d/override.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty -a root -o '-p -- \\u' --noclear - \$TERM
EOF
# Reload systemd and restart the getty service
systemctl daemon-reload
systemctl restart container-getty@tty1.service
printf "\033[0;32m[OK]\033[0m Auto-login configured for console\n"
"
