#!/usr/bin/env python3
"""
Mythara Engine - Dependency Validation Script

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

This script validates that all required dependencies are installed
and provides clear guidance on what to install if anything is missing.
"""

import sys
from typing import Dict, List, Tuple

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


def check_python_version() -> bool:
    """Check if Python version is 3.11 or higher"""
    version = sys.version_info
    print(f"\n{BOLD}Python Version Check:{RESET}")
    print(f"  Current: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 11:
        print(f"  {GREEN}✅ Python version OK (3.11+ required){RESET}")
        return True
    else:
        print(f"  {RED}❌ Python 3.11+ required, found {version.major}.{version.minor}{RESET}")
        return False


def check_package(package_name: str, description: str) -> Tuple[bool, str]:
    """
    Check if a package is installed and return its version
    
    Returns:
        (is_installed, version)
    """
    try:
        mod = __import__(package_name)
        version = getattr(mod, '__version__', 'unknown')
        return (True, version)
    except ImportError:
        return (False, '')


def check_core_dependencies() -> Tuple[int, int]:
    """
    Check core dependencies from requirements.txt
    
    Returns:
        (installed_count, total_count)
    """
    print(f"\n{BOLD}Core Dependencies (requirements.txt):{RESET}")
    
    packages: Dict[str, str] = {
        'click': 'CLI framework',
        'pydantic': 'Data validation',
        'yaml': 'YAML parsing (PyYAML)',
        'pytest': 'Testing framework',
        'numpy': 'Scientific computing',
        'pandas': 'Data processing',
        'cryptography': 'Security and encryption',
    }
    
    installed = 0
    total = len(packages)
    
    for pkg, desc in packages.items():
        is_installed, version = check_package(pkg, desc)
        if is_installed:
            print(f"  {GREEN}✅{RESET} {pkg:15} ({version:10}) - {desc}")
            installed += 1
        else:
            print(f"  {RED}❌{RESET} {pkg:15} {RED}(MISSING){RESET}    - {desc}")
    
    return (installed, total)


def check_api_dependencies() -> Tuple[int, int]:
    """
    Check API-specific dependencies from core/source_proprietary/requirements-api.txt
    
    Returns:
        (installed_count, total_count)
    """
    print(f"\n{BOLD}API Dependencies (core/source_proprietary/requirements-api.txt):{RESET}")
    
    packages: Dict[str, str] = {
        'httpx': 'HTTP client for external APIs (CRITICAL)',
        'fastapi': 'Web framework (CRITICAL)',
        'uvicorn': 'ASGI server (CRITICAL)',
        'pydantic': 'Data validation (CRITICAL)',
        'sqlalchemy': 'Database ORM',
        'sendgrid': 'Email service',
        'stripe': 'Payment processing',
        'jose': 'JWT tokens (python-jose)',
        'passlib': 'Password hashing',
        'markdown': 'Markdown rendering',
    }
    
    installed = 0
    total = len(packages)
    
    for pkg, desc in packages.items():
        is_installed, version = check_package(pkg, desc)
        if is_installed:
            print(f"  {GREEN}✅{RESET} {pkg:15} ({version:10}) - {desc}")
            installed += 1
        else:
            critical = '(CRITICAL)' in desc
            marker = f"{RED}❌ CRITICAL{RESET}" if critical else f"{YELLOW}⚠️{RESET} "
            print(f"  {marker} {pkg:15} {RED}(MISSING){RESET}    - {desc}")
    
    return (installed, total)


def check_optional_dependencies() -> None:
    """Check optional dependencies"""
    print(f"\n{BOLD}Optional Dependencies:{RESET}")
    
    packages: Dict[str, str] = {
        'redis': 'Redis caching (optional)',
        'psycopg2': 'PostgreSQL driver (optional, for production)',
    }
    
    for pkg, desc in packages.items():
        is_installed, version = check_package(pkg, desc)
        if is_installed:
            print(f"  {GREEN}✅{RESET} {pkg:15} ({version:10}) - {desc}")
        else:
            print(f"  {YELLOW}ℹ️{RESET}  {pkg:15} {YELLOW}(not installed){RESET} - {desc}")


def print_installation_instructions(missing_core: bool, missing_api: bool) -> None:
    """Print installation instructions for missing dependencies"""
    if not (missing_core or missing_api):
        return
    
    print(f"\n{BOLD}{YELLOW}Installation Instructions:{RESET}")
    
    if missing_core:
        print(f"\n{YELLOW}To install core dependencies:{RESET}")
        print(f"  {BLUE}pip install -r requirements.txt{RESET}")
    
    if missing_api:
        print(f"\n{YELLOW}To install API dependencies:{RESET}")
        print(f"  {BLUE}pip install -r core/source_proprietary/requirements-api.txt{RESET}")
    
    print(f"\n{YELLOW}Or install everything at once:{RESET}")
    print(f"  {BLUE}pip install -r requirements.txt{RESET}")
    print(f"  {BLUE}pip install -r core/source_proprietary/requirements-api.txt{RESET}")


def check_network_connectivity() -> None:
    """Check basic network connectivity for external APIs"""
    print(f"\n{BOLD}Network Connectivity Check:{RESET}")
    
    try:
        import httpx
        print(f"  {GREEN}✅ httpx installed - can test connectivity{RESET}")
        
        # Test connectivity to ElevenLabs API
        try:
            import asyncio
            
            async def test_connectivity():
                async with httpx.AsyncClient(timeout=5.0) as client:
                    try:
                        response = await client.get("https://api.elevenlabs.io")
                        print(f"  {GREEN}✅ ElevenLabs API reachable (status: {response.status_code}){RESET}")
                        return True
                    except httpx.TimeoutException:
                        print(f"  {YELLOW}⚠️  ElevenLabs API timeout (may be slow network){RESET}")
                        return False
                    except httpx.ConnectError:
                        print(f"  {RED}❌ Cannot connect to ElevenLabs API (network issue){RESET}")
                        return False
            
            asyncio.run(test_connectivity())
            
        except Exception as e:
            print(f"  {YELLOW}⚠️  Could not test connectivity: {e}{RESET}")
    
    except ImportError:
        print(f"  {YELLOW}⚠️  httpx not installed - skipping connectivity test{RESET}")


def print_summary(python_ok: bool, core_installed: int, core_total: int, 
                 api_installed: int, api_total: int) -> int:
    """
    Print summary and return exit code
    
    Returns:
        0 if all OK, 1 if missing dependencies
    """
    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}SUMMARY:{RESET}")
    
    all_ok = True
    
    if not python_ok:
        print(f"  {RED}❌ Python version too old{RESET}")
        all_ok = False
    else:
        print(f"  {GREEN}✅ Python version OK{RESET}")
    
    core_ok = core_installed == core_total
    if core_ok:
        print(f"  {GREEN}✅ Core dependencies: {core_installed}/{core_total} installed{RESET}")
    else:
        print(f"  {RED}❌ Core dependencies: {core_installed}/{core_total} installed ({core_total - core_installed} missing){RESET}")
        all_ok = False
    
    api_ok = api_installed == api_total
    if api_ok:
        print(f"  {GREEN}✅ API dependencies: {api_installed}/{api_total} installed{RESET}")
    else:
        print(f"  {RED}❌ API dependencies: {api_installed}/{api_total} installed ({api_total - api_installed} missing){RESET}")
        all_ok = False
    
    print(f"{BOLD}{'='*70}{RESET}")
    
    if all_ok:
        print(f"\n{GREEN}{BOLD}✅ All dependencies installed correctly!{RESET}")
        print(f"{GREEN}You can now start the Mythara Engine API server.{RESET}\n")
        print(f"Start the server with:")
        print(f"  {BLUE}python core/source_proprietary/main.py{RESET}")
        print(f"  {BLUE}# or{RESET}")
        print(f"  {BLUE}uvicorn core.source_proprietary.main:app --reload --host 0.0.0.0 --port 8000{RESET}\n")
        return 0
    else:
        print(f"\n{RED}{BOLD}❌ Missing dependencies detected!{RESET}")
        print(f"{YELLOW}Please install missing dependencies before starting the server.{RESET}\n")
        return 1


def main() -> int:
    """Main validation function"""
    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}Mythara Engine - Dependency Validation{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check core dependencies
    core_installed, core_total = check_core_dependencies()
    
    # Check API dependencies
    api_installed, api_total = check_api_dependencies()
    
    # Check optional dependencies
    check_optional_dependencies()
    
    # Check network connectivity (if httpx is available)
    check_network_connectivity()
    
    # Print installation instructions if needed
    missing_core = core_installed < core_total
    missing_api = api_installed < api_total
    print_installation_instructions(missing_core, missing_api)
    
    # Print summary and return exit code
    return print_summary(python_ok, core_installed, core_total, 
                        api_installed, api_total)


if __name__ == "__main__":
    sys.exit(main())
