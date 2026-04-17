import hashlib
import os
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# Paths and configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASHES_FILE = os.path.join(BASE_DIR, "lab", "hashes.txt")
WORDLIST_FILE = os.path.join(BASE_DIR, "lab", "wordlist.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "lab", "cracked.txt")

def print_header(title):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(60)}")
    print(f"{Fore.CYAN}{'='*60}")

def load_hashes(filepath):
    """Load hashes from file, stripping comments and whitespace."""
    target_hashes = set()
    if not os.path.exists(filepath):
        print(f"{Fore.RED}[!] Error: {filepath} not found.")
        return target_hashes
    
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                target_hashes.add(line.lower())
    return target_hashes

def crack_hashes():
    print_header("PROJECT 4: DICTIONARY ATTACK SIMULATION")
    
    targets = load_hashes(HASHES_FILE)
    if not targets:
        print(f"{Fore.RED}[!] No target hashes found. Exiting.")
        return

    print(f"{Fore.YELLOW}[*] Target Hashes Loaded: {Fore.WHITE}{len(targets)}")
    print(f"{Fore.YELLOW}[*] Wordlist:            {Fore.BLUE}{os.path.basename(WORDLIST_FILE)}")
    print(f"{Fore.CYAN}{'-' * 60}")

    results = {}
    
    if not os.path.exists(WORDLIST_FILE):
        print(f"{Fore.RED}[!] Error: Wordlist not found.")
        return

    try:
        with open(WORDLIST_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for password in f:
                password = password.strip()
                if not password:
                    continue
                
                # Check MD5
                md5_hash = hashlib.md5(password.encode()).hexdigest()
                if md5_hash in targets:
                    results[md5_hash] = (password, "MD5")
                    print(f"{Fore.GREEN}[+] {Fore.WHITE}CRACKED ({Fore.MAGENTA}MD5{Fore.WHITE}): {Fore.CYAN}{md5_hash} {Fore.WHITE}--> {Fore.GREEN}{password}")
                    targets.remove(md5_hash)

                # Check SHA1
                sha1_hash = hashlib.sha1(password.encode()).hexdigest()
                if sha1_hash in targets:
                    results[sha1_hash] = (password, "SHA1")
                    print(f"{Fore.GREEN}[+] {Fore.WHITE}CRACKED ({Fore.MAGENTA}SHA1{Fore.WHITE}): {Fore.CYAN}{sha1_hash} {Fore.WHITE}--> {Fore.GREEN}{password}")
                    targets.remove(sha1_hash)
                    
                if not targets:
                    break
                    
    except Exception as e:
        print(f"{Fore.RED}[!] Error reading wordlist: {e}")

    # Output results to file
    with open(OUTPUT_FILE, "w") as f:
        f.write("--- Password Cracking Results ---\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S') if 'time' in globals() else 'Now'}\n\n")
        for h, (p, alg) in results.items():
            f.write(f"[{alg}] {h} : {p}\n")
            
    print(f"{Fore.CYAN}{'-' * 60}")
    print(f"{Fore.YELLOW}[*] Attack complete. {Fore.GREEN}{len(results)} {Fore.YELLOW}hashes cracked.")
    print(f"{Fore.WHITE}Results saved to: {Fore.BLUE}{os.path.basename(OUTPUT_FILE)}")
    
    if targets:
        print(f"{Fore.RED}[!] {len(targets)} hashes were NOT cracked.")

if __name__ == "__main__":
    import time
    crack_hashes()
