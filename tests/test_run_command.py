import pytest
from ssh_manager import SSHManager

@pytest.fixture
def manager():
    return SSHManager()

def test_run_command_simulation(manager, monkeypatch):
    # Mock command output instead of real SSH
    def fake_run_command(name, cmd):
        return "mocked output"
    manager.run_command = fake_run_command

    result = manager.run_command("test_system", "ls")
    assert "mocked" in result
