"""Test suite for openvpn role."""
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_openvpn_script(host):
    """Check if openvpn-install script exists."""
    script = host.file('/usr/local/sbin/openvpn-install.sh')
    assert script.exists
    assert script.is_file
    assert script.mode == 0o755


def test_openvpn_config(host):
    """Check if OpenVPN server config exists."""
    config = host.file('/etc/openvpn/server/server.conf')
    assert config.exists
    assert config.is_file


def test_openvpn_service(host):
    """Check if OpenVPN service is running and enabled."""
    service = host.service('openvpn-server@server')
    assert service.is_running
    assert service.is_enabled


def test_openvpn_port(host):
    """Check if OpenVPN port 1195 is listening."""
    socket = host.socket('udp://0.0.0.0:1195')
    assert socket.is_listening


def test_client_configs(host):
    """Check if client config files were generated."""
    configs_dir = host.file('/srv/openvpn/configs')
    assert configs_dir.exists
    assert configs_dir.is_directory
    
    # Check for at least one .ovpn file
    cmd = host.run('find /srv/openvpn/configs -name "*.ovpn" | wc -l')
    assert cmd.rc == 0
    assert int(cmd.stdout.strip()) >= 1

