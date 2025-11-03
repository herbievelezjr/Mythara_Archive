# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

# Mythara Archive - GitHub Repository Setup Script
# Run this after Git is installed to push your code to GitHub

Write-Host "=" * 80
Write-Host "MYTHARA ARCHIVE - GITHUB REPOSITORY SETUP"
Write-Host "=" * 80

# Check if Git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "[ERROR] Git is not installed yet. Please install Git first:" -ForegroundColor Red
    Write-Host "        1. Run: choco install git -y"
    Write-Host "        2. Close and reopen PowerShell"
    Write-Host "        3. Run this script again"
    exit 1
}

Write-Host "[OK] Git version: $(git --version)" -ForegroundColor Green

# Configure Git (update with your details)
Write-Host "`n[1/7] Configuring Git user..." -ForegroundColor Cyan
git config --global user.name "Herbert Velez Jr"
git config --global user.email "your-email@example.com"  # UPDATE THIS
Write-Host "[OK] Git configured" -ForegroundColor Green

# Initialize repository
Write-Host "`n[2/7] Initializing Git repository..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    git init
    Write-Host "[OK] Repository initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Repository already initialized" -ForegroundColor Yellow
}

# Create .gitignore
Write-Host "`n[3/7] Creating .gitignore..." -ForegroundColor Cyan
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
.venv/
venv/
ENV/
*.egg-info/
dist/
build/

# SQLite databases (sensitive data)
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log

# Temporary files
*.tmp
*.temp
~$*

# Sensitive files
*_private.py
*_secrets.py
*.key
*.pem
*.cert

# CSV exports (may contain customer data)
*_expanded.csv
*_export.csv
"@

$gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8
Write-Host "[OK] .gitignore created" -ForegroundColor Green

# Create README if it doesn't exist
Write-Host "`n[4/7] Creating README.md..." -ForegroundColor Cyan
if (-not (Test-Path "README.md")) {
    $readmeContent = @"
# Mythara Archive

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**  
**Proprietary and Confidential.**

## Overview

Mythara Engine: Symbolic Safety Integrity Protocol (SSIP) orchestration system for enterprise contract verification and compliance automation.

## Features

- **15 Autonomous AI Bots** - Full C-suite automation
- **SSIP Compliance** - Cryptographic integrity verification
- **Grant Acquisition** - \$9.45M+ grant pipeline
- **Zero Operating Cost** - Runs on Windows Task Scheduler

## Bots

1. Finance VP
2. Sales/Marketing VP
3. Customer Success VP
4. DevOps VP
5. Logistics VP
6. Public Affairs VP
7. HR VP
8. Support Chat Bot
9. International Sales VP
10. DevSecOps VP
11. SEO Master Bot
12. Researcher Bot
13. Grant Writer Bot
14. SBGA Integration Bot
15. Accounting VP

## Security

This is a **private, proprietary repository**. Do not share, fork, or distribute.

## License

All rights reserved. No license granted for use, modification, or distribution.
"@

    $readmeContent | Out-File -FilePath "README.md" -Encoding UTF8
    Write-Host "[OK] README.md created" -ForegroundColor Green
} else {
    Write-Host "[OK] README.md already exists" -ForegroundColor Yellow
}

# Add all files
Write-Host "`n[5/7] Staging files for commit..." -ForegroundColor Cyan
git add .
Write-Host "[OK] Files staged" -ForegroundColor Green

# Initial commit
Write-Host "`n[6/7] Creating initial commit..." -ForegroundColor Cyan
$commitExists = git log -1 2>&1
if ($LASTEXITCODE -ne 0) {
    git commit -m "Initial commit: Mythara Archive with 15 autonomous bots"
    Write-Host "[OK] Initial commit created" -ForegroundColor Green
} else {
    Write-Host "[OK] Repository already has commits" -ForegroundColor Yellow
}

# Instructions for GitHub
Write-Host "`n[7/7] GitHub repository setup instructions:" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS TO PUSH TO GITHUB:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: Mythara_Archives" -ForegroundColor White
Write-Host "3. Visibility: PRIVATE (important!)" -ForegroundColor Red
Write-Host "4. Do NOT initialize with README (we already have one)" -ForegroundColor White
Write-Host "5. Click 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "6. Copy the repository URL (should be like: https://github.com/YOUR_USERNAME/Mythara_Archives.git)" -ForegroundColor White
Write-Host ""
Write-Host "7. Then run these commands:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/Mythara_Archives.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 80
Write-Host "REPOSITORY READY FOR GITHUB!" -ForegroundColor Green
Write-Host "=" * 80
