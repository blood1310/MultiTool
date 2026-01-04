# Personal Multi-Tool 🔥

*A colorful, interactive all-in-one menu for Kali Linux that automatically downloads, installs, and launches popular pentesting tools with just a few clicks.*

## Included Tools

- **Phishing & Social Engineering.**
  - *Zphisher (30+ phishing templates).*
  - *CamPhish (camera phishing).*

- **Anonymity & Privacy.**
  - *Whoami (MAC/IP/Tor/DNS changer).*
  - *IPGhost (fast IP rotation via Tor).*

- **Remote Access & Backdoor (RAT).**
  - *TheFatRat (backdoor generator for Android/Windows/Linux).*

- **Password Attacks & Wordlists.**
  - *CUPP (custom wordlist generator based on victim info).*

- **Device Tracking & OSINT.**
  - *Seeker (precise GPS location via link).*

- **Wi-Fi Cracking.**
  - *AngryOxide (advanced 802.11 attack toolkit).*
  - *Fluxion (Evil Twin + Captive Portal for WPA/WPA2).*

## Requirements:

- *Kali Linux (or any Debian-based distribution).*
- *Python 3 (pre-installed on Kali).*
- *Git.*
- *Internet connection.*
- *Root privileges (most tools require `sudo`).*

## Installation & Usage:

### Method 1: Git Clone (Recommended).

```bash
cd /home/kali
git clone https://github.com/blood1310/MultiTool.git
cd MultiTool
```

### Method 2: Download as .tar.gz (Alternative).


```bash
cd /home/kali
wget https://github.com/blood1310/MultiTool/archive/refs/heads/main.tar.gz -O MultiTool.tar.gz
tar -xzvf MultiTool.tar.gz
mv MultiTool-main MultiTool   # rename the extracted folder
cd MultiTool
```

### Final Steps (for both methods).

1. *(Optional) Make the script executable:*
   
```bash
chmod +x multi-tool.py
```

2. *Always run the script as root:*

```bash
sudo python3 multi-tool.py
```

*The script will automatically create the folder /home/kali/MultiTool/DownloadedTools where all external tools will be cloned and stored.*

# How It Works:

*The first time you select a tool, it will be automatically downloaded, configured (if needed), and launched.
On subsequent uses, the tool will launch directly.
After finishing with a tool, press ENTER to return to the main menu.*

## Special Notes:

### AngryOxide.
*Requires Rust (automatically installed if missing).*
*Needs a wireless interface in monitor mode.*
*The script will list available interfaces and prompt you for the correct one (e.g., wlan0mon).*
*Tip: Put your Wi-Fi card in monitor mode first:*

```bash
sudo airmon-ng start wlan0
```

*(Fluxion Automatically installs any missing dependencies on first launch).*

*Other tools (Zphisher, TheFatRat, Seeker, etc.) manage their own setup automatically).*

# Updating the Multi-Tool

**To get the latest version of the menu and script:**

```bash
cd /home/kali/MultiTool
git pull
```

*To update a specific tool, simply delete its folder inside DownloadedTools and reselect it from the menu — it will be freshly re-cloned.*

## Credits & Original Repositories

*This multi-tool automates the download and execution of the following amazing open-source projects. Huge thanks to their authors!*

*- **Zphisher** → https://github.com/htr-tech/zphisher*
*- **CamPhish** → https://github.com/techchipnet/CamPhish*
*- **Whoami** → https://github.com/owerdogan/whoami-project*
*- **IPGhost** → https://github.com/s-r-e-e-r-a-j/IPGhost*
*- **TheFatRat** → https://github.com/screetsec/TheFatRat*
*- **CUPP** → https://github.com/Mebus/cupp*
*- **Seeker** → https://github.com/thewhiteh4t/seeker*
*- **AngryOxide** → https://github.com/Ragnt/AngryOxide*
*- **Fluxion** → https://github.com/FluxionNetwork/fluxion*

*Respect the original licenses and give proper credit when using these tools individually.*

# Legal Disclaimer
 *This tool is intended only for educational purposes and authorized penetration testing.
Use it exclusively on systems and networks you own or have explicit written permission to test.
The author assumes no responsibility for any misuse or illegal activity.
Enjoy responsibly! 🔥*

***Repository: https://github.com/blood1310/MultiTool***

*Made with 🔥 by [blood1310](https://github.com/blood1310)*


