#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick test of SERE Bot fixes
#>

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$sereBotPath = "$scriptPath\sere_bot.py"

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "SERE BOT FIX VALIDATION" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$tests = @{
    "Force Baseline Support" = "force_baseline"
    "BootShell Whitelisted" = "bootshell"
    "BootIM Whitelisted" = "bootim"
    "HyperV Support" = "hyper-v"
}

$passed = 0
$failed = 0

foreach ($testName in $tests.Keys) {
    $pattern = $tests[$testName]
    $found = Select-String -Path $sereBotPath -Pattern $pattern -Quiet
    
    if ($found) {
        Write-Host "✓ $testName" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "✗ $testName" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "────────────────────────────────────────────────────────────" -ForegroundColor Magenta

$timeout5Count = (Select-String -Path $sereBotPath -Pattern "timeout=5" | Measure-Object).Count
$timeout15Count = (Select-String -Path $sereBotPath -Pattern "timeout=15" | Measure-Object).Count

if ($timeout5Count -eq 0) {
    Write-Host "✓ All timeouts updated (timeout=15: $timeout15Count)" -ForegroundColor Green
    $passed++
} else {
    Write-Host "✗ Timeout=5 still present: $timeout5Count" -ForegroundColor Red
    $failed++
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "RESULTS: $passed passed, $failed failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($failed -eq 0) {
    Write-Host "✅ All fixes verified! Ready to run sere_bot.py" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some issues detected" -ForegroundColor Yellow
}

Write-Host ""
