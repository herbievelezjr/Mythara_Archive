# Network Errors Explanation and Resolution

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**
**Proprietary and Confidential.**

---

## Problem Summary

The Mythara Engine API server (`core/source_proprietary/main.py`) is experiencing network-related errors due to **missing Python dependencies**. Specifically, the `httpx` library and related FastAPI dependencies are not installed in the current environment.

---

## Root Cause Analysis

### 1. Missing `httpx` Library

**Location**: `core/source_proprietary/main.py`, line 26

```python
import httpx  # For ElevenLabs API calls
```

**Purpose**: The `httpx` library is used to make asynchronous HTTP requests to external APIs, specifically:
- **ElevenLabs Text-to-Speech API** (line 2044): For generating audio responses
- Other potential external service integrations

**Error When Missing**:
```
ModuleNotFoundError: No module named 'httpx'
```

### 2. Missing FastAPI Dependencies

The API server requires several packages that may not be installed:
- `fastapi` - Core web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `httpx` - HTTP client

These are specified in `core/source_proprietary/requirements-api.txt` but may not have been installed.

---

## Why This Causes "Network Errors"

When the API server tries to start:

1. **Import Phase Failure**: Python attempts to import `httpx` and fails
2. **Server Doesn't Start**: The API server cannot initialize
3. **Connection Refused**: Clients trying to connect get network errors because the server isn't running
4. **External API Calls Fail**: Even if the server starts, calls to external APIs (like ElevenLabs) will fail without `httpx`

**Symptom**: You may see one or more of these errors:
- `ModuleNotFoundError: No module named 'httpx'`
- `ModuleNotFoundError: No module named 'fastapi'`
- Connection refused errors when trying to access the API
- Timeout errors when making API requests
- Import errors in startup logs

---

## Solution: Install All Dependencies

### Step 1: Install Root Dependencies

```bash
cd /home/runner/work/Mythara_Archive/Mythara_Archive
pip install -r requirements.txt
```

This installs core utilities and testing frameworks.

### Step 2: Install API-Specific Dependencies

```bash
pip install -r core/source_proprietary/requirements-api.txt
```

This installs:
- ✅ `httpx==0.25.2` - HTTP client for external API calls
- ✅ `fastapi==0.104.1` - Web framework
- ✅ `uvicorn==0.24.0` - ASGI server
- ✅ `pydantic==2.5.0` - Data validation
- ✅ All other API dependencies (SendGrid, SQLAlchemy, etc.)

### Step 3: Verify Installation

```bash
python3 -c "import httpx; print(f'✅ httpx version: {httpx.__version__}')"
python3 -c "import fastapi; print(f'✅ FastAPI version: {fastapi.__version__}')"
python3 -c "import uvicorn; print(f'✅ Uvicorn version: {uvicorn.__version__}')"
```

**Expected Output**:
```
✅ httpx version: 0.25.2
✅ FastAPI version: 0.104.1
✅ Uvicorn version: 0.24.0
```

### Step 4: Start the API Server

```bash
# Method 1: Using the main.py script
python core/source_proprietary/main.py

# Method 2: Using uvicorn directly
uvicorn core.source_proprietary.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output** (server starts successfully):
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Common Network Issues and Fixes

### Issue 1: "Connection Refused" Errors

**Symptoms**:
- Cannot connect to `http://localhost:8000`
- `curl` commands timeout or fail
- Browser shows "Unable to connect"

**Cause**: API server is not running

**Fix**:
1. Check if server is running: `ps aux | grep "uvicorn\|main.py"`
2. Check for error logs in terminal where you started the server
3. Verify all dependencies are installed (see Step 3 above)
4. Restart the server

### Issue 2: "ModuleNotFoundError" on Startup

**Symptoms**:
```
ModuleNotFoundError: No module named 'httpx'
ModuleNotFoundError: No module named 'fastapi'
```

**Cause**: Dependencies not installed

**Fix**:
```bash
pip install -r core/source_proprietary/requirements-api.txt
```

### Issue 3: External API Calls Fail

**Symptoms**:
- ElevenLabs text-to-speech requests fail
- Timeout errors when calling external services
- "Connection timeout" errors

**Cause**: 
- `httpx` not installed, OR
- Network connectivity issues, OR
- API keys not configured

**Fix**:
1. Install `httpx`: `pip install httpx==0.25.2`
2. Check network connectivity: `curl https://api.elevenlabs.io`
3. Verify API keys in environment variables or `.env` file
4. Check firewall settings

### Issue 4: Timeout Errors

**Location in code**: `core/source_proprietary/main.py`, line 2044

```python
async with httpx.AsyncClient(timeout=30.0) as client:
```

**Cause**: External API calls taking longer than 30 seconds

**Fix**:
- Check network connectivity
- Verify external service (ElevenLabs) is operational
- Increase timeout if needed (edit line 2044)
- Check for rate limiting or API quota issues

---

## Dependency Installation Best Practices

### Complete Installation Command

```bash
# Install all dependencies in one go
cd /home/runner/work/Mythara_Archive/Mythara_Archive
pip install -r requirements.txt
pip install -r core/source_proprietary/requirements-api.txt
```

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r core/source_proprietary/requirements-api.txt
```

### Verify Complete Installation

```bash
# Check all critical packages
python3 << 'EOF'
import sys
packages = {
    'httpx': 'HTTP client for external APIs',
    'fastapi': 'Web framework',
    'uvicorn': 'ASGI server',
    'pydantic': 'Data validation',
    'sqlalchemy': 'Database ORM',
    'sendgrid': 'Email service',
    'numpy': 'Scientific computing',
}

missing = []
for pkg, desc in packages.items():
    try:
        mod = __import__(pkg)
        version = getattr(mod, '__version__', 'unknown')
        print(f'✅ {pkg:15} ({version:10}) - {desc}')
    except ImportError:
        print(f'❌ {pkg:15} (MISSING)    - {desc}')
        missing.append(pkg)

if missing:
    print(f'\n⚠️  Missing packages: {", ".join(missing)}')
    print('Run: pip install -r core/source_proprietary/requirements-api.txt')
    sys.exit(1)
else:
    print('\n✅ All dependencies installed correctly!')
EOF
```

---

## Network Configuration

### CORS (Cross-Origin Resource Sharing)

The API server is configured to accept requests from specific origins. By default:

```python
# Default allowed origins (from main.py, lines 256-259)
"http://localhost:3000",
"http://localhost:8000", 
"http://127.0.0.1:3000",
"http://127.0.0.1:8000"
```

**To add custom origins**, set environment variable:

```bash
export MYTHARA_ALLOWED_ORIGINS="https://app.example.com,https://www.example.com"
```

### External API Endpoints

The server makes outbound HTTP calls to:

1. **ElevenLabs API** (Text-to-Speech)
   - Endpoint: `https://api.elevenlabs.io/v1/text-to-speech`
   - Line: 220 in `main.py`
   - Used for: Generating audio responses via `/v1/voice/generate` endpoint
   - Requires: `ELEVENLABS_API_KEY` environment variable

**To configure ElevenLabs**:

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

---

## Testing Network Connectivity

### Test 1: Verify Server is Running

```bash
# Check if server process is running
ps aux | grep uvicorn

# Check if port 8000 is listening
netstat -tuln | grep 8000
# or on some systems:
ss -tuln | grep 8000
```

### Test 2: Test API Endpoint

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}
```

### Test 3: Test with Authentication

```bash
# Test clause invocation (requires API key)
curl -X POST http://localhost:8000/v1/clauses/invoke \
  -H "Authorization: Bearer dev_test_key_001" \
  -H "Content-Type: application/json" \
  -d '{
    "clause_id": "Legacy_Seed",
    "messenger": "M-001", 
    "payload": {"emotion": "grief", "intensity": 0.87},
    "consent_token": "test_consent"
  }'
```

### Test 4: Test External API (ElevenLabs)

```bash
# This requires ELEVENLABS_API_KEY to be set
curl -X POST http://localhost:8000/v1/voice/generate \
  -H "Authorization: Bearer dev_test_key_001" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test message",
    "voice_id": "test_voice"
  }'
```

---

## Environment Variables

Create a `.env` file in the root directory:

```bash
# API Keys
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# CORS Configuration
MYTHARA_ALLOWED_ORIGINS=http://localhost:3000,https://app.example.com

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/mythara

# Redis (if using caching)
REDIS_URL=redis://localhost:6379

# Email (if using SendGrid)
SENDGRID_API_KEY=your_sendgrid_key_here
SENDGRID_FROM_EMAIL=noreply@mythara.com
```

---

## Docker Deployment (Network Isolation)

If using Docker, ensure proper network configuration:

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build:
      context: .
      dockerfile: core/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    networks:
      - mythara-network

networks:
  mythara-network:
    driver: bridge
```

---

## Summary Checklist

Before running the API server, ensure:

- [x] Python 3.11+ is installed
- [x] All root dependencies installed: `pip install -r requirements.txt`
- [x] All API dependencies installed: `pip install -r core/source_proprietary/requirements-api.txt`
- [x] `httpx` is available: `python3 -c "import httpx"`
- [x] Environment variables configured (`.env` file or export commands)
- [x] Port 8000 is available (not used by another process)
- [x] Firewall allows connections on port 8000 (if applicable)
- [x] External API keys configured (for ElevenLabs, SendGrid, etc.)

**Quick verification**:

```bash
# One-line dependency check
python3 -c "import httpx, fastapi, uvicorn, pydantic; print('✅ All critical packages installed')" && echo "✅ Ready to start server" || echo "❌ Install dependencies first"
```

---

## Additional Resources

- **API Documentation**: `core/source_proprietary/README_API.md`
- **Full Installation Guide**: `README.md` (lines 26-53)
- **Docker Setup**: `core/Dockerfile` and `core/source_proprietary/docker-compose.yml`
- **Copilot Instructions**: `.github/copilot-instructions.md`
- **Dual Framing Guide**: `DUAL_FRAMING_GUIDE.md`

---

**For support or questions**, refer to the repository documentation or contact the development team.
