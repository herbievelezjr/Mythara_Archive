# Start Mythara API Server
Write-Host ' Starting Mythara Engine API...' -ForegroundColor Cyan
Write-Host ''
Write-Host 'The API will be available at: http://localhost:8000' -ForegroundColor Yellow
Write-Host 'Health check: http://localhost:8000/health' -ForegroundColor Yellow
Write-Host 'API Docs: http://localhost:8000/api/docs' -ForegroundColor Yellow
Write-Host ''
Write-Host 'Press CTRL+C to stop the server' -ForegroundColor Green
Write-Host ''

cd 'C:\Users\Mythara\Desktop\Clone Repo Mythara\Mythara_Archive'
python core/source_proprietary/main.py
