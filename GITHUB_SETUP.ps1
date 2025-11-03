# Mythara Archive - GitHub Setup Guide
# Run these commands step by step

# 1. Install Git (if not installed)
# Download from: https://git-scm.com/download/win
# Or use winget:
winget install --id Git.Git -e --source winget

# 2. Configure Git (first time only)
git config --global user.name "Herbert Velez Jr"
git config --global user.email "your-github-email@example.com"  # Replace with your actual GitHub email

# 3. Initialize repository
cd C:\Users\HVele\OneDrive\Desktop\Mythara_Archive
git init

# 4. Create .gitignore
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.db
*.db-journal

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Secrets
.env
*.key
*.pem
*_secrets.py

# Logs
*.log
"@ | Out-File -FilePath .gitignore -Encoding utf8

# 5. Add files
git add .

# 6. Initial commit
git commit -m "Initial commit - Mythara Archive with 15 autonomous bots"

# 7. Create GitHub repo (go to github.com/new)
# Name: Mythara_Archive
# Private repository (IMPORTANT - this is proprietary!)
# Don't initialize with README (we already have files)

# 8. Connect to GitHub (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/Mythara_Archive.git

# 9. Push to GitHub
git branch -M main
git push -u origin main

# Done! Your code is now backed up on GitHub (private repo)
