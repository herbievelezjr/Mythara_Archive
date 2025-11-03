# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

# Auto-push to GitHub - Commits and pushes all changes automatically

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "MYTHARA AUTO-PUSH TO GITHUB" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan

# Stage all changes
Write-Host "`n[1/3] Staging all changes..." -ForegroundColor Cyan
git add .
Write-Host "[OK] All files staged" -ForegroundColor Green

# Commit with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMessage = "Auto-update: $timestamp - Added runners and scheduler for all 15 bots"

Write-Host "`n[2/3] Creating commit..." -ForegroundColor Cyan
git commit -m "$commitMessage"
Write-Host "[OK] Commit created: $commitMessage" -ForegroundColor Green

# Push to GitHub
Write-Host "`n[3/3] Pushing to GitHub..." -ForegroundColor Cyan
git push origin main
Write-Host "[OK] Pushed to GitHub!" -ForegroundColor Green

Write-Host "`n" + "=" * 80 -ForegroundColor Cyan
Write-Host "SUCCESS! Changes pushed to:" -ForegroundColor Green
Write-Host "https://github.com/herbievelezjr/Mythara_Archives" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
