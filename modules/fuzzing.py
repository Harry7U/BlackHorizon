import os
import subprocess

TARGET = "testphp.vulnweb.com"
fuzz_wordlist = "wordlists/fuzz.txt"

if not os.path.exists(fuzz_wordlist):
    print("❌ Missing fuzzing wordlist! Run `python wordlists_manager.py` first.")
    exit(1)

# Run fuzzing
print("🔍 Running AI-Powered Fuzzing...")
fuzz_results = subprocess.run(["wfuzz", "-w", fuzz_wordlist, f"http://{TARGET}/FUZZ"], capture_output=True, text=True)
print(fuzz_results.stdout)
