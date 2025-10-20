#!/bin/bash
# Upload to GitHub without affecting global git config

echo "================================================"
echo "Upload to GitHub (Preserves GitLab Config)"
echo "================================================"
echo ""

# Get GitHub repo URL from user
read -p "Enter your GitHub repo URL (e.g., https://github.com/user/repo.git): " GITHUB_REPO

if [ -z "$GITHUB_REPO" ]; then
    echo "❌ Error: Repository URL is required"
    exit 1
fi

echo ""
echo "📦 Initializing local git repository..."

# Initialize git only in this directory
git init

# Set local config (won't affect global GitLab config)
git config --local user.name "Your Name"
git config --local user.email "your-email@example.com"

echo ""
echo "📝 Adding files..."
git add .

echo ""
echo "✅ Creating commit..."
git commit -m "Initial commit: Production-ready OpenVPN + Nginx Ansible playbook

- Docker installation role with automatic setup
- Nginx file browser role for serving VPN configs
- OpenVPN server role with automated configuration
- Idempotent and optimized for performance
- Comprehensive documentation (README, QUICKSTART, TESTING)
- Production-tested and validated
- Molecule tests included for all roles"

echo ""
echo "🔗 Adding GitHub remote..."
git remote add origin "$GITHUB_REPO"

echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "================================================"
echo "✅ Done! Your code is now on GitHub!"
echo "================================================"
echo ""
echo "Your global git config is unchanged."
echo "This repository uses local git configuration."
echo ""
echo "Visit your repository at:"
echo "${GITHUB_REPO%.git}"

