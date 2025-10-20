"""Test suite for nginx_file_browser role."""
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_configs_directory(host):
    """Check if configs directory exists."""
    directory = host.file('/srv/openvpn/configs')
    assert directory.exists
    assert directory.is_directory
    assert directory.mode == 0o755


def test_nginx_config_file(host):
    """Check if nginx config file exists."""
    config = host.file('/etc/nginx-file-browser.conf')
    assert config.exists
    assert config.is_file
    assert config.mode == 0o644


def test_nginx_container_running(host):
    """Check if nginx container is running."""
    cmd = host.run('docker ps --filter name=nginx-file-browser --format "{{.Names}}"')
    assert cmd.rc == 0
    assert 'nginx-file-browser' in cmd.stdout


def test_http_port_listening(host):
    """Check if HTTP port 80 is listening."""
    socket = host.socket('tcp://0.0.0.0:80')
    assert socket.is_listening


def test_http_response(host):
    """Check if HTTP server responds."""
    cmd = host.run('curl -sS http://127.0.0.1:80/')
    assert cmd.rc == 0

