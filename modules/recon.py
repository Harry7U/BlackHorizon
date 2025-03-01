import os
import json
import time
import requests
from colorama import Fore, Style, init
from waybackpy import WaybackMachineCDXServerAPI

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
GITHUB_API_KEY = config.get("GITHUB_API_KEY", "")
TIMEOUT = config.get("TIMEOUT", 10)

# Function to fetch historical URLs from Wayback Machine
def fetch_wayback_urls():
    print(Fore.CYAN + "🔍 Fetching historical URLs from Wayback Machine...")

    try:
        wayback = WaybackMachineCDXServerAPI(TARGET)
        urls = [entry["url"] for entry in wayback.snapshots()]
        
        if urls:
            print(Fore.GREEN + f"✅ Found {len(urls)} historical URLs.")
            return urls
        else:
            print(Fore.YELLOW + "⚠️ No historical URLs found.")
            return []

    except Exception as e:
        print(Fore.RED + f"❌ Error fetching Wayback URLs: {e}")
        return []

# Function to search for sensitive leaks in GitHub
def search_github_leaks():
    print(Fore.CYAN + "🔍 Searching for potential leaks on GitHub...")

    if not GITHUB_API_KEY:
        print(Fore.RED + "⚠️ No GitHub API Key found in settings.json! Skipping GitHub Recon.")
        return []

    headers = {"Authorization": f"token {GITHUB_API_KEY}"}
    query = f"{TARGET} in:file"
    url = f"https://api.github.com/search/code?q={query}"

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code == 403:
            print(Fore.RED + "❌ GitHub API rate limit exceeded! Try again later.")
            return []
        elif response.status_code != 200:
            print(Fore.RED + f"❌ Error fetching GitHub results: {response.text}")
            return []

        results = response.json().get("items", [])
        leak_urls = [item["html_url"] for item in results]

        if leak_urls:
            print(Fore.GREEN + f"✅ Found {len(leak_urls)} potential leaks!")
            return leak_urls
        else:
            print(Fore.YELLOW + "⚠️ No leaks found on GitHub.")
            return []

    except Exception as e:
        print(Fore.RED + f"❌ Error searching GitHub: {e}")
        return []

# Save Recon Results
def save_results(data, filename):
    os.makedirs("reports", exist_ok=True)
    filepath = f"reports/{filename}"

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    print(Fore.GREEN + f"📄 Recon Report saved: {filepath}")

# Main Execution
def main():
    print(Fore.MAGENTA + "🚀 Running AI-Powered Reconnaissance...")
    start_time = time.time()

    wayback_urls = fetch_wayback_urls()
    github_leaks = search_github_leaks()

    recon_data = {
        "wayback_urls": wayback_urls,
        "github_leaks": github_leaks
    }

    save_results(recon_data, f"{TARGET}_recon.json")

    end_time = time.time()
    print(Fore.GREEN + f"✅ Reconnaissance completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
