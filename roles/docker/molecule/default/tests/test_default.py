"""Test suite for docker role."""
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_docker_installed(host):
    """Check if Docker is installed."""
    docker = host.package('docker-ce')
    assert docker.is_installed


def test_docker_service(host):
    """Check if Docker service is running and enabled."""
    service = host.service('docker')
    assert service.is_running
    assert service.is_enabled


def test_docker_command(host):
    """Check if docker command is available."""
    cmd = host.run('docker --version')
    assert cmd.rc == 0
    assert 'Docker version' in cmd.stdout

