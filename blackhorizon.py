import os
import json
import subprocess
import requests

# Ensure required directories exist
REQUIRED_DIRS = ["config", "modules", "reports", "wordlists"]
for directory in REQUIRED_DIRS:
    os.makedirs(directory, exist_ok=True)

# Load Config
CONFIG_PATH = "config/settings.json"
if not os.path.exists(CONFIG_PATH):
    print("⚠️ Missing configuration file! Creating a default one...")
    default_config = {"TARGET": ""}
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(default_config, config_file, indent=4)

with open(CONFIG_PATH) as config_file:
    config = json.load(config_file)

TARGET = config.get("TARGET", "").strip()

if not TARGET:
    print("⚠️ No target specified in config/settings.json! Please set a valid TARGET.")
    exit(1)

# Ensure wordlists are updated
def update_all_wordlists():
    """Ensures all required wordlists are downloaded."""
    WORDLISTS = {
        "subdomains": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
        "directories": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
        "xss": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/Intruders/IntrudersXSS.txt",
        "sqli": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder/Auth_Bypass.txt",
        "lfi": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Directory%20Traversal/Intruder/lfi.txt",
        "fuzz": "https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt"
    }

    WORDLIST_DIR = "wordlists"
    os.makedirs(WORDLIST_DIR, exist_ok=True)

    for name, url in WORDLISTS.items():
        path = os.path.join(WORDLIST_DIR, f"{name}.txt")
        if not os.path.exists(path):
            print(f"⬇️ Downloading {name} wordlist...")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(path, "w", encoding="utf-8") as file:
                    file.write(response.text)
                print(f"✅ {name} wordlist saved successfully!")
            except requests.RequestException as e:
                print(f"⚠️ Failed to fetch {name} wordlist! Error: {e}")

update_all_wordlists()

# Display Banner
def display_banner():
    """Displays the ASCII art banner."""
    banner_text = """
    ██████╗ ██╗      █████╗  ██████╗██╗  ██╗
    ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝
    ██████╔╝██║     ███████║██║     █████╔╝ 
    ██╔═══╝ ██║     ██╔══██║██║     ██╔═██╗ 
    ██║     ███████╗██║  ██║╚██████╗██║  ██╗
    ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
      Black Horizon - AI-Powered Cyber Offense Suite
    -----------------------------------------------
    Automating Reconnaissance, Exploitation, C2 & Evasion
    """
    print(banner_text)

# Run a module and handle errors
def run_module(module_name, script_path):
    """Runs a module and handles errors."""
    print(f"\n🚀 Running {module_name}...\n")
    try:
        subprocess.run(["python3", script_path], check=True)
    except FileNotFoundError:
        print(f"⚠️ Module {script_path} not found!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error in {module_name}: {e}")

# Main Execution
def main():
    """Executes all modules in sequence."""
    display_banner()

    print("✅ Welcome to Black Horizon – AI-Powered Cyber Offense Suite")
    print("🚀 Automating Reconnaissance, Exploitation, C2 & Anti-Forensics...\n")

    MODULES = {
        "Reconnaissance": "modules/recon.py",
        "Active Vulnerability Scan": "modules/active_scan.py",
        "AI-Powered Exploitation": "modules/exploit.py",
        "Command & Control (C2)": "modules/c2.py",
        "Fuzzing": "modules/fuzzing.py",
        "Privilege Escalation": "modules/priv_esc.py",
        "Evasion": "modules/evasion.py",
        "Anti-Forensics": "modules/anti_forensics.py"
    }

    for module, path in MODULES.items():
        run_module(module, path)

    print("\n🎯 All modules executed successfully! Reports saved in 'reports/'\n")

if __name__ == "__main__":
    main()
