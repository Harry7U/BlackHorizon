import os
import json
import requests
import subprocess
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Load Configuration
CONFIG_PATH = "config/settings.json"

if not os.path.exists(CONFIG_PATH):
    print(Fore.RED + f"[ERROR] Missing config file: {CONFIG_PATH}")
    exit(1)

with open(CONFIG_PATH) as config_file:
    config = json.load(config_file)

TARGET = config["TARGET"]
WAYBACK_API = "http://web.archive.org/cdx/search/cdx?url={}&output=json"

# Ensure wordlists exist
WORDLISTS_DIR = "wordlists"
COMMON_WORDLIST = os.path.join(WORDLISTS_DIR, "common.txt")

if not os.path.exists(COMMON_WORDLIST):
    print(Fore.YELLOW + "[WARNING] Wordlist not found! Downloading...")
    os.makedirs(WORDLISTS_DIR, exist_ok=True)
    subprocess.run(["wget", "-O", COMMON_WORDLIST, "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt"])

# Function to fetch Wayback URLs
def fetch_wayback_urls():
    print(Fore.CYAN + "[*] Fetching historical URLs from Wayback Machine...")
    try:
        response = requests.get(WAYBACK_API.format(TARGET), timeout=10)
        response.raise_for_status()
        wayback_data = response.json()

        if len(wayback_data) > 1:
            urls = [entry[2] for entry in wayback_data[1:]]
            return list(set(urls))  # Remove duplicates
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[ERROR] Failed to fetch Wayback URLs: {e}")
        return []

# Function to search GitHub for leaks
def search_github_leaks():
    print(Fore.CYAN + "[*] Searching GitHub for leaked credentials...")
    try:
        gh_leaks = subprocess.check_output(["github-dorks", "-t", TARGET]).decode().splitlines()
        return gh_leaks
    except subprocess.CalledProcessError:
        print(Fore.RED + "[ERROR] GitHub Dork search failed.")
        return []

# Main Recon Function
def run_recon():
    print(Fore.GREEN + "[+] Running AI-Powered Reconnaissance...")

    # Fetch Wayback URLs
    wayback_urls = fetch_wayback_urls()
    if wayback_urls:
        print(Fore.YELLOW + f"[+] Found {len(wayback_urls)} historical URLs!")
    else:
        print(Fore.RED + "[!] No Wayback URLs found.")

    # Search GitHub for leaks
    github_leaks = search_github_leaks()
    if github_leaks:
        print(Fore.YELLOW + f"[+] Found {len(github_leaks)} potential GitHub leaks!")

    # Save results to a report
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{TARGET}_recon.json"

    with open(report_path, "w") as report_file:
        json.dump({
            "wayback_urls": wayback_urls,
            "github_leaks": github_leaks
        }, report_file, indent=4)

    print(Fore.GREEN + f"[✓] Recon Report saved: {report_path}")

if __name__ == "__main__":
    run_recon()
