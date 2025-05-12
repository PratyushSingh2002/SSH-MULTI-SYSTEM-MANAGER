from ssh_manager import *

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
        print(f"{Fore.YELLOW}Exiting... Goodbye!")
        break

    else:
        print(f"{Fore.RED}Invalid choice. Please try again.")

