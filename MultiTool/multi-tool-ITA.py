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
        print("\033[1m\033[93m AVVISO LEGALE\033[0m")
        print("\033[91m" + "="*70 + "\033[0m")
        print("\033[97mQuesto tool è destinato esclusivamente a scopi educativi e")
        print("penetration testing autorizzato.\n")
        print("Utilizzalo solo su sistemi e reti di tua proprietà o")
        print("per cui hai esplicito permesso scritto di testare.\n")
        print("L'autore non si assume alcuna responsabilità per usi impropri")
        print("o attività illegali.\033[0m")
        print("\033[91m" + "="*70 + "\033[0m\n")
        input("\033[94mPremi INVIO per accettare e continuare...\033[0m")
        disclaimer_shown = True

def create_tools_dir():
    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR, exist_ok=True)
        print(f"[+] Cartella {TOOLS_DIR} creata!")

def clone_and_setup(repo, folder_name, clone_extra="", initial_setup_cmd=None):
    path = os.path.join(TOOLS_DIR, folder_name)
    if not os.path.exists(path):
        print(f"[+] Download di {folder_name} in corso...")
        subprocess.run(f"git clone {clone_extra} {repo} {path}", shell=True, check=True)
        os.chdir(path)
        if initial_setup_cmd:
            print("[+] Esecuzione configurazione iniziale...")
            subprocess.run(initial_setup_cmd, shell=True)
        os.chdir(TOOLS_DIR)
    else:
        print(f"[+] {folder_name} già presente!")
    os.chdir(path)

    # Avvio specifico per ogni tool
    if folder_name == "CamPhish":
        subprocess.run("bash camphish.sh", shell=True)

    elif folder_name == "whoami-project":
        print("\033[92m[+] Avvio modalità anonimato Whoami (--start)...\033[0m")
        subprocess.run("sudo kali-whoami --start", shell=True)

    elif folder_name == "IPGhost":
        subprocess.run("bash IPGhost/ipghost.sh", shell=True)

    elif folder_name == "TheFatRat":
        os.chdir(path)

        config_dir = os.path.join(path, "config")
        config_file = os.path.join(config_dir, "config")
        if not os.path.exists(config_dir) or not os.path.isfile(config_file):
            print("\033[93m[+] Configurazione TheFatRat mancante → Correzione automatica in corso...\033[0m")

            if subprocess.run(["which", "zipalign"], capture_output=True).returncode != 0:
                print("[+] Download e installazione di zipalign (necessario per payload Android)...")
                subprocess.run([
                    "wget", "https://raw.githubusercontent.com/Screetsec/TheFatRat/master/zipalign",
                    "-O", "zipalign"
                ], check=False)
                subprocess.run(["chmod", "+x", "zipalign"], check=True)
                subprocess.run(["sudo", "mv", "zipalign", "/usr/bin/"], check=True)
                print("\033[92m[+] zipalign installato con successo in /usr/bin/\033[0m")

            print("[+] Esecuzione setup di TheFatRat (potrebbe richiedere qualche minuto la prima volta)...")
            subprocess.run(["chmod", "+x", "setup.sh"], check=True)
            setup_process = subprocess.Popen(["./setup.sh"], stdin=subprocess.PIPE)
            setup_process.communicate(input=b'Y\n\n\n\n\n')

            if os.path.exists(config_file):
                print("\033[92m[+] Configurazione creata con successo!\033[0m")
            else:
                print("\033[91m[!] Configurazione ancora mancante. Prova a eseguire ./setup.sh manualmente nella cartella.\033[0m")

        print("\n\033[92m[+] Avvio di TheFatRat...\033[0m")
        subprocess.run(["chmod", "+x", "fatrat"], check=True)
        subprocess.run(["./fatrat"])

        os.chdir(TOOLS_DIR)
        input("\n\033[94mPremi INVIO per tornare al menu principale...\033[0m")

    elif folder_name == "cupp":
        subprocess.run("./cupp.py -i", shell=True)

    elif folder_name == "zphisher":
        script_path = os.path.join(path, "zphisher.sh")
        if os.path.exists(script_path):
            subprocess.run(f"chmod +x \"{script_path}\"", shell=True)
            subprocess.run(f"bash \"{script_path}\"", shell=True)
        else:
            print("\033[91m[!] Errore critico: zphisher.sh non trovato!\033[0m")
            print(f"Percorso atteso: {script_path}")
            print("\033[93mSuggerimento: Elimina la cartella e riprova:\033[0m")
            print(f"rm -rf {path}")

    elif folder_name == "seeker":
        subprocess.run("python3 seeker.py", shell=True)

    elif folder_name == "fluxion":
        script_path = os.path.join(path, "fluxion.sh")
        print("\033[92m[+] Avvio di Fluxion...\033[0m")
        if os.path.exists(script_path):
            subprocess.run(["chmod", "+x", script_path])
            subprocess.run(["bash", script_path])
        else:
            print("\033[91m[!] Errore critico: fluxion.sh non trovato!\033[0m")

    elif folder_name == "AngryOxide":
        if subprocess.run(["which", "cargo"], capture_output=True).returncode != 0:
            print("[+] Installazione di Rust (necessario per AngryOxide)...")
            subprocess.run('curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y', shell=True)
            os.environ["PATH"] += ":/root/.cargo/bin"
            print("[+] Rust installato. Ricarica la shell se necessario.")
        print("[+] Compilazione e installazione di AngryOxide...")
        result = subprocess.run("make && sudo make install", shell=True)
        if result.returncode != 0:
            print("\033[91m[!] Errore durante compilazione/installazione di AngryOxide.\033[0m")
        else:
            print("\033[92m[+] AngryOxide installato con successo!\033[0m")
        print("\n\033[93mAngryOxide richiede un'interfaccia wireless in modalità monitor.\033[0m")
        print("Esempi: wlan0, wlan0mon, wlp3s0mon\n")
        print("Interfacce rilevate:")
        subprocess.run("iwconfig 2>/dev/null | grep -o '^[a-z0-9]*' | grep -v '^lo$' || echo 'Nessuna trovata'", shell=True)
        interface = input("\n\033[94mInserisci interfaccia (es. wlan0mon) o premi INVIO per aiuto: \033[0m").strip()
        if interface:
            print(f"\033[92m[+] Avvio di AngryOxide su {interface}...\033[0m")
            subprocess.run(f"sudo angryoxide --interface {interface}", shell=True)
        else:
            print("\033[93mMostro l'aiuto di AngryOxide...\033[0m")
            subprocess.run("sudo angryoxide --help", shell=True)
        os.chdir(TOOLS_DIR)
        input("\nPremi INVIO per tornare al menu...")

# MENU PRINCIPALE
def main_menu():
    create_tools_dir()
    while True:
        print_banner()
        print("\033[95m╔════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[95m║ MENU PRINCIPALE                                           ║\033[0m")
        print("\033[95m╚════════════════════════════════════════════════════════════╝\033[0m\n")
        print("\033[1m\033[95m[1] PHISHING & SOCIAL ENGINEERING\033[0m")
        print(" - Zphisher (phishing con oltre 30 template)")
        print(" - CamPhish (accesso camera tramite phishing)\n")
        print("\033[1m\033[96m[2] ANONYMITY & PRIVACY\033[0m")
        print(" - Whoami (cambio MAC, IP, Tor, DNS)")
        print(" - IPGhost (cambio rapido IP tramite Tor)\n")
        print("\033[1m\033[91m[3] REMOTE ACCESS & BACKDOOR (RAT)\033[0m")
        print(" - TheFatRat (genera backdoor per Android/Windows/Linux)\n")
        print("\033[1m\033[93m[4] PASSWORD ATTACKS & WORDLIST\033[0m")
        print(" - CUPP (crea wordlist personalizzate su informazioni vittima)\n")
        print("\033[1m\033[92m[5] DEVICE TRACKING & OSINT\033[0m")
        print(" - Seeker (localizzazione GPS precisa tramite link)\n")
        print("\033[1m\033[94m[6] WI-FI CRACKING\033[0m")
        print(" - AngryOxide (tool avanzato per attacchi 802.11)")
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

# Sottomenu
def menu_phishing():
    while True:
        os.system("clear")
        print_banner()
        print("\033[95m╔════════════════════════════════════╗\033[0m")
        print("\033[95m║ PHISHING & SOCIAL ENGINEERING      ║\033[0m")
        print("\033[95m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Zphisher")
        print("\033[92m[2]\033[0m CamPhish")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/htr-tech/zphisher.git", "zphisher")
        elif sub == "2":
            clone_and_setup("https://github.com/techchipnet/CamPhish.git", "CamPhish")
        elif sub == "0":
            return
        else:
            print("\033[91mScelta non valida!\033[0m")
            sleep(1)

def menu_anonymity():
    while True:
        os.system("clear")
        print_banner()
        print("\033[96m╔════════════════════════════╗\033[0m")
        print("\033[96m║ ANONYMITY & PRIVACY        ║\033[0m")
        print("\033[96m╚════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Whoami")
        print("\033[92m[2]\033[0m IPGhost")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/owerdogan/whoami-project.git", "whoami-project", "", "sudo apt update && sudo apt install -y tar tor curl python3 python3-scapy network-manager && sudo make install")
        elif sub == "2":
            clone_and_setup("https://github.com/s-r-e-e-r-a-j/IPGhost.git", "IPGhost", "", "sudo bash install.sh")
        elif sub == "0":
            return
        else:
            print("\033[91mScelta non valida!\033[0m")
            sleep(1)

def menu_rat():
    while True:
        os.system("clear")
        print_banner()
        print("\033[91m╔════════════════════════════════════╗\033[0m")
        print("\033[91m║ REMOTE ACCESS & BACKDOOR (RAT)    ║\033[0m")
        print("\033[91m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m TheFatRat")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/screetsec/TheFatRat.git", "TheFatRat", "", "chmod +x setup.sh")
        elif sub == "0":
            return
        else:
            print("\033[91mScelta non valida!\033[0m")
            sleep(1)

def menu_password():
    while True:
        os.system("clear")
        print_banner()
        print("\033[93m╔════════════════════════════════════╗\033[0m")
        print("\033[93m║ PASSWORD ATTACKS & WORDLIST       ║\033[0m")
        print("\033[93m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m CUPP")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/Mebus/cupp.git", "cupp")
        elif sub == "0":
            return
        else:
            print("\033[91mScelta non valida!\033[0m")
            sleep(1)

def menu_tracking():
    while True:
        os.system("clear")
        print_banner()
        print("\033[92m╔════════════════════════════════════╗\033[0m")
        print("\033[92m║ DEVICE TRACKING & OSINT           ║\033[0m")
        print("\033[92m╚════════════════════════════════════╝\033[0m\n")
        print("\033[92m[1]\033[0m Seeker")
        print("\033[91m[0]\033[0m Torna al menu principale\n")
        sub = input("\033[94mSeleziona tool: \033[0m")
        if sub == "1":
            clone_and_setup("https://github.com/thewhiteh4t/seeker.git", "seeker", "", "chmod +x install.sh && ./install.sh")
        elif sub == "0":
            return
        else:
            print("\033[91mScelta non valida!\033[0m")
            sleep(1)

def menu_wifi_cracking():
    while True:
        os.system("clear")
        print_banner()
        print("\033[94m╔══════════════════════════╗\033[0m")
        print("\033[94m║ WI-FI CRACKING            ║\033[0m")
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
        print("\033[91m[!] Esegui come root: sudo python3 blood1310-tool.py\033[0m")
        sleep(3)
        sys.exit()
    main_menu()