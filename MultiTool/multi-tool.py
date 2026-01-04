#!/usr/bin/env python3
import os
import subprocess
import sys
from time import sleep

TOOLS_DIR = "/home/kali/MyTool/DownloadedTools"

def print_banner():
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
    print("\033[93m IL TUO MULTI-TOOL PERSONALE\033[0m\n")

def create_tools_dir():
    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR, exist_ok=True)
        print(f"[+] Cartella {TOOLS_DIR} creata!")

def clone_and_setup(repo, folder_name, clone_extra="", initial_setup_cmd=None):
    path = os.path.join(TOOLS_DIR, folder_name)
    if not os.path.exists(path):
        print(f"[+] Scaricamento {folder_name} in corso...")
        subprocess.run(f"git clone {clone_extra} {repo} {path}", shell=True, check=True)
        os.chdir(path)
        if initial_setup_cmd:
            print("[+] Esecuzione setup iniziale...")
            subprocess.run(initial_setup_cmd, shell=True)
        os.chdir(TOOLS_DIR)
    else:
        print(f"[+] {folder_name} già presente!")
    os.chdir(path)

    # Avvio specifico per ogni tool
    if folder_name == "CamPhish":
        subprocess.run("bash camphish.sh", shell=True)
    elif folder_name == "whoami-project":
        subprocess.run("sudo kali-whoami", shell=True)
    elif folder_name == "IPGhost":
        subprocess.run("bash IPGhost/ipghost.sh", shell=True)
    elif folder_name == "TheFatRat":
        config_file = os.path.join(path, "config", "config")
        if not os.path.exists(config_file):
            print("[+] Configurazione mancante → Esecuzione automatica di setup.sh...")
            subprocess.run("chmod +x setup.sh && ./setup.sh", shell=True, input=b'\n')
        subprocess.run("chmod +x fatrat && ./fatrat", shell=True)
    elif folder_name == "cupp":
        subprocess.run("./cupp.py -i", shell=True)
    elif folder_name == "zphisher":
        subprocess.run("bash zphisher.sh", shell=True)
    elif folder_name == "seeker":
        subprocess.run("python3 seeker.py", shell=True)
    elif folder_name == "fluxion":
        print("\033[92m[+] Avvio Fluxion (installa automaticamente dipendenze mancanti)...\033[0m")
        subprocess.run("./fluxion.sh", shell=True)
    elif folder_name == "AngryOxide":
        # Installa Rust se necessario
        if subprocess.run(["which", "cargo"], capture_output=True).returncode != 0:
            print("[+] Installazione Rust (necessaria per AngryOxide)...")
            subprocess.run('curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y', shell=True)
            os.environ["PATH"] += ":/root/.cargo/bin"
            print("[+] Rust installato. Ricarica la shell se necessario.")

        print("[+] Compilazione e installazione AngryOxide...")
        result = subprocess.run("make && sudo make install", shell=True)
        if result.returncode != 0:
            print("\033[91m[!] Errore durante compilazione/installazione di AngryOxide.\033[0m")
        else:
            print("\033[92m[+] AngryOxide installato con successo!\033[0m")

        # Chiedi interfaccia Wi-Fi
        print("\n\033[93mAngryOxide richiede un'interfaccia Wi-Fi in monitor mode.\033[0m")
        print("Esempi: wlan0, wlan0mon, wlp3s0mon\n")
        print("Interfacce rilevate:")
        subprocess.run("iwconfig 2>/dev/null | grep -o '^[a-z0-9]*' | grep -v '^lo$' || echo 'Nessuna trovata'", shell=True)

        interface = input("\n\033[94mInserisci interfaccia (es. wlan0mon) o INVIO per help: \033[0m").strip()

        if interface:
            print(f"\033[92m[+] Avvio AngryOxide su {interface}...\033[0m")
            subprocess.run(f"sudo angryoxide --interface {interface}", shell=True)
        else:
            print("\033[93mMostro l'help di AngryOxide...\033[0m")
            subprocess.run("sudo angryoxide --help", shell=True)

    os.chdir(TOOLS_DIR)
    input("\nPremi INVIO per tornare al menu...")

# MENU PRINCIPALE
def main_menu():
    create_tools_dir()
    while True:
        print_banner()
        print("\033[95m╔════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[95m║ MENU PRINCIPALE ║\033[0m")
        print("\033[95m╚════════════════════════════════════════════════════════════╝\033[0m\n")

        print("\033[1m\033[95m[1] PHISHING & SOCIAL ENGINEERING\033[0m")
        print(" - Zphisher (phishing con 30+ template)")
        print(" - CamPhish (hack camera via phishing)\n")

        print("\033[1m\033[96m[2] ANONYMITY & PRIVACY\033[0m")
        print(" - Whoami (cambia MAC, IP, Tor, DNS)")
        print(" - IPGhost (cambio IP rapido con Tor)\n")

        print("\033[1m\033[91m[3] REMOTE ACCESS & BACKDOOR (RAT)\033[0m")
        print(" - TheFatRat (genera backdoor Android/Windows/Linux)\n")

        print("\033[1m\033[93m[4] PASSWORD ATTACKS & WORDLIST\033[0m")
        print(" - CUPP (crea wordlist personalizzate dalla vittima)\n")

        print("\033[1m\033[92m[5] DEVICE TRACKING & OSINT\033[0m")
        print(" - Seeker (posizione GPS precisa via link)\n")

        print("\033[1m\033[94m[6] WI-FI CRACKING\033[0m")
        print(" - AngryOxide (802.11 attack tool avanzato)")
        print(" - Fluxion (Evil Twin + Captive Portal WPA/WPA2)\n")

        print("\033[1m\033[91m[7] ESCI\033[0m\n")

        choice = input("\033[94mSeleziona categoria (1-7): \033[0m")
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
            print("\033[91mArrivederci boss! 🔥\033[0m")
            sys.exit()
        else:
            print("\033[91mScelta non valida! Riprova.\033[0m")
            sleep(1)

def menu_phishing():
    while True:
        os.system("clear")
        print_banner()
        print("\033[95m╔════════════════════════════════════╗\033[0m")
        print("\033[95m║ PHISHING & SOCIAL ENGINEERING ║\033[0m")
        print("\033[95m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Zphisher")
        print("\033[92m[2]\033[0m CamPhish")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1": clone_and_setup("https://github.com/htr-tech/zphisher.git", "zphisher")
        elif sub == "2": clone_and_setup("https://github.com/techchipnet/CamPhish.git", "CamPhish")
        elif sub == "0": return
        else: print("\033[91mScelta non valida!\033[0m"); sleep(1)

def menu_anonymity():
    while True:
        os.system("clear")
        print_banner()
        print("\033[96m╔════════════════════════════╗\033[0m")
        print("\033[96m║ ANONYMITY & PRIVACY ║\033[0m")
        print("\033[96m╚════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Whoami")
        print("\033[92m[2]\033[0m IPGhost")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1": clone_and_setup("https://github.com/owerdogan/whoami-project.git", "whoami-project", "", "sudo apt update && sudo apt install -y tar tor curl python3 python3-scapy network-manager && sudo make install")
        elif sub == "2": clone_and_setup("https://github.com/s-r-e-e-r-a-j/IPGhost.git", "IPGhost", "", "sudo bash install.sh")
        elif sub == "0": return
        else: print("\033[91mScelta non valida!\033[0m"); sleep(1)

def menu_rat():
    while True:
        os.system("clear")
        print_banner()
        print("\033[91m╔════════════════════════════════════╗\033[0m")
        print("\033[91m║ REMOTE ACCESS & BACKDOOR (RAT) ║\033[0m")
        print("\033[91m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m TheFatRat")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1": clone_and_setup("https://github.com/screetsec/TheFatRat.git", "TheFatRat", "", "chmod +x setup.sh")
        elif sub == "0": return
        else: print("\033[91mScelta non valida!\033[0m"); sleep(1)

def menu_password():
    while True:
        os.system("clear")
        print_banner()
        print("\033[93m╔════════════════════════════════════╗\033[0m")
        print("\033[93m║ PASSWORD ATTACKS & WORDLIST ║\033[0m")
        print("\033[93m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m CUPP")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1": clone_and_setup("https://github.com/Mebus/cupp.git", "cupp")
        elif sub == "0": return
        else: print("\033[91mScelta non valida!\033[0m"); sleep(1)

def menu_tracking():
    while True:
        os.system("clear")
        print_banner()
        print("\033[92m╔════════════════════════════════════╗\033[0m")
        print("\033[92m║ DEVICE TRACKING & OSINT ║\033[0m")
        print("\033[92m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Seeker")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1": clone_and_setup("https://github.com/thewhiteh4t/seeker.git", "seeker", "", "chmod +x install.sh && ./install.sh")
        elif sub == "0": return
        else: print("\033[91mScelta non valida!\033[0m"); sleep(1)

def menu_wifi_cracking():
    while True:
        os.system("clear")
        print_banner()
        print("\033[94m╔══════════════════════════╗\033[0m")
        print("\033[94m║ WI-FI CRACKING ║\033[0m")
        print("\033[94m╚══════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m AngryOxide")
        print("\033[92m[2]\033[0m Fluxion")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/Ragnt/AngryOxide.git", "AngryOxide", "--recurse-submodules")
        elif sub == "2":
            clone_and_setup("https://github.com/FluxionNetwork/fluxion.git", "fluxion")
        elif sub == "0":
            return
        else:
            print("\033[91mScelta non valida!\033[0m")
            sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("\033[91m[!] Esegui come root: sudo python3 multi-tool.py\033[0m")
        sleep(3)
        sys.exit()
    main_menu()