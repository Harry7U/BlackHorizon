import os
import requests
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Ensure the wordlists directory exists
WORDLIST_DIR = "wordlists"
os.makedirs(WORDLIST_DIR, exist_ok=True)

# Wordlists Mapping - GitHub Raw URLs
WORDLISTS = {
    "subdomains": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
    "directories": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
    "xss": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/Intruders/IntrudersXSS.txt",
    "sqli": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder/Auth_Bypass.txt",
    "sqli_time_based": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder/Time_Based.txt",
    "sqli_blind": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder/Blind.txt",
    "sqli_union": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder/Union.txt",
    "lfi": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Directory%20Traversal/Intruder/lfi.txt",
    "fuzz": "https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt"
}

def download_wordlist(name, url):
    """Downloads a wordlist if not already available."""
    path = os.path.join(WORDLIST_DIR, f"{name}.txt")

    if os.path.exists(path):
        print(Fore.GREEN + f"✅ {name} wordlist already exists.")
        return

    print(Fore.YELLOW + f"⬇️ Downloading {name} wordlist from GitHub...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(Fore.GREEN + f"✅ {name} wordlist saved successfully!")
    except requests.RequestException as e:
        print(Fore.RED + f"⚠️ Failed to fetch {name} wordlist! Error: {e}")

def update_all_wordlists():
    """Ensures all wordlists are present."""
    print(Fore.CYAN + "\n🔄 Checking & Updating Wordlists...\n")
    for name, url in WORDLISTS.items():
        download_wordlist(name, url)
    print(Fore.GREEN + "\n✅ All wordlists are updated and ready!\n")

if __name__ == "__main__":
    update_all_wordlists()
