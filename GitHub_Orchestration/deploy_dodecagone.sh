#!/bin/bash

# DodecaGone Systems GitHub Deployment Script
# This script force-pushes the current local state to GitHub for all repositories.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# List of all repos (matching orchestrate.py)
REPOS=(
    "haskinj_personal/you-are-here"
    "haskinj_personal/DodecaGone-Systems"
    "haskinj_personal/profile"
    "haskinj_personal/cr-imrad"
    "haskinj_personal/forge-math"
    "haskinj_personal/i-need-maintenance"
    "haskinj_personal/void"
    "haskinj_personal/wonkys"
    "haskinj_personal/dodecagone-website"
    "DodecaGoneSystems_Org/You-Are-Here"
    "DodecaGoneSystems_Org/SeesawTheory"
    "DodecaGoneSystems_Org/CR-IMRAD"
    "DodecaGoneSystems_Org/Void"
    "DodecaGoneSystems_Org/ForensicAbsolution"
    "DodecaGoneSystems_Org/ForgeMath"
)

echo "🚀 Starting DodecaGone GitHub Deployment..."

for REPO_PATH in "${REPOS[@]}"
do
    echo "------------------------------------------------"
    echo "📦 Processing: $REPO_PATH"
    
    TARGET_DIR="$SCRIPT_DIR/$REPO_PATH"
    
    if [ ! -d "$TARGET_DIR" ]; then
        echo "❌ Error: Directory $TARGET_DIR not found. Skipping."
        continue
    fi
    
    cd "$TARGET_DIR"
    
    if [ ! -d ".git" ]; then
        echo "❌ Error: $REPO_PATH is not a git repository. Run orchestrate.py first."
        continue
    fi
    
    echo "⬆️  Pushing to GitHub..."
    echo "⚠️  Note: You may be prompted for your GitHub credentials for each repository."
    
    # Force push to ensure the clean slate is applied
    git push -u origin main --force
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully deployed $REPO_PATH"
    else
        echo "❌ Failed to push $REPO_PATH. Please check your credentials/permissions."
        echo "   If you have many repos, consider using a Git Personal Access Token (PAT) with cache."
    fi
done

echo "------------------------------------------------"
echo "🏁 Deployment Task Complete."
