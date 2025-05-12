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
    
    with open(SYSTEMS_FILE, "r") as file:
        content = file.read().strip()  # Read the content and strip any leading/trailing whitespace
        if not content:  # If the file is empty, return an empty dictionary
            return {}
        return json.loads(content)  # Otherwise, load the JSON content


def save_systems(systems):
    with open(SYSTEMS_FILE, "w") as file:
        json.dump(systems, file, indent=4)

def add_system(name, username, host, port):
    systems = load_systems()
    if name in systems:
        print(f"{Fore.RED}System '{name}' already exists.")
        return
    systems[name] = {"username": username, "host": host, "port": port}
    save_systems(systems)
    print(f"{Fore.GREEN}System '{name}' added successfully.")

    # Ask user for password and store it securely using keyring
    password = input(f"Enter password for {username}@{host}: ")
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
    # Remove password from keyring
    keyring.delete_password(KEYRING_SERVICE, name)
    print(f"{Fore.YELLOW}System '{name}' deleted successfully.")

def list_systems():
    systems = load_systems()
    if not systems:
        print(f"{Fore.CYAN}No systems available.")
        return
    print(f"\n{Fore.MAGENTA}{'-'*40}\nAvailable Systems:")
    for name, info in systems.items():
        print(f"{Fore.YELLOW}{name}: {Fore.WHITE}{info['username']}@{info['host']}:{info['port']}")
    print(f"{Fore.MAGENTA}{'-'*40}")

def connect_to_system(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return
    info = systems[name]

    # Retrieve the password from keyring
    password = keyring.get_password(KEYRING_SERVICE, f"{name}_{info['username']}")
    if not password:
        print(f"{Fore.RED}Password not found for {info['username']}@{info['host']}.")
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(info["host"], port=int(info["port"]),
                    username=info["username"], password=password)
        print(f"{Fore.GREEN}Connected to {name} successfully!")
        stdin, stdout, stderr = ssh.exec_command('uname -a')
        print(f"{Fore.CYAN}System Info:\n{Fore.WHITE}{stdout.read().decode()}")
        ssh.close()
    except Exception as e:
        print(f"{Fore.RED}Failed to connect: {e}")

def run_command_on_system(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return
    info = systems[name]

    # Retrieve the password from keyring
    password = keyring.get_password(KEYRING_SERVICE, f"{name}_{info['username']}")
    if not password:
        print(f"{Fore.RED}Password not found for {info['username']}@{info['host']}.")
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(info["host"], port=int(info["port"]),
                    username=info["username"], password=password)
        print(f"\n{Fore.GREEN}Connected to {name}. Type {Fore.YELLOW}'exit'{Fore.GREEN} to end session.\n")

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
                except:
                    pass
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

        ssh.close()

    except Exception as e:
        print(f"{Fore.RED}Failed to connect or run command: {e}")

def send_file_to_system(name):
    systems = load_systems()
    if name not in systems:
        print(f"{Fore.RED}System '{name}' does not exist.")
        return

    # List files in current directory
    local_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    if not local_files:
        print(f"{Fore.RED}No files found in current directory.")
        return

    print(f"\n{Fore.BLUE}Files in current directory:")
    for i, file in enumerate(local_files, 1):
        print(f"{Fore.YELLOW}{i}. {file}")

    try:
        choice = int(input(f"{Fore.CYAN}Enter file number to send: {Style.RESET_ALL}"))
        if choice < 1 or choice > len(local_files):
            print(f"{Fore.RED}Invalid file number.")
            return
    except ValueError:
        print(f"{Fore.RED}Invalid input.")
        return

    filename = local_files[choice - 1]
    info = systems[name]

    # Retrieve the password from keyring
    password = keyring.get_password(KEYRING_SERVICE, f"{name}_{info['username']}")
    if not password:
        print(f"{Fore.RED}Password not found for {info['username']}@{info['host']}.")
        return

    try:
        transport = paramiko.Transport((info["host"], int(info["port"])))
        transport.connect(username=info["username"], password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_home = f"/home/{info['username']}"
        remote_dir = f"{remote_home}/downloads"
        remote_path = f"{remote_dir}/{filename}"

        try:
            sftp.chdir(remote_dir)
        except IOError:
            sftp.mkdir(remote_dir)

        sftp.put(filename, remote_path)
        print(f"{Fore.GREEN}File '{filename}' successfully uploaded to '{remote_path}'.")

        sftp.close()
        transport.close()

    except Exception as e:
        print(f"{Fore.RED}File upload failed: {e}")

