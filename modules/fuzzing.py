import os
import json
import subprocess
from colorama import Fore, Style, init
from wordlists_manager import update_all_wordlists  # Ensure wordlists are available

# Initialize colorama for colored output
init(autoreset=True)

# Load Config
CONFIG_PATH = "config/settings.json"
if not os.path.exists(CONFIG_PATH):
    print(Fore.RED + "[ERROR] Missing config file! Creating a default one...")
    os.makedirs("config", exist_ok=True)
    default_config = {"TARGET": "http://testphp.vulnweb.com"}
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(default_config, config_file, indent=4)

with open(CONFIG_PATH) as config_file:
    config = json.load(config_file)

TARGET = config["TARGET"]
WORDLIST_DIR = "wordlists"

# Ensure wordlists are up-to-date
update_all_wordlists()

# Wordlist paths
FUZZING_WORDLIST = os.path.join(WORDLIST_DIR, "fuzz.txt")

if not os.path.exists(FUZZING_WORDLIST):
    print(Fore.RED + "[ERROR] Fuzzing wordlist not found! Run `wordlists_manager.py` first.")
    exit(1)

# Function to run FFUF for fuzzing
def run_ffuf(url, wordlist, filter_status="404"):
    """Executes FFUF for fuzzing and returns found endpoints."""
    try:
        command = f"ffuf -u {url} -w {wordlist} -fc {filter_status} -of json -o reports/fuzz_results.json"
        print(Fore.CYAN + f"\n🔍 Running Fuzzing on {url} with {wordlist}...")
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(Fore.GREEN + "✅ Fuzzing Completed Successfully!")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[ERROR] FFUF Failed: {e}")
        return []

# Run Fuzzing
def run_fuzzing():
    print(Fore.BLUE + "\n🚀 Running AI-Powered Fuzzing...\n")
    
    endpoints = [
        f"{TARGET}/FUZZ",
        f"{TARGET}/api/FUZZ",
        f"{TARGET}/admin/FUZZ"
    ]

    os.makedirs("reports", exist_ok=True)

    for endpoint in endpoints:
        run_ffuf(endpoint, FUZZING_WORDLIST)

    print(Fore.GREEN + "\n✅ Fuzzing Completed! Results saved in `reports/fuzz_results.json`\n")

if __name__ == "__main__":
    run_fuzzing()
