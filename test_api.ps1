# Test Mythara API
Write-Host ' Testing Mythara API...' -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing -TimeoutSec 5
    Write-Host ' API is responding!' -ForegroundColor Green
    Write-Host 'Status Code:' $response.StatusCode
    Write-Host 'Response:' $response.Content
} catch {
    Write-Host ' API is not responding' -ForegroundColor Red
    Write-Host 'Error:' $_.Exception.Message
}
