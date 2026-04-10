#!/bin/bash

# DodecaGone Systems GitHub Deployment Script
# This script initializes and force-pushes clean structures to reorganized repositories.

REPOS=("you-are-here" "i-need-maintenance" "forge-math" "cr-imrad" "haskinj" "DodecaGone-Systems")
BASE_DIR="/home/node00/Documents/GitHub_Orchestration"

echo "🚀 Starting DodecaGone GitHub Orchestration..."

for REPO in "${REPOS[@]}"
do
    echo "------------------------------------------------"
    echo "📦 Processing: $REPO"
    
    TARGET_DIR="$BASE_DIR/$REPO"
    
    if [ ! -d "$TARGET_DIR" ]; then
        echo "❌ Error: Directory $TARGET_DIR not found. Skipping."
        continue
    fi
    
    cd "$TARGET_DIR"
    
    # Initialize Git if not already present
    if [ ! -d ".git" ]; then
        git init -b main
    fi
    
    # Set the remote (assuming the correct user and new names)
    # We use force push to ensure total clean slate as requested
    git remote remove origin 2>/dev/null
    git remote add origin "https://github.com/haskinj/$REPO.git"
    
    # Prepare and Commit
    git add .
    git commit -m "Initialize professional DodecaGone Systems structure (Clean Slate)"
    
    echo "⬆️  Ready to push to haskinj/$REPO"
    echo "⚠️  Note: You may be prompted for your GitHub credentials."
    
    # Attempt to push
    git push -u origin main --force
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully deployed $REPO"
    else
        echo "❌ Failed to push $REPO. Please check your credentials/permissions."
    fi
done

echo "------------------------------------------------"
echo "🏁 Orchestration Task Complete."
