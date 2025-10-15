import pytest
from ssh_manager import SSHManager  # Yeh assume karte hue ke SSHManager main class hai

@pytest.fixture
def manager():
    return SSHManager()

def test_add_connection(manager):
    manager.add_connection('test_system', '192.168.1.1', 'user', 'password')
    assert 'test_system' in manager.list_connections()

def test_run_command(manager):
    output = manager.run_command('test_system', 'ls')
    assert 'expected_output' in output
