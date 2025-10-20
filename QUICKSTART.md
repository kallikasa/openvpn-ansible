# Quick Start Guide

Get your OpenVPN server running in less than 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

- [ ] Ansible 2.10+ installed on your local machine
- [ ] SSH access to your target server (root or sudo user)
- [ ] Target server running Ubuntu/Debian
- [ ] Ports 22, 80, and 1195 accessible on your server

## Step-by-Step Deployment

### 1. Install Ansible (if not already installed)

**macOS:**
```bash
brew install ansible
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ansible
```

**Verify installation:**
```bash
ansible --version
# Should show version 2.10 or higher
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-directory>

# Install required collections
ansible-galaxy collection install -r requirements.yml
```

### 3. Configure Your Server

Create your inventory file:

```bash
nano inventories/production/hosts.ini
```

Add your server details:

```ini
[vpn_servers]
your.server.ip.address ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa

[vpn_servers:vars]
ansible_python_interpreter=/usr/bin/python3
```

**Replace:**
- `your.server.ip.address` with your actual server IP
- `ansible_user=root` with your SSH user (if not root)
- `~/.ssh/id_rsa` with your SSH key path

### 4. Test Connectivity

```bash
ansible all -i inventories/production/hosts.ini -m ping
```

Expected output:
```
your.server.ip.address | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### 5. Configure VPN Clients (Optional)

Edit the client list:

```bash
nano group_vars/all.yml
```

Modify the `openvpn_clients` section:

```yaml
openvpn_clients:
  - alice      # Replace with your client names
  - bob
  - charlie
```

### 6. Validate Configuration

```bash
./validate.sh
```

This checks everything is ready for deployment. All checks should pass ✓.

### 7. Deploy!

**Dry run first (recommended):**
```bash
ansible-playbook site.yml -i inventories/production/hosts.ini --check
```

**Actual deployment:**
```bash
ansible-playbook site.yml -i inventories/production/hosts.ini
```

The deployment takes approximately 3-5 minutes depending on your server's internet speed.

### 8. Verify Deployment

After deployment completes, verify services are running:

```bash
ansible all -i inventories/production/hosts.ini -m shell -a "systemctl status openvpn-server@server"
ansible all -i inventories/production/hosts.ini -m shell -a "docker ps"
```

### 9. Download Client Configs

Open your browser and navigate to:

```
http://your.server.ip.address/ovpn/
```

You'll see a file listing with your client configurations:
- `alice.ovpn`
- `bob.ovpn`
- `charlie.ovpn`

Download the config for your device.

### 10. Connect to VPN

**On Linux:**
```bash
sudo openvpn --config alice.ovpn
```

**On macOS:**
- Install [Tunnelblick](https://tunnelblick.net/)
- Import the `.ovpn` file
- Connect

**On Windows:**
- Install [OpenVPN GUI](https://openvpn.net/community-downloads/)
- Import the `.ovpn` file
- Connect

**On iOS/Android:**
- Install OpenVPN Connect app
- Import the `.ovpn` file
- Connect

## Verification Checklist

After deployment, verify everything is working:

- [ ] OpenVPN service is running: `systemctl status openvpn-server@server`
- [ ] Docker is running: `docker ps`
- [ ] Nginx container is running: `docker ps | grep nginx`
- [ ] Port 1195 is listening: `ss -tulpn | grep 1195`
- [ ] Web interface is accessible: `curl http://your-server-ip/ovpn/`
- [ ] Client configs exist: `ls /srv/openvpn/configs/`
- [ ] Can download configs from web browser
- [ ] Can connect to VPN using downloaded config

## Common First-Time Issues

### Issue: "Permission denied" during connection test

**Solution:**
```bash
# Make sure your SSH key has correct permissions
chmod 600 ~/.ssh/id_rsa

# Or use password authentication (less secure)
# Add to inventory: ansible_ssh_pass='your_password'
```

### Issue: "sudo password required"

**Solution:**
```bash
# Add to your inventory file:
ansible_become_pass='your_sudo_password'

# Or configure passwordless sudo on the server:
echo "your_user ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/your_user
```

### Issue: Playbook fails at Docker installation

**Solution:**
```bash
# Make sure your server has internet access
ansible all -i inventories/production/hosts.ini -m shell -a "ping -c 3 google.com"

# Check if port 80/443 are blocked
# Ensure APT repositories are working
```

### Issue: Cannot access web interface

**Solution:**
```bash
# Check if port 80 is accessible from your network
curl http://your-server-ip

# Check firewall rules
ansible all -i inventories/production/hosts.ini -m shell -a "ufw status"

# If using cloud provider, check security groups/firewall rules
```

## Next Steps

### Add More Clients

1. Edit `group_vars/all.yml` and add client names
2. Re-run the playbook:
   ```bash
   ansible-playbook site.yml -i inventories/production/hosts.ini
   ```
3. Download new configs from `http://your-server-ip/ovpn/`

### Change VPN Port

1. Edit `group_vars/all.yml`:
   ```yaml
   openvpn_port: 1194  # or any port you prefer
   ```
2. Re-run the playbook
3. Update firewall rules if needed

### Secure the Web Interface

By default, configs are served over HTTP. To add security:

**Option 1: Restrict by IP**
```bash
# Add firewall rule to allow only your IP
ufw allow from your.ip.address to any port 80
```

**Option 2: Add SSL/TLS**
Use a reverse proxy with Let's Encrypt SSL certificate.

**Option 3: Use VPN to access**
Only access the web interface while connected to the VPN.

## Test Idempotency

One of the key features is idempotency - you can run the playbook multiple times safely:

```bash
# Run once
ansible-playbook site.yml -i inventories/production/hosts.ini

# Run again immediately
ansible-playbook site.yml -i inventories/production/hosts.ini
```

The second run should show `changed=0`, meaning nothing was modified.

## Multiple Servers

To deploy to multiple servers:

1. Add all servers to your inventory:
   ```ini
   [vpn_servers]
   vpn1.example.com ansible_user=root
   vpn2.example.com ansible_user=root
   vpn3.example.com ansible_user=root
   ```

2. Run the playbook once:
   ```bash
   ansible-playbook site.yml -i inventories/production/hosts.ini
   ```

All servers will be configured identically!

## Staging Environment

Before deploying to production, test in staging:

1. Configure `inventories/staging/hosts.ini` with a test server
2. Deploy to staging:
   ```bash
   ansible-playbook site.yml -i inventories/staging/hosts.ini
   ```
3. Test thoroughly
4. Deploy to production with confidence

## Getting Help

- Check logs: `journalctl -u openvpn-server@server -f`
- Review [TESTING.md](TESTING.md) for detailed testing procedures
- See [README.md](README.md) for full documentation
- Run validation: `./validate.sh`
- Check troubleshooting section in README

## Summary

You now have:
- ✅ OpenVPN server running on port 1195
- ✅ Web interface for downloading configs on port 80
- ✅ Client configurations ready to use
- ✅ Docker and all services running automatically
- ✅ System configured to survive reboots

**Next**: Connect a client and test the VPN connection!

---

**Deployment time**: ~3-5 minutes  
**Difficulty**: Easy  
**Skill level required**: Basic Linux and Ansible knowledge
