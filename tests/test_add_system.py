import pytest
from ssh_manager import SSHManager

@pytest.fixture
def manager():
    return SSHManager()

def test_add_system(manager):
    manager.add_connection("test1", "192.168.1.1", "user", "pass")
    systems = manager.list_connections()
    assert "test1" in systems

def test_delete_system(manager):
    manager.add_connection("test_del", "192.168.1.2", "user", "pass")
    manager.delete_connection("test_del")
    systems = manager.list_connections()
    assert "test_del" not in systems
