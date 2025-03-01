import os
import json
import subprocess
import threading
import time
import signal
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load Config
CONFIG_FILE = "config/settings.json"
if not os.path.exists(CONFIG_FILE):
    print(Fore.RED + f"⚠️ Config file {CONFIG_FILE} is missing! Run `setup_config.py`")
    exit(1)

with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

TARGET = config.get("TARGET", "example.com")

# Handle Keyboard Interrupt
def signal_handler(sig, frame):
    print(Fore.RED + "\n⚠️ Process interrupted by user (Ctrl+C). Cleaning up...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Run a module safely
def run_module(module_name, script_path):
    """Runs a module and handles errors."""
    if not os.path.exists(script_path):
        print(Fore.RED + f"❌ Module {module_name} not found: {script_path}")
        return

    print(Fore.CYAN + f"\n🚀 Running {module_name}...\n" + Fore.YELLOW)
    
    start_time = time.time()
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"⚠️ Error in {module_name}: {e}")
    except KeyboardInterrupt:
        print(Fore.RED + f"⚠️ {module_name} interrupted by user.")
        exit(0)

    end_time = time.time()
    print(Fore.GREEN + f"✅ {module_name} completed in {round(end_time - start_time, 2)} seconds.")

# Run all modules
def run_all_modules():
    """Executes all modules in sequence."""
    modules = {
        "Reconnaissance": "modules/recon.py",
        "Active Vulnerability Scan": "modules/active_scan.py",
        "AI-Powered Exploitation": "modules/exploit.py",
        "Command & Control (C2)": "modules/c2.py",
        "AI-Powered Fuzzing": "modules/fuzzing.py",
        "Privilege Escalation": "modules/priv_esc.py",
        "Evasion": "modules/evasion.py",
        "Anti-Forensics": "modules/anti_forensics.py"
    }

    threads = []
    for module_name, script_path in modules.items():
        thread = threading.Thread(target=run_module, args=(module_name, script_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main Execution
def main():
    """Executes all modules."""
    print(Fore.GREEN + "✅ Welcome to Black Horizon – AI-Powered Cyber Offense Suite")
    print(Fore.GREEN + "🚀 Automating Reconnaissance, Exploitation, C2 & Anti-Forensics...\n")

    run_all_modules()

    print(Fore.GREEN + "\n🎯 All modules executed successfully! Reports saved in 'reports/'\n")

if __name__ == "__main__":
    main()
