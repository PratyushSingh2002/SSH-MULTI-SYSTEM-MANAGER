
# 🔐 NEXA

**A simple command-line tool to manage multiple SSH systems**  
Created with ❤️ by **Pratyush Singh**

---

## 🧩 Features

- 🔌 Add, update, and delete SSH connections
- 📜 List all stored systems
- 💻 Connect to remote systems via SSH
- 🖥️ Run interactive terminal commands (e.g., `cd`, `mysqld`, `ls`, `top`, etc.)
- 🧠 Retrieve system information (e.g., `uname -a`) from connected systems
- 🎨 Stylish terminal output using `colorama`
- 🔐 Secure password storage using the `keyring` module

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ssh-system-multi-manager.git
cd ssh-system-multi-manager
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

- On **Windows**:
  ```bash
  venv\Scriptsctivate
  ```

- On **Linux/macOS**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python main.py
```

You’ll see a menu like this:

```
===== SSH SYSTEM MULTI MANAGER =====
Made by Pratyush Singh

1. Add system
2. Update system
3. Delete system
4. List systems
5. Connect to system
6. Exit
7. Run command on system
8. Get system info
```

---

## 🧳 System Info

- The **Get system info** option retrieves and displays the basic system info (e.g., `uname -a`) of the remote system you connect to.

---

## 📂 File Transfer

- The **Send file to system** option allows you to select a file from your current directory.
- The selected file is sent via **SFTP** to the `~/downloads/` directory on the remote system.
- If the directory doesn’t exist, it will be created automatically.

---

## 📄 Requirements

- Python 3.7+
- OpenSSH server installed on remote systems

---

## 📁 File Structure

```
ssh-system-multi-manager/
├── main.py              # Entry point for the app
├── ssh_manager.py       # Core functionality
├── requirements.txt     # Python dependencies
├── systems.json         # Auto-generated storage for system details
├── README.md            # Project documentation
```

---

## 🧠 Notes

- Ensure SSH is enabled and accessible on the target system.
- Termux and some systems may have non-standard home directories (e.g., `/data/data/com.termux/files/home`).
- This project currently uses password-based authentication.

---

## 📌 To Do

- [ ] Add key-based authentication support
- [ ] Encrypt stored system credentials (for security)
- [ ] Add download-from-remote feature
- [ ] Build into installable CLI

---

## 📜 License

MIT License

---

> ✨ “Productivity is never an accident. It is always the result of a commitment to excellence.” – Paul J. Meyer
