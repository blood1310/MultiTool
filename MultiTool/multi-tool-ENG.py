#!/usr/bin/env python3
import os
import subprocess
import sys
from time import sleep

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "DownloadedTools")

# Controlla se il disclaimer è già stato mostrato
disclaimer_shown = False

def print_banner():
    global disclaimer_shown
    os.system("clear")
    print("\033[91m" + r"""
 ________ ___       ________  ___      ___ ___  ________          ________  ________  _____ ______   ________  ________     
|\  _____\\  \     |\   __  \|\  \    /  /|\  \|\   __  \        |\   __  \|\   __  \|\   _ \  _   \|\   __  \|\   __  \    
\ \  \__/\ \  \    \ \  \|\  \ \  \  /  / | \  \ \  \|\  \       \ \  \|\ /\ \  \|\  \ \  \\\__\ \  \ \  \|\ /\ \  \|\  \   
 \ \   __\\ \  \    \ \   __  \ \  \/  / / \ \  \ \  \\\  \       \ \   __  \ \  \\\  \ \  \\|__| \  \ \   __  \ \   __  \  
  \ \  \_| \ \  \____\ \  \ \  \ \    / /   \ \  \ \  \\\  \       \ \  \|\  \ \  \\\  \ \  \    \ \  \ \  \|\  \ \  \ \  \ 
   \ \__\   \ \_______\ \__\ \__\ \__/ /     \ \__\ \_______\       \ \_______\ \_______\ \__\    \ \__\ \_______\ \__\ \__\
    \|__|    \|_______|\|__|\|__|\|__|/       \|__|\|_______|        \|_______|\|_______|\|__|     \|__|\|_______|\|__|\|__|
    """ + "\033[0m")
    print("\033[93m BLOOD1310 TOOL 🔥 \033[0m\n")

    # Mostra il disclaimer SOLO la prima volta
    if not disclaimer_shown:
        print("\033[91m" + "="*70 + "\033[0m")
        print("\033[1m\033[93m LEGAL WARNING\033[0m")
        print("\033[91m" + "="*70 + "\033[0m")
        print("\033[97mThis tool is intended only for educational purposes and")
        print("authorized penetration testing.\n")
        print("Use it exclusively on systems and networks you own or")
        print("have explicit written permission to test.\n")
        print("The author assumes no responsibility for any misuse")
        print("or illegal activity.\033[0m")
        print("\033[91m" + "="*70 + "\033[0m\n")
        input("\033[94mPress ENTER to accept and continue...\033[0m")
        disclaimer_shown = True

def create_tools_dir():
    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR, exist_ok=True)
        print(f"[+] Folder {TOOLS_DIR} created!")

def clone_and_setup(repo, folder_name, clone_extra="", initial_setup_cmd=None):
    path = os.path.join(TOOLS_DIR, folder_name)
    if not os.path.exists(path):
        print(f"[+] Downloading {folder_name}...")
        subprocess.run(f"git clone {clone_extra} {repo} {path}", shell=True, check=True)
        os.chdir(path)
        if initial_setup_cmd:
            print("[+] Running initial setup...")
            subprocess.run(initial_setup_cmd, shell=True)
        os.chdir(TOOLS_DIR)
    else:
        print(f"[+] {folder_name} already present!")
    os.chdir(path)

    # Tool-specific launch with full path fix
    if folder_name == "CamPhish":
        subprocess.run("bash camphish.sh", shell=True)

    elif folder_name == "whoami-project":
        print("\033[92m[+] Starting Whoami anonymity mode (--start)...\033[0m")
        subprocess.run("sudo kali-whoami --start", shell=True)

    elif folder_name == "IPGhost":
        subprocess.run("bash IPGhost/ipghost.sh", shell=True)

    elif folder_name == "TheFatRat":
        os.chdir(path)  # Entra nella directory di TheFatRat

        # Controlla se la configurazione esiste
        config_dir = os.path.join(path, "config")
        config_file = os.path.join(config_dir, "config")
        if not os.path.exists(config_dir) or not os.path.isfile(config_file):
            print("\033[93m[+] TheFatRat configuration missing → Fixing automatically...\033[0m")

            # Installa zipalign manualmente se non presente (problema principale su Kali recenti)
            if subprocess.run(["which", "zipalign"], capture_output=True).returncode != 0:
                print("[+] Downloading and installing zipalign (required for Android payloads)...")
                subprocess.run([
                    "wget", "https://raw.githubusercontent.com/Screetsec/TheFatRat/master/zipalign",
                    "-O", "zipalign"
                ], check=False)
                subprocess.run(["chmod", "+x", "zipalign"], check=True)
                subprocess.run(["sudo", "mv", "zipalign", "/usr/bin/"], check=True)
                print("\033[92m[+] zipalign successfully installed in /usr/bin/\033[0m")

            # Esegui setup.sh
            print("[+] Running TheFatRat setup (may take a while the first time)...")
            subprocess.run(["chmod", "+x", "setup.sh"], check=True)
            # Invia "Y" e alcuni ENTER per accettare tutto automaticamente
            setup_process = subprocess.Popen(["./setup.sh"], stdin=subprocess.PIPE)
            setup_process.communicate(input=b'Y\n\n\n\n\n')

            # Verifica finale
            if os.path.exists(config_file):
                print("\033[92m[+] Configuration created successfully!\033[0m")
            else:
                print("\033[91m[!] Configuration still missing. Try running ./setup.sh manually inside the folder.\033[0m")

        # Avvia TheFatRat
        print("\n\033[92m[+] Starting TheFatRat...\033[0m")
        subprocess.run(["chmod", "+x", "fatrat"], check=True)
        subprocess.run(["./fatrat"])

        # Torna alla directory principale e attendi input
        os.chdir(TOOLS_DIR)
        input("\n\033[94mPress ENTER to return to the main menu...\033[0m")

    elif folder_name == "cupp":
        subprocess.run("./cupp.py -i", shell=True)

    elif folder_name == "zphisher":
        script_path = os.path.join(path, "zphisher.sh")
        if os.path.exists(script_path):
            subprocess.run(f"chmod +x \"{script_path}\"", shell=True)
            subprocess.run(f"bash \"{script_path}\"", shell=True)
        else:
            print("\033[91m[!] Critical error: zphisher.sh not found!\033[0m")
            print(f"Expected path: {script_path}")
            print("\033[93mSuggestion: Delete the folder and try again:\033[0m")
            print(f"rm -rf {path}")

    elif folder_name == "seeker":
        subprocess.run("python3 seeker.py", shell=True)

    elif folder_name == "fluxion":
        script_path = os.path.join(path, "fluxion.sh")
        print("\033[92m[+] Starting Fluxion...\033[0m")
        if os.path.exists(script_path):
            subprocess.run(["chmod", "+x", script_path])
            subprocess.run(["bash", script_path])
        else:
            print("\033[91m[!] Critical error: fluxion.sh not found!\033[0m")

    elif folder_name == "AngryOxide":
        if subprocess.run(["which", "cargo"], capture_output=True).returncode != 0:
            print("[+] Installing Rust (required for AngryOxide)...")
            subprocess.run('curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y', shell=True)
            os.environ["PATH"] += ":/root/.cargo/bin"
            print("[+] Rust installed. Reload shell if needed.")
        print("[+] Building and installing AngryOxide...")
        result = subprocess.run("make && sudo make install", shell=True)
        if result.returncode != 0:
            print("\033[91m[!] Error during build/install of AngryOxide.\033[0m")
        else:
            print("\033[92m[+] AngryOxide successfully installed!\033[0m")
        print("\n\033[93mAngryOxide requires a wireless interface in monitor mode.\033[0m")
        print("Examples: wlan0, wlan0mon, wlp3s0mon\n")
        print("Detected interfaces:")
        subprocess.run("iwconfig 2>/dev/null | grep -o '^[a-z0-9]*' | grep -v '^lo$' || echo 'None found'", shell=True)
        interface = input("\n\033[94mEnter interface (e.g. wlan0mon) or press ENTER for help: \033[0m").strip()
        if interface:
            print(f"\033[92m[+] Starting AngryOxide on {interface}...\033[0m")
            subprocess.run(f"sudo angryoxide --interface {interface}", shell=True)
        else:
            print("\033[93mShowing AngryOxide help...\033[0m")
            subprocess.run("sudo angryoxide --help", shell=True)
        os.chdir(TOOLS_DIR)
        input("\nPress ENTER to return to the menu...")

# MAIN MENU
def main_menu():
    create_tools_dir()
    while True:
        print_banner()
        print("\033[95m╔════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[95m║ MAIN MENU ║\033[0m")
        print("\033[95m╚════════════════════════════════════════════════════════════╝\033[0m\n")
        print("\033[1m\033[95m[1] PHISHING & SOCIAL ENGINEERING\033[0m")
        print(" - Zphisher (phishing with 30+ templates)")
        print(" - CamPhish (camera hack via phishing)\n")
        print("\033[1m\033[96m[2] ANONYMITY & PRIVACY\033[0m")
        print(" - Whoami (change MAC, IP, Tor, DNS)")
        print(" - IPGhost (fast IP change via Tor)\n")
        print("\033[1m\033[91m[3] REMOTE ACCESS & BACKDOOR (RAT)\033[0m")
        print(" - TheFatRat (generate backdoor for Android/Windows/Linux)\n")
        print("\033[1m\033[93m[4] PASSWORD ATTACKS & WORDLIST\033[0m")
        print(" - CUPP (create custom wordlists based on victim info)\n")
        print("\033[1m\033[92m[5] DEVICE TRACKING & OSINT\033[0m")
        print(" - Seeker (precise GPS location via link)\n")
        print("\033[1m\033[94m[6] WI-FI CRACKING\033[0m")
        print(" - AngryOxide (advanced 802.11 attack tool)")
        print(" - Fluxion (Evil Twin + Captive Portal WPA/WPA2)\n")
        print("\033[1m\033[91m[7] EXIT\033[0m\n")
        choice = input("\033[94mSelect category (1-7): \033[0m")
        if choice == "1":
            menu_phishing()
        elif choice == "2":
            menu_anonymity()
        elif choice == "3":
            menu_rat()
        elif choice == "4":
            menu_password()
        elif choice == "5":
            menu_tracking()
        elif choice == "6":
            menu_wifi_cracking()
        elif choice == "7":
            print("\033[91mGoodbye boss! 🔥\033[0m")
            sys.exit()
        else:
            print("\033[91mInvalid choice! Try again.\033[0m")
            sleep(1)

# Submenus
def menu_phishing():
    while True:
        os.system("clear")
        print_banner()
        print("\033[95m╔════════════════════════════════════╗\033[0m")
        print("\033[95m║ PHISHING & SOCIAL ENGINEERING ║\033[0m")
        print("\033[95m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Zphisher")
        print("\033[92m[2]\033[0m CamPhish")
        print("\033[91m[0]\033[0m Back to main menu\n")
        sub = input("\033[94mSelect tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/htr-tech/zphisher.git", "zphisher")
        elif sub == "2":
            clone_and_setup("https://github.com/techchipnet/CamPhish.git", "CamPhish")
        elif sub == "0":
            return
        else:
            print("\033[91mInvalid choice!\033[0m")
            sleep(1)

def menu_anonymity():
    while True:
        os.system("clear")
        print_banner()
        print("\033[96m╔════════════════════════════╗\033[0m")
        print("\033[96m║ ANONYMITY & PRIVACY ║\033[0m")
        print("\033[96m╚════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Whoami")
        print("\033[92m[2]\033[0m IPGhost")
        print("\033[91m[0]\033[0m Back to main menu\n")
        sub = input("\033[94mSelect tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/owerdogan/whoami-project.git", "whoami-project", "", "sudo apt update && sudo apt install -y tar tor curl python3 python3-scapy network-manager && sudo make install")
        elif sub == "2":
            clone_and_setup("https://github.com/s-r-e-e-r-a-j/IPGhost.git", "IPGhost", "", "sudo bash install.sh")
        elif sub == "0":
            return
        else:
            print("\033[91mInvalid choice!\033[0m")
            sleep(1)

def menu_rat():
    while True:
        os.system("clear")
        print_banner()
        print("\033[91m╔════════════════════════════════════╗\033[0m")
        print("\033[91m║ REMOTE ACCESS & BACKDOOR (RAT) ║\033[0m")
        print("\033[91m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m TheFatRat")
        print("\033[91m[0]\033[0m Back to main menu\n")
        sub = input("\033[94mSelect tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/screetsec/TheFatRat.git", "TheFatRat", "", "chmod +x setup.sh")
        elif sub == "0":
            return
        else:
            print("\033[91mInvalid choice!\033[0m")
            sleep(1)

def menu_password():
    while True:
        os.system("clear")
        print_banner()
        print("\033[93m╔════════════════════════════════════╗\033[0m")
        print("\033[93m║ PASSWORD ATTACKS & WORDLIST ║\033[0m")
        print("\033[93m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m CUPP")
        print("\033[91m[0]\033[0m Back to main menu\n")
        sub = input("\033[94mSelect tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/Mebus/cupp.git", "cupp")
        elif sub == "0":
            return
        else:
            print("\033[91mInvalid choice!\033[0m")
            sleep(1)

def menu_tracking():
    while True:
        os.system("clear")
        print_banner()
        print("\033[92m╔════════════════════════════════════╗\033[0m")
        print("\033[92m║ DEVICE TRACKING & OSINT ║\033[0m")
        print("\033[92m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Seeker")
        print("\033[91m[0]\033[0m Back to main menu\n")
        sub = input("\033[94mSelect tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/thewhiteh4t/seeker.git", "seeker", "", "chmod +x install.sh && ./install.sh")
        elif sub == "0":
            return
        else:
            print("\033[91mInvalid choice!\033[0m")
            sleep(1)

def menu_wifi_cracking():
    while True:
        os.system("clear")
        print_banner()
        print("\033[94m╔══════════════════════════╗\033[0m")
        print("\033[94m║ WI-FI CRACKING ║\033[0m")
        print("\033[94m╚══════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m AngryOxide")
        print("\033[92m[2]\033[0m Fluxion")
        print("\033[91m[0]\033[0m Back to main menu\n")
        sub = input("\033[94mSelect tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/Ragnt/AngryOxide.git", "AngryOxide", "--recurse-submodules")
        elif sub == "2":
            clone_and_setup("https://github.com/FluxionNetwork/fluxion.git", "fluxion")
        elif sub == "0":
            return
        else:
            print("\033[91mInvalid choice!\033[0m")
            sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("\033[91m[!] Run as root: sudo python3 multi-tool-ENG.py\033[0m")
        sleep(3)
        sys.exit()
    main_menu()