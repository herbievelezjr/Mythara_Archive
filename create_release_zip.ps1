# Mythara Engine — Automatic Release Package Builder
# This script creates a distribution-ready ZIP file for GitHub releases
# Version: 1.0.0
# Date: November 2, 2025

param(
    [string]$Version = "1.0.0",
    [switch]$IncludeTests = $true
)

# Set variables
$releaseDir = "mythara-engine-v$Version"
$zipName = "mythara-engine-v$Version.zip"

Write-Host "Building Mythara Engine Release Package v$Version" -ForegroundColor Cyan
Write-Host ""

# Create staging directory
Write-Host "Creating staging directory: $releaseDir"
if (Test-Path $releaseDir) {
    Remove-Item -Path $releaseDir -Recurse -Force
}
New-Item -ItemType Directory -Path $releaseDir -Force | Out-Null

# Copy documentation files
Write-Host "Copying documentation..."
$docs = @("README.md", "LICENSE.md", "COPYRIGHT.md", "INSTALL.md")
foreach ($doc in $docs) {
    $sourcePath = "GitHub_Release_Package\$doc"
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination "$releaseDir\" -Force
        Write-Host "  + $doc"
    }
}

# Copy core directories
Write-Host "Copying core components..."
$coreDirs = @("core", "docs", "Commercial", "Legal", "manifest", "validate_suite")
foreach ($dir in $coreDirs) {
    if (Test-Path $dir) {
        Copy-Item -Path $dir -Destination "$releaseDir\$dir" -Recurse -Force
        Write-Host "  + $dir"
    }
}

# Include tests and evidence
if ($IncludeTests) {
    Write-Host "Including test suite and evidence..."
    $testDirs = @("tests", "Evidence")
    foreach ($dir in $testDirs) {
        if (Test-Path $dir) {
            Copy-Item -Path $dir -Destination "$releaseDir\$dir" -Recurse -Force
            Write-Host "  + $dir"
        }
    }
}

# Copy verification files
Write-Host "Copying verification artifacts..."
$verifyFiles = @(
    "forensic_manifest.json",
    "forensic_manifest.json.asc",
    "forensic_public_key.asc"
)
foreach ($file in $verifyFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination "$releaseDir\" -Force
        Write-Host "  + $file"
    }
}

# Create ZIP archive
Write-Host ""
Write-Host "Creating ZIP archive..."
if (Test-Path $zipName) {
    Remove-Item -Path $zipName -Force
}
Compress-Archive -Path $releaseDir -DestinationPath $zipName -CompressionLevel Optimal -Force

# Calculate ZIP hash
Write-Host ""
Write-Host "Calculating package hash..."
$hash = (Get-FileHash -Algorithm SHA256 $zipName).Hash.ToLower()

# Cleanup staging directory
Write-Host "Cleaning up..."
Remove-Item -Path $releaseDir -Recurse -Force

# Display results
Write-Host ""
Write-Host "SUCCESS: Release package created!" -ForegroundColor Green
Write-Host ""
Write-Host "Package Details:" -ForegroundColor Cyan
Write-Host "  File: $zipName"
Write-Host "  Size: $([math]::Round((Get-Item $zipName).Length / 1MB, 2)) MB"
Write-Host "  SHA256: $hash"
Write-Host ""

# Save hash to file
$hashFile = "$zipName.sha256"
Set-Content -Path $hashFile -Value "$hash  $zipName"
Write-Host "Hash saved to: $hashFile" -ForegroundColor Green
