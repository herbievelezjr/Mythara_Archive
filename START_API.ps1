# Mythara Engine - Startup Script
Write-Host " Starting Mythara Engine API Server..." -ForegroundColor Cyan
Write-Host ""
Set-Location "C:\Users\Mythara\Desktop\Clone Repo Mythara\Mythara_Archive\core\source_proprietary"
Write-Host " Starting server on http://localhost:8000" -ForegroundColor Yellow
Write-Host " API Docs: http://localhost:8000/api/docs" -ForegroundColor Yellow
Write-Host " Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""
& "C:/Users/Mythara/AppData/Local/Programs/Python/Python311/python.exe" main.py
