from ssh_manager import *
import signal
import sys

def handle_exit(signum, frame):
    print(f"\n{Fore.YELLOW}👋 Exiting safely... Goodbye!{Style.RESET_ALL}")
    sys.exit(0)

# Handle Ctrl+C (SIGINT) and Ctrl+Z (SIGTSTP)
signal.signal(signal.SIGINT, handle_exit)   # Ctrl + C
signal.signal(signal.SIGTSTP, handle_exit)  # Ctrl + Z

def menu():
    print(f"\n{Fore.MAGENTA}===== SSH SYSTEM MULTI MANAGER ====={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Made by Pratyush Singh\n")
    print("1. Add system")
    print("2. Update system")
    print("3. Delete system")
    print("4. List systems")
    print("5. Connect to system")
    print("6. Run command on system")
    print("7. Get system info")
    print("8. Exit")

try:
    while True:
        menu()
        choice = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}")

        if choice == "1":
            name = input("Enter system name: ")
            username = input("Enter username: ")
            host = input("Enter host: ")
            port = input("Enter port: ")
            add_system(name, username, host, port)

        elif choice == "2":
            name = input("Enter system name to update: ")
            username = input("New username (leave blank to keep): ")
            host = input("New host (leave blank to keep): ")
            port = input("New port (leave blank to keep): ")
            update_system(name, username or None, host or None, port or None)

        elif choice == "3":
            name = input("Enter system name to delete: ")
            delete_system(name)

        elif choice == "4":
            list_systems()

        elif choice == "5":
            name = input("Enter system name to connect: ")
            connect_to_system(name)

        elif choice == "6":
            name = input("Enter system name: ")
            run_command_on_system(name)

        elif choice == "7":
            name = input("Enter system name to get info: ")
            get_system_info(name)

        elif choice == "8":
            print(f"{Fore.YELLOW}👋 Exiting... Goodbye!{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

except KeyboardInterrupt:
    print(f"\n{Fore.YELLOW}👋 Program interrupted by user (Ctrl + C). Exiting safely...{Style.RESET_ALL}")
except EOFError:
    print(f"\n{Fore.YELLOW}👋 Detected Ctrl + Z / EOF. Exiting safely...{Style.RESET_ALL}")
except Exception as e:
    print(f"\n{Fore.RED}⚠️ Unexpected error: {e}{Style.RESET_ALL}")
finally:
    print(f"{Fore.GREEN}✅ Cleanup done. Bye!{Style.RESET_ALL}")
