#!/usr/bin/env python3
import os
import subprocess
from orchestrate import REPOS

# --- CONFIGURATION ---
BACKUP_BASE_DIR = "/home/node00/Documents/GitHub"
# Map account names to their respective backup directories
ACCOUNT_MAP = {
    "haskinj": "haskinj",
    "DodecaGoneSystems": "DodecaGone Systems"
}

def run(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}\n{e.stderr}")
        return None

def extract_token():
    try:
        # Try to get the token from the current repo's remote
        remote_url = subprocess.check_output("git remote get-url origin", shell=True, text=True).strip()
        if "@" in remote_url and "ghp_" in remote_url:
            return remote_url.split("@")[0].split("//")[-1]
    except:
        pass
    return None

def backup():
    print("📥 Starting GitHub Backup...")
    token = extract_token()
    if token:
        print("🔑 Authentication token detected and will be used for private repositories.")
    
    
    if not os.path.exists(BACKUP_BASE_DIR):
        os.makedirs(BACKUP_BASE_DIR)
        print(f"Created base backup directory: {BACKUP_BASE_DIR}")

    for repo in REPOS:
        account = repo["account"]
        name = repo["name"]
        
        # Determine the target directory for this account
        account_folder = ACCOUNT_MAP.get(account, account)
        account_dir = os.path.join(BACKUP_BASE_DIR, account_folder)
        
        if not os.path.exists(account_dir):
            os.makedirs(account_dir)
            print(f"Created account directory: {account_dir}")
        
        target_dir = os.path.join(account_dir, name)
        
        if token:
            remote_url = f"https://{token}@github.com/{account}/{name}.git"
        else:
            remote_url = f"https://github.com/{account}/{name}.git"

        if not os.path.exists(target_dir):
            print(f"\n🚀 Cloning {account}/{name}...")
            run(f"git clone {remote_url} {name}", cwd=account_dir)
        else:
            print(f"\n🔄 Updating {account}/{name}...")
            # Check if it's a git repo
            if os.path.exists(os.path.join(target_dir, ".git")):
                # Update remote URL to include token if it changed
                run(f"git remote set-url origin {remote_url}", cwd=target_dir)
                run("git pull origin main", cwd=target_dir)
            else:
                print(f"⚠️ {target_dir} exists but is not a git repository. Skipping.")

    print("\n🏁 Backup complete.")

if __name__ == "__main__":
    backup()
