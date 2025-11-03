# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

# Mythara Archives - Manual Upload Instructions
# Use this if Git installation is problematic

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "MYTHARA ARCHIVES - MANUAL GITHUB UPLOAD" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan

Write-Host "`nSince Git installation is taking time, here's the manual method:" -ForegroundColor White

Write-Host "`n[OPTION 1] Use GitHub Desktop (Easiest):" -ForegroundColor Green
Write-Host "1. Download GitHub Desktop: https://desktop.github.com/" -ForegroundColor White
Write-Host "2. Install and sign in with your GitHub account" -ForegroundColor White
Write-Host "3. File > Add Local Repository" -ForegroundColor White
Write-Host "4. Select: C:\Users\HVele\OneDrive\Desktop\Mythara_Archive" -ForegroundColor White
Write-Host "5. Click 'Publish repository'" -ForegroundColor White
Write-Host "6. Make sure 'Keep this code private' is checked" -ForegroundColor White
Write-Host "7. Click 'Publish'" -ForegroundColor White

Write-Host "`n[OPTION 2] Use VS Code Built-in Git:" -ForegroundColor Green
Write-Host "1. Open VS Code in this folder" -ForegroundColor White
Write-Host "2. Click Source Control icon (left sidebar)" -ForegroundColor White
Write-Host "3. Click 'Initialize Repository'" -ForegroundColor White
Write-Host "4. Stage all files (+ icon)" -ForegroundColor White
Write-Host "5. Enter commit message: 'Initial commit'" -ForegroundColor White
Write-Host "6. Click checkmark to commit" -ForegroundColor White
Write-Host "7. Click '...' > Remote > Add Remote" -ForegroundColor White
Write-Host "8. Enter: https://github.com/herbievelezjr/Mythara_Archives.git" -ForegroundColor White
Write-Host "9. Click '...' > Push" -ForegroundColor White

Write-Host "`n[OPTION 3] Wait for Git to Install:" -ForegroundColor Green
Write-Host "1. Wait a few more minutes for Git installation to complete" -ForegroundColor White
Write-Host "2. Close and reopen PowerShell" -ForegroundColor White
Write-Host "3. Run: .\push_to_github.ps1" -ForegroundColor White

Write-Host "`n" + "=" * 80 -ForegroundColor Cyan
Write-Host "Choose whichever option works best for you!" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan
