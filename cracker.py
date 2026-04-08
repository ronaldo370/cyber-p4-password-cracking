import hashlib
import os

# Paths and configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASHES_FILE = os.path.join(BASE_DIR, "lab", "hashes.txt")
WORDLIST_FILE = os.path.join(BASE_DIR, "lab", "wordlist.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "lab", "cracked.txt")

def load_hashes(filepath):
    """Load hashes from file, stripping comments and whitespace."""
    target_hashes = set()
    if not os.path.exists(filepath):
        print(f"[!] Error: {filepath} not found.")
        return target_hashes
    
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                target_hashes.add(line.lower())
    return target_hashes

def crack_hashes():
    targets = load_hashes(HASHES_FILE)
    if not targets:
        print("[!] No target hashes found. Exiting.")
        return

    print(f"[*] Loaded {len(targets)} target hashes.")
    print(f"[*] Starting dictionary attack using: {WORDLIST_FILE}")
    print("-" * 50)

    results = {}
    
    if not os.path.exists(WORDLIST_FILE):
        print(f"[!] Error: Wordlist {WORDLIST_FILE} not found.")
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
                    print(f"[+] CRACKED (MD5): {md5_hash} --> {password}")
                    targets.remove(md5_hash)

                # Check SHA1
                sha1_hash = hashlib.sha1(password.encode()).hexdigest()
                if sha1_hash in targets:
                    results[sha1_hash] = (password, "SHA1")
                    print(f"[+] CRACKED (SHA1): {sha1_hash} --> {password}")
                    targets.remove(sha1_hash)
                    
                if not targets:
                    break
                    
    except Exception as e:
        print(f"[!] Error reading wordlist: {e}")

    # Output results to file
    with open(OUTPUT_FILE, "w") as f:
        f.write("--- Password Cracking Results ---\n")
        f.write(f"Timestamp: {os.path.getmtime(OUTPUT_FILE) if os.path.exists(OUTPUT_FILE) else 'Now'}\n\n")
        for h, (p, alg) in results.items():
            f.write(f"[{alg}] {h} : {p}\n")
            
    print("-" * 50)
    print(f"[*] Attack complete. {len(results)} hashes cracked.")
    print(f"[*] Results saved to {OUTPUT_FILE}")
    if targets:
        print(f"[!] {len(targets)} hashes were NOT cracked.")

if __name__ == "__main__":
    crack_hashes()
