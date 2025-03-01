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

# Save Privilege Escalation Logs
def log_priv_esc(data):
    os.makedirs("reports", exist_ok=True)
    log_path = f"reports/{TARGET}_priv_esc.json"

    with open(log_path, "w") as log_file:
        json.dump(data, log_file, indent=4)

    print(Fore.GREEN + f"📄 Privilege Escalation Report saved: {log_path}")

# Run system command
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=TIMEOUT)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "❌ Command Timeout!"
    except Exception as e:
        return f"❌ Error: {e}"

# Check SUID Binaries
def check_suid():
    print(Fore.CYAN + "🔍 Searching for SUID Binaries...")
    suid_binaries = run_command("find / -perm -4000 2>/dev/null")
    return suid_binaries.split("\n") if suid_binaries else []

# Check for misconfigured sudo permissions
def check_sudo():
    print(Fore.CYAN + "🔍 Checking for Sudo Misconfigurations...")
    sudo_output = run_command("sudo -l")
    return sudo_output if "may run the following commands" in sudo_output else ""

# Check for passwords in files
def check_passwords():
    print(Fore.CYAN + "🔍 Searching for Passwords in Configuration Files...")
    password_files = run_command("grep -r 'password' /etc 2>/dev/null")
    return password_files if password_files else ""

# Check for writable cron jobs
def check_cron_jobs():
    print(Fore.CYAN + "🔍 Checking for Writable Cron Jobs...")
    cron_jobs = run_command("ls -lah /etc/cron* 2>/dev/null")
    return cron_jobs if cron_jobs else ""

# Check for capabilities
def check_capabilities():
    print(Fore.CYAN + "🔍 Checking for Dangerous Capabilities...")
    capabilities = run_command("getcap -r / 2>/dev/null")
    return capabilities.split("\n") if capabilities else []

# AI-Powered Exploit Suggestion
def suggest_exploit(priv_esc_results):
    print(Fore.YELLOW + "\n🤖 AI-Suggested Exploits:")

    if priv_esc_results["suid"]:
        print(Fore.GREEN + f"🔥 Exploit SUID binary: `{priv_esc_results['suid'][0]}`")
        print(Fore.YELLOW + f"Try: `./{priv_esc_results['suid'][0]}` or find exploits on GTFOBins!")

    if priv_esc_results["sudo"]:
        print(Fore.GREEN + "🔥 Sudo misconfiguration detected! Try: `sudo -l`")
        print(Fore.YELLOW + "Possible command execution: `sudo <command>`")

    if priv_esc_results["passwords"]:
        print(Fore.GREEN + "🔥 Possible Password Leaks Found!")
        print(Fore.YELLOW + "Check manually in `/etc/shadow` or config files.")

    if priv_esc_results["cron_jobs"]:
        print(Fore.GREEN + "🔥 Writable Cron Jobs Detected!")
        print(Fore.YELLOW + "Try injecting a reverse shell in the cron job.")

    if priv_esc_results["capabilities"]:
        print(Fore.GREEN + f"🔥 Dangerous Capability Found: {priv_esc_results['capabilities'][0]}")
        print(Fore.YELLOW + "Try privilege escalation using `getcap` and `setcap`.")

# Main Execution
def main():
    print(Fore.MAGENTA + "🚀 Running AI-Powered Privilege Escalation Analysis...")
    start_time = time.time()

    results = {
        "suid": check_suid(),
        "sudo": check_sudo(),
        "passwords": check_passwords(),
        "cron_jobs": check_cron_jobs(),
        "capabilities": check_capabilities()
    }

    log_priv_esc(results)
    suggest_exploit(results)

    end_time = time.time()
    print(Fore.GREEN + f"✅ Privilege Escalation Analysis completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
