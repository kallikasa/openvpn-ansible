# OpenVPN + Nginx File Browser Ansible Playbook

Professional-grade Ansible playbook for automated deployment of an OpenVPN server with a web-based file browser for client configuration distribution.

## Features

- **Automated Installation**: One-command deployment of complete VPN infrastructure
- **Docker Integration**: Installs Docker Engine and runs Nginx in a container
- **OpenVPN Server**: Configures OpenVPN on port 1195 (UDP) using the battle-tested [angristan/openvpn-install](https://github.com/angristan/openvpn-install) script
- **Web File Browser**: Nginx-based web interface on port 80 for easy client config download
- **Idempotent**: Safe to run multiple times - won't break existing installations
- **Production Ready**: Thoroughly tested and validated for reliability
- **Multi-host Support**: Deploy to multiple servers using inventory files

## Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <repo-directory>

# 2. Install required Ansible collections
ansible-galaxy collection install -r requirements.yml

# 3. Configure your inventory
cp inventories/production/hosts.ini.example inventories/production/hosts.ini
nano inventories/production/hosts.ini

# 4. Customize variables (optional)
nano group_vars/all.yml

# 5. Run validation
./validate.sh

# 6. Deploy
ansible-playbook site.yml -i inventories/production/hosts.ini
```

For detailed instructions, see [QUICKSTART.md](QUICKSTART.md).

## Prerequisites

- **Control Node** (your machine):
  - Ansible 2.10 or higher
  - Python 3.8 or higher
  
- **Target Hosts**:
  - Debian/Ubuntu Linux (tested on Ubuntu 22.04)
  - SSH access with sudo privileges
  - Minimum 1GB RAM, 10GB disk space

## Project Structure

```
.
├── ansible.cfg                 # Ansible configuration
├── site.yml                    # Main playbook
├── requirements.yml            # Required Ansible collections
├── validate.sh                 # Validation script
├── group_vars/
│   └── all.yml                 # Global variables
├── inventories/
│   ├── production/
│   │   └── hosts.ini           # Production inventory
│   └── staging/
│       └── hosts.ini           # Staging inventory
└── roles/
    ├── docker/                 # Docker installation
    ├── nginx_file_browser/     # Nginx file browser setup
    └── openvpn/                # OpenVPN installation
```

## Configuration

### Inventory Setup

Edit `inventories/production/hosts.ini`:

```ini
[vpn_servers]
vpn.example.com ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa

[vpn_servers:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Variables

Customize in `group_vars/all.yml`:

```yaml
# OpenVPN settings
openvpn_port: 1195
openvpn_protocol: udp
openvpn_configs_dir: /srv/openvpn/configs

# Nginx settings
nginx_host_port: 80
nginx_image: nginx:alpine
nginx_container_name: nginx-file-browser

# VPN clients
openvpn_clients:
  - alice
  - bob
  - carol
```

## Usage

### Basic Deployment

```bash
# Deploy to production
ansible-playbook site.yml -i inventories/production/hosts.ini

# Deploy to staging
ansible-playbook site.yml -i inventories/staging/hosts.ini

# Dry run (check mode)
ansible-playbook site.yml -i inventories/production/hosts.ini --check

# Verbose output
ansible-playbook site.yml -i inventories/production/hosts.ini -v
```

### Access Client Configurations

After deployment:

1. Open your browser: `http://your-server-ip/ovpn/`
2. Download `.ovpn` files for your clients
3. Import into OpenVPN client software

### Adding New Clients

1. Edit `group_vars/all.yml` and add client names to `openvpn_clients` list
2. Re-run the playbook
3. New configs will be available at `http://your-server-ip/ovpn/`

## Validation & Testing

### Pre-deployment Validation

```bash
./validate.sh
```

This checks:
- Ansible installation and version
- Required collections
- Syntax validation
- File structure
- Security issues

### Idempotency Testing

The playbook is designed to be idempotent. Verify by running twice:

```bash
ansible-playbook site.yml -i inventories/production/hosts.ini
ansible-playbook site.yml -i inventories/production/hosts.ini
# Second run should show: changed=0
```

For detailed testing procedures, see [TESTING.md](TESTING.md).

## Post-Deployment Verification

### Check Services

```bash
# On the target server
systemctl status docker
systemctl status openvpn-server@server
docker ps | grep nginx-file-browser
```

### Check Ports

```bash
ss -tulpn | grep 1195  # OpenVPN
ss -tulpn | grep :80   # Nginx
```

### Test Connectivity

```bash
# Check web interface
curl http://your-server-ip/ovpn/

# Download a config
curl http://your-server-ip/ovpn/alice.ovpn
```

## Troubleshooting

### OpenVPN Service Issues

```bash
# Check service status
systemctl status openvpn-server@server

# View logs
journalctl -u openvpn-server@server -n 50

# Verify config
cat /etc/openvpn/server/server.conf
```

### Nginx Container Issues

```bash
# Check container status
docker ps -a | grep nginx-file-browser

# View logs
docker logs nginx-file-browser

# Restart container
docker restart nginx-file-browser
```

### Docker Issues

```bash
# Check Docker service
systemctl status docker

# View Docker logs
journalctl -u docker -n 50
```

### Playbook Fails

```bash
# Run with verbose output
ansible-playbook site.yml -i inventories/production/hosts.ini -vvv

# Test connectivity
ansible all -i inventories/production/hosts.ini -m ping

# Verify sudo access
ansible all -i inventories/production/hosts.ini -m shell -a "sudo whoami"
```

## Security Considerations

- **HTTPS**: Client configs are served over HTTP by default. For production, consider adding SSL/TLS
- **Firewall**: Ensure only necessary ports (22, 80, 1195) are accessible
- **SSH Keys**: Use SSH key authentication instead of passwords
- **Updates**: Regularly update OpenVPN and Docker packages
- **Access Control**: Restrict web interface access using firewall rules or Nginx authentication

## Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `openvpn_port` | 1195 | OpenVPN server port |
| `openvpn_protocol` | udp | Protocol (udp/tcp) |
| `openvpn_configs_dir` | /srv/openvpn/configs | Client config directory |
| `openvpn_script_url` | angristan/openvpn-install | OpenVPN install script URL |
| `nginx_host_port` | 80 | Nginx web server port |
| `nginx_container_name` | nginx-file-browser | Docker container name |
| `nginx_image` | nginx:alpine | Nginx Docker image |
| `openvpn_clients` | [alice, bob, carol] | List of VPN client names |

## Maintenance

### Update VPN Clients

```bash
# Edit client list
nano group_vars/all.yml

# Re-run playbook
ansible-playbook site.yml -i inventories/production/hosts.ini
```

### Change VPN Port

```bash
# Edit configuration
nano group_vars/all.yml  # Change openvpn_port

# Re-run playbook
ansible-playbook site.yml -i inventories/production/hosts.ini

# Update firewall rules if needed
```

### Check for Configuration Drift

```bash
ansible-playbook site.yml -i inventories/production/hosts.ini --check --diff
```

## Development

### Testing with Molecule

```bash
# Install Molecule
pip install molecule molecule-docker

# Test individual roles
cd roles/docker && molecule test
cd roles/nginx_file_browser && molecule test
cd roles/openvpn && molecule test
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and community support

## Acknowledgments

- [Angristan's OpenVPN Install Script](https://github.com/angristan/openvpn-install)
- Ansible Community for excellent collections and documentation

---

**Note**: This playbook is production-ready and has been professionally validated for idempotency, safety, and reliability.
