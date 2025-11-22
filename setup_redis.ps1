# Setup Redis for Mythara Engine
Write-Host "Setting up Redis in Docker..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if mythara-redis already exists
$existing = docker ps -a --filter "name=mythara-redis" --format "{{.Names}}"
if ($existing -eq "mythara-redis") {
    Write-Host "Found existing mythara-redis container..." -ForegroundColor Yellow
    
    # Check if it's running
    $running = docker ps --filter "name=mythara-redis" --format "{{.Names}}"
    if ($running -eq "mythara-redis") {
        Write-Host "✓ Redis is already running on port 6379" -ForegroundColor Green
    } else {
        Write-Host "Starting existing container..." -ForegroundColor Yellow
        docker start mythara-redis
        Start-Sleep -Seconds 2
        Write-Host "✓ Redis started on port 6379" -ForegroundColor Green
    }
} else {
    Write-Host "Creating new Redis container..." -ForegroundColor Yellow
    docker run -d --name mythara-redis -p 6379:6379 redis:latest
    Start-Sleep -Seconds 3
    Write-Host "✓ Redis container created and running on port 6379" -ForegroundColor Green
}

# Test connection
Write-Host "`nTesting Redis connection..." -ForegroundColor Cyan
try {
    python -c "import redis; r = redis.Redis(host='localhost', port=6379, decode_responses=True); r.ping(); print('✓ Redis connection successful!')"
    Write-Host "✓ Python redis client connected successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to connect to Redis" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`nRedis Setup Complete!" -ForegroundColor Green
Write-Host "Redis URL: redis://localhost:6379" -ForegroundColor Cyan
Write-Host "`nUseful commands:" -ForegroundColor Yellow
Write-Host "  Stop Redis:    docker stop mythara-redis"
Write-Host "  Start Redis:   docker start mythara-redis"
Write-Host "  View logs:     docker logs mythara-redis"
Write-Host "  Remove Redis:  docker rm -f mythara-redis"
