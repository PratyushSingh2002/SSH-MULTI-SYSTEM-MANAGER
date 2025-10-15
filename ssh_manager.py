import json
import os
import paramiko
import threading
import time
import keyring
from colorama import init, Fore, Style

init(autoreset=True)

SYSTEMS_FILE = "systems.json"
KEYRING_SERVICE = "ssh_manager"


def load_systems():
    if not os.path.exists(SYSTEMS_FILE):
        return {}

    with open(SYSTEMS_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return {}
        return json.loads(content)


def save_systems(systems):
    with open(SYSTEMS_FILE, "w", encoding="utf-8") as file:
        json.dump(systems, file, indent=4)


def add_system(name, username, host, port):
    systems = load_systems()
    if name in systems:
        print(f"{Fore.RED}System '{name}' already exists.")
        return

    systems[name] = {"username": username, "host": host, "port": port}
    save_systems(systems)
    print(f"{Fore.GREEN}System '{name}' added successfully.")

    password = os.getenv("SYSTEM_PASSWORD") or input(
        f"Enter password for {username}@{host}: "
    )
    keyring.set_password(KEYRING_SERVICE, f"{name}_{username}", password)


def update_system(name, username=None, host=None, port=None):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return

    if username:
        systems[name]["username"] = username
    if host:
        systems[name]["host"] = host
    if port:
        systems[name]["port"] = port

    save_systems(systems)
    print(f"{Fore.GREEN}System '{name}' updated successfully.")


def delete_system(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return

    del systems[name]
    save_systems(systems)
    try:
        keyring.delete_password(KEYRING_SERVICE, name)
    except keyring.errors.PasswordDeleteError:
        print(f"{Fore.YELLOW}Warning: password not found in keyring.")
    print(f"{Fore.YELLOW}System '{name}' deleted successfully.")


def list_systems():
    systems = load_systems()
    if not systems:
        print(f"{Fore.CYAN}No systems available.")
        return

    print(f"\n{Fore.MAGENTA}{'-'*40}\nAvailable Systems:")
    for name, info in systems.items():
        print(
            f"{Fore.YELLOW}{name}: "
            f"{Fore.WHITE}{info['username']}@{info['host']}:{info['port']}"
        )
    print(f"{Fore.MAGENTA}{'-'*40}")


def connect_to_system(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return

    info = systems[name]
    password = keyring.get_password(KEYRING_SERVICE, f"{name}_{info['username']}")
    if not password:
        print(f"{Fore.RED}Password not found for {info['username']}@{info['host']}.")
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            info["host"],
            port=int(info["port"]),
            username=info["username"],
            password=password,
        )
        print(f"{Fore.GREEN}Connected to {name} successfully!")
        stdin, stdout, stderr = ssh.exec_command("uname -a")
        print(f"{Fore.CYAN}System Info:\n{Fore.WHITE}{stdout.read().decode()}")
    except Exception as e:
        print(f"{Fore.RED}Failed to connect: {e}")
    finally:
        ssh.close()


def run_command_on_system(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return

    info = systems[name]
    password = keyring.get_password(KEYRING_SERVICE, f"{name}_{info['username']}")
    if not password:
        print(f"{Fore.RED}Password not found for {info['username']}@{info['host']}.")
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            info["host"],
            port=int(info["port"]),
            username=info["username"],
            password=password,
        )
        print(
            f"\n{Fore.GREEN}Connected to {name}. "
            f"Type {Fore.YELLOW}'exit'{Fore.GREEN} to end session.\n"
        )

        shell = ssh.invoke_shell()
        shell.settimeout(1)

        def receive_output():
            while True:
                if shell.closed:
                    break
                try:
                    if shell.recv_ready():
                        output = shell.recv(4096).decode()
                        print(output, end="")
                except Exception:
                    continue
                time.sleep(0.2)

        output_thread = threading.Thread(target=receive_output, daemon=True)
        output_thread.start()

        while True:
            command = input(f"{Fore.CYAN}ssh@{name}$ {Style.RESET_ALL}")
            if command.strip().lower() == "exit":
                print(f"{Fore.YELLOW}Closing SSH session...\n")
                shell.close()
                break
            shell.send(command + "\n")

    except Exception as e:
        print(f"{Fore.RED}Failed to connect or run command: {e}")
    finally:
        ssh.close()


def get_system_info(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return

    info = systems[name]
    password = keyring.get_password(KEYRING_SERVICE, f"{name}_{info['username']}")
    if not password:
        print(f"{Fore.RED}Password not found for {info['username']}@{info['host']}.")
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            info["host"],
            port=int(info["port"]),
            username=info["username"],
            password=password,
        )
        print(f"{Fore.GREEN}Connected to {name} — Fetching system info...\n")

        commands = {
            "OS Info": "uname -a",
            "Uptime": "uptime",
            "Memory Usage": "free -h",
            "Disk Usage": "df -h",
        }

        for title, cmd in commands.items():
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            print(f"{Fore.MAGENTA}{title}:\n{Fore.WHITE}{output}\n")

    except Exception as e:
        print(f"{Fore.RED}Failed to retrieve system info: {e}")
    finally:
        ssh.close()
