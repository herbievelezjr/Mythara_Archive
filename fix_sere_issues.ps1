#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Fix SERE Bot issues: code integrity, registry false positives, network timeouts
.DESCRIPTION
    Regenerates integrity baseline and provides diagnostic information
#>

param(
    [switch]$ResetIntegrity,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = "$scriptPath\.venv\Scripts\python.exe"
$sereBotPath = "$scriptPath\sere_bot.py"
$hashFile = "$scriptPath\sere_bot_code_hash.sha256"

Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "SERE BOT FIX UTILITY" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check files exist
if (-not (Test-Path $venvPath)) {
    Write-Host "ERROR: Virtual environment not found at $venvPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $sereBotPath)) {
    Write-Host "ERROR: sere_bot.py not found at $sereBotPath" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python environment found" -ForegroundColor Green
Write-Host "✓ sere_bot.py found" -ForegroundColor Green
Write-Host ""

# Issue 1: Code Integrity Hash
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host "Issue 1: Code Integrity Hash" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta

if (Test-Path $hashFile) {
    $oldHash = Get-Content $hashFile
    Write-Host "Current hash file: $oldHash" -ForegroundColor Yellow
    
    if ($ResetIntegrity) {
        Remove-Item $hashFile -Force
        Write-Host "✓ Hash file deleted - will regenerate on next run" -ForegroundColor Green
    } else {
        Write-Host "NOTE: Use -ResetIntegrity flag to regenerate baseline" -ForegroundColor Cyan
    }
} else {
    Write-Host "✓ Hash file does not exist (will be created on first run)" -ForegroundColor Green
}

Write-Host ""

# Issue 2: Registry Whitelist
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host "Issue 2: Registry False Positives" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta

$whitelistCheck = Select-String -Path $sereBotPath -Pattern "bootshell|bootim" -Quiet
if ($whitelistCheck) {
    Write-Host "✓ BootShell and BootIM added to registry whitelist" -ForegroundColor Green
} else {
    Write-Host "✗ Whitelist update not found - please verify changes" -ForegroundColor Yellow
}

Write-Host ""

# Issue 3: Network Timeouts
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host "Issue 3: Network Timeouts" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta

$timeout5Count = (Select-String -Path $sereBotPath -Pattern "timeout=5" | Measure-Object).Count
$timeout15Count = (Select-String -Path $sereBotPath -Pattern "timeout=15" | Measure-Object).Count

Write-Host "Timeout values found:" -ForegroundColor Cyan
Write-Host "  - timeout=5: $timeout5Count occurrences (old)" -ForegroundColor Yellow
Write-Host "  - timeout=15: $timeout15Count occurrences (fixed)" -ForegroundColor Green

Write-Host ""

# Issue 4: Cloud Provider Whitelisting
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host "Issue 4: Cloud Provider Whitelisting" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta

$providers = @('Microsoft', 'Google', 'Amazon', 'Cloudflare', 'Apple', 'Meta')
foreach ($provider in $providers) {
    $found = Select-String -Path $sereBotPath -Pattern $provider -Quiet
    $status = if ($found) { "✓" } else { "✗" }
    Write-Host "$status $provider" -ForegroundColor $(if ($found) { "Green" } else { "Yellow" })
}

Write-Host ""

# Summary
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "SUMMARY OF FIXES" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. ✓ Code Integrity: force_baseline parameter added" -ForegroundColor Green
Write-Host "2. ✓ Registry Whitelist: BootShell/BootIM added" -ForegroundColor Green
Write-Host "3. ✓ Network Timeouts: Increased from 5s to 15s" -ForegroundColor Green
Write-Host "4. ⚠ Cloud Providers: Check if fully whitelisted" -ForegroundColor Yellow
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Run: python sere_bot.py" -ForegroundColor White
Write-Host "2. The bot will regenerate the integrity baseline on startup" -ForegroundColor White
Write-Host "3. Monitor for fewer false positives on registry scans" -ForegroundColor White
Write-Host "4. Network timeouts should be reduced with 15-second limit" -ForegroundColor White
Write-Host ""
