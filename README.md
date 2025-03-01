# 💀 Black Horizon by Harry7U

Black Horizon is an **AI-powered cyber offense suite** designed to automate **reconnaissance, exploitation, C2 (Command & Control), evasion, and anti-forensics**.

## 🚀 Features
✅ **AI-Powered Reconnaissance** – Find subdomains, leaked credentials, and historical URLs  
✅ **Automated Exploitation** – Uses AI to generate payloads for SQLi, XSS, RCE, LFI, and Open Redirects  
✅ **Command & Control (C2)** – Reverse shell, encrypted SSH tunnels, remote execution  
✅ **AI-Based Fuzzing** – Finds hidden parameters, admin panels, and brute-force vulnerable endpoints  
✅ **Privilege Escalation** – Identifies SUID binaries, sudo misconfigurations, and password leaks  
✅ **Evasion & Obfuscation** – Bypasses security monitoring tools using stealth techniques  
✅ **Anti-Forensics** – Clears logs, erases traces, and prevents forensic analysis  

## 📂 Installation
### 🔹 Prerequisites
Ensure **Python 3** and the following dependencies are installed:
```bash
pip install requests colorama waybackpy github3.py scikit-learn paramiko pycryptodome wfuzz
```

### 🔹 Clone the Repository
```bash
git clone https://github.com/Harry7U/BlackHorizon.git
cd BlackHorizon
```

### 🔹 Configure Settings
Edit `config/settings.json`:
```json
{
    "TARGET": "example.com",
    "C2_SERVER": "your-c2-server.com",
    "C2_PORT": 4444,
    "GITHUB_API_KEY": "your_github_token_here",
    "TIMEOUT": 10
}
```

## 🛠 Usage

### 🔥 Run Full Automation
```bash
python blackhorizon.py
```
This will:
1. **Enumerate subdomains, historical URLs, and leaked credentials**
2. **Actively scan for vulnerabilities**
3. **Exploit detected vulnerabilities using AI-powered payloads**
4. **Deploy a C2 (Command & Control) session**
5. **Run fuzzing, privilege escalation, and anti-forensics**
6. **Bypass security defenses using evasion techniques**
7. **Generate comprehensive reports in `/reports/`**

### 📜 Run Individual Modules
- **Reconnaissance:** `python modules/recon.py`
- **Active Vulnerability Scan:** `python modules/active_scan.py`
- **AI-Powered Exploitation:** `python modules/exploit.py`
- **Command & Control (C2):** `python modules/c2.py`
- **AI-Powered Fuzzing:** `python modules/fuzzing.py`
- **Privilege Escalation:** `python modules/priv_esc.py`
- **Evasion:** `python modules/evasion.py`
- **Anti-Forensics:** `python modules/anti_forensics.py`

### 📜 Reports & Logs
All execution logs and scan results are stored in the `reports/` directory:
```bash
ls reports/
example.com_recon.json  example.com_scan.json  example.com_exploit.json
example.com_fuzzing.json example.com_c2.json  example.com_priv_esc.json
example.com_evasion.json example.com_anti_forensics.json
```

## ⚠️ Legal Disclaimer
🚨 **Black Horizon is intended for authorized penetration testing and educational purposes only.**  
🚨 **Unauthorized use is illegal and may result in criminal prosecution.**  
🚨 **Always obtain permission before testing any system.**  

## 🎯 Ready to launch Black Horizon?
```bash
python blackhorizon.py
```

---
💀 **Developed by Harry7U** | 🔥 **Automating Offensive Security with AI** 🚀
