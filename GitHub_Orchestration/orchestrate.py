#!/usr/bin/env python3
import os
import subprocess
import shutil
import json

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DOWNLOADS_DIR = os.path.join(os.path.dirname(BASE_DIR), "downloads")

REPOS = [
    # --- HASKINJ (PERSONAL) ---
    {"name": "you-are-here", "account": "haskinj", "local_path": "haskinj_personal/you-are-here", "mirror": True, "files": ["you_are_here.pdf", "you_are_here_simple.pdf", "you_are_here_jr.pdf"], "banner": "you_are_here_banner"},
    {"name": "DodecaGone-Systems", "account": "haskinj", "local_path": "haskinj_personal/DodecaGone-Systems", "mirror": False, "files": [], "banner": "dodecagone_hub_banner"},
    {"name": "haskinj", "account": "haskinj", "local_path": "haskinj_personal/profile", "mirror": False, "files": [], "banner": "dodecagone_hub_banner"},
    {"name": "cr-imrad", "account": "haskinj", "local_path": "haskinj_personal/cr-imrad", "mirror": True, "files": ["cr_imrad.pdf", "cr_imrad.json"], "banner": "cr_imrad_banner"},
    {"name": "forge-math", "account": "haskinj", "local_path": "haskinj_personal/forge-math", "mirror": True, "files": ["FORGE_MATH_UNIVERSAL.pdf"], "banner": "forge_math_banner"},
    {"name": "i-need-maintenance", "account": "haskinj", "local_path": "haskinj_personal/i-need-maintenance", "mirror": False, "files": [], "banner": "i_need_maintenance_banner"},
    {"name": "void", "account": "haskinj", "local_path": "haskinj_personal/void", "mirror": True, "files": ["void_of_potential.pdf"], "banner": "void_of_potential_banner"},
    {"name": "wonkys", "account": "haskinj", "local_path": "haskinj_personal/wonkys", "mirror": False, "files": ["kairosfilesifter.py", "progresspanic2.py", "smoosher2.py", "wonkypad.py"], "banner": "wonkys_banner"},
    {"name": "dodecagone-website", "account": "haskinj", "local_path": "haskinj_personal/dodecagone-website", "mirror": False, "files": [], "banner": None, "private": True},

    # --- DODECA GONESYSTEMS (ORG) ---
    {"name": "You-Are-Here", "account": "DodecaGoneSystems", "local_path": "DodecaGoneSystems_Org/You-Are-Here", "mirror": False, "files": ["you_are_here.pdf", "you_are_here_simple.pdf", "you_are_here_jr.pdf"], "banner": "you_are_here_banner"},
    {"name": "SeesawTheory", "account": "DodecaGoneSystems", "local_path": "DodecaGoneSystems_Org/SeesawTheory", "mirror": False, "files": ["seesaw.pdf"], "banner": "seesaw_theory_banner"},
    {"name": "CR-IMRAD", "account": "DodecaGoneSystems", "local_path": "DodecaGoneSystems_Org/CR-IMRAD", "mirror": False, "files": ["cr_imrad.pdf", "cr_imrad.json"], "banner": "cr_imrad_banner"},
    {"name": "Void", "account": "DodecaGoneSystems", "local_path": "DodecaGoneSystems_Org/Void", "mirror": False, "files": ["void_of_potential.pdf"], "banner": "void_of_potential_banner"},
    {"name": "ForensicAbsolution", "account": "DodecaGoneSystems", "local_path": "DodecaGoneSystems_Org/ForensicAbsolution", "mirror": False, "files": ["FORENSIC_ABSOLUTION_v1_5.pdf"], "banner": "forensic_absolution_banner"},
    {"name": "ForgeMath", "account": "DodecaGoneSystems", "local_path": "DodecaGoneSystems_Org/ForgeMath", "mirror": False, "files": ["FORGE_MATH_UNIVERSAL.pdf"], "banner": "forge_math_banner"},
]

def run(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}\n{e.stderr}")
        return None

def orchestrate():
    print("🚀 DodecaGone Hub Orchestration Started...")
    
    for repo in REPOS:
        name = repo["name"]
        account = repo["account"]
        local_rel = repo["local_path"]
        local_abs = os.path.join(BASE_DIR, local_rel)
        
        print(f"\n--- Checking Repo: {account}/{name} ---")
        
        if not os.path.exists(local_abs):
            os.makedirs(local_abs)
            print(f"Created directory {local_abs}")
        
        # 1. Sync Assets (Banner)
        if repo.get("banner"):
            # Find the actual filename in assets (it has a timestamp)
            banner_prefix = repo["banner"]
            found_banner = None
            for f in os.listdir(ASSETS_DIR):
                if f.startswith(banner_prefix) and f.endswith(".png"):
                    found_banner = f
                    break
            
            if found_banner:
                dest_banner = os.path.join(local_abs, "repo_banner.png")
                shutil.copy2(os.path.join(ASSETS_DIR, found_banner), dest_banner)
                print(f"Synced banner: {found_banner}")

        # 2. Sync PDFs/Files
        for f_name in repo.get("files", []):
            src = os.path.join(DOWNLOADS_DIR, f_name)
            if os.path.exists(src):
                # For Wonkys, put tools in scripts/
                dest_sub = ""
                if name == "wonkys" and f_name in ["kairosfilesifter.py"]:
                    dest_sub = "tools"
                elif name == "wonkys":
                    dest_sub = "experimental"
                
                dest_dir = os.path.join(local_abs, dest_sub)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.copy2(src, os.path.join(dest_dir, f_name))
                print(f"Synced file: {f_name}")
            else:
                print(f"Warning: File {f_name} not found in downloads.")

        # 3. Git Operations
        print(f"Staging Git for {name}...")
        run("git init -b main", cwd=local_abs)
        
        remote_url = f"https://github.com/{account}/{name}.git"
        # We don't remove origin if it exists to avoid errors on first run, 
        # but the script currently does it. We'll keep it as is for consistency.
        run("git remote remove origin", cwd=local_abs)
        run(f"git remote add origin {remote_url}", cwd=local_abs)
        
        run("git add .", cwd=local_abs)
        
        # Check if there are changes before committing
        status = run("git status --porcelain", cwd=local_abs)
        if status and status.strip():
            run('git commit -m "Standardize professional DodecaGone metadata and hub citations (Professional Polish)"', cwd=local_abs)
            print(f"Committed changes for {name}")
        else:
            print(f"No changes to commit for {name}")
        
        print(f"Push to {remote_url} is READY (Dry Run: git push -u origin main --force)")

    print("\n🏁 Orchestration configuration complete. Read READMEs carefully before final push.")

if __name__ == "__main__":
    orchestrate()
