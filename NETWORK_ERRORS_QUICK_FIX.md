# Network Errors Quick Fix Guide

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

---

## 🚨 Seeing Network Errors?

### Most Common Issue: Missing `httpx` Library

**Error Message:**
```
ModuleNotFoundError: No module named 'httpx'
```

**Quick Fix:**
```bash
pip install -r core/source_proprietary/requirements-api.txt
```

---

## ✅ Complete Installation (Start Here)

```bash
# Step 1: Install core dependencies
pip install -r requirements.txt

# Step 2: Install API dependencies (REQUIRED for API server)
pip install -r core/source_proprietary/requirements-api.txt

# Step 3: Validate everything is installed
python validate_dependencies.py
```

---

## 🔍 Verify Installation

**Check critical packages:**
```bash
python -c "import httpx; print('✅ httpx:', httpx.__version__)"
python -c "import fastapi; print('✅ FastAPI:', fastapi.__version__)"
python -c "import uvicorn; print('✅ Uvicorn:', uvicorn.__version__)"
```

**Or use the validation script:**
```bash
python validate_dependencies.py
```

Expected output: `✅ All dependencies installed correctly!`

---

## 🚀 Start the Server

**After dependencies are installed:**
```bash
# Method 1: Direct script
python core/source_proprietary/main.py

# Method 2: Using uvicorn
uvicorn core.source_proprietary.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🔧 Test API Endpoints

**Health check:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{"status":"healthy","version":"1.0.0"}
```

---

## 📚 Detailed Documentation

- **Complete troubleshooting guide**: `NETWORK_ERRORS_EXPLAINED.md`
- **API documentation**: `core/source_proprietary/README_API.md`
- **Installation guide**: `README.md` (Quickstart section)
- **Copilot instructions**: `.github/copilot-instructions.md`

---

## 🆘 Still Having Issues?

### Issue: "Connection Refused"
**Cause**: Server not running  
**Fix**: Check if uvicorn process is running: `ps aux | grep uvicorn`

### Issue: "Timeout" on external API calls
**Cause**: Missing `httpx` or network connectivity  
**Fix**: 
1. Install httpx: `pip install httpx==0.25.2`
2. Check network: `curl https://api.elevenlabs.io`

### Issue: "Import Error" for other packages
**Cause**: Incomplete dependency installation  
**Fix**: Run both pip install commands above

---

## 📦 What Each Requirements File Contains

### `requirements.txt` (Core)
- Testing frameworks (pytest)
- Data processing (numpy, pandas)
- Security (cryptography)
- CLI tools (click)

### `core/source_proprietary/requirements-api.txt` (API)
- **httpx** - HTTP client for external APIs ⚠️ CRITICAL
- **FastAPI** - Web framework ⚠️ CRITICAL
- **uvicorn** - ASGI server ⚠️ CRITICAL
- **pydantic** - Data validation ⚠️ CRITICAL
- SQLAlchemy, SendGrid, Stripe, etc.

**Both are required for the API server to function!**

---

## 💡 Pro Tips

1. **Use a virtual environment** to avoid conflicts:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Verify before starting**: Always run `python validate_dependencies.py` first

3. **Check logs**: If server fails, check terminal output for specific errors

4. **Environment variables**: Create a `.env` file for API keys (see `.env.example`)

---

**For complete documentation, see: `NETWORK_ERRORS_EXPLAINED.md`**
