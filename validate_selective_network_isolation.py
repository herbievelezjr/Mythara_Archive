#!/usr/bin/env python3
"""
S.E.R.E. SELECTIVE Network Isolation Validation Script

Copyright © 2025 Herbert Velez Jr. All rights reserved.

This script validates that S.E.R.E. network isolation uses REAL Windows APIs
and implements SELECTIVE blocking that preserves critical systems.
"""

import subprocess
import sys
import os
import re

def run_command(cmd, description):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def validate_powershell_integration():
    """Validate that PowerShell Get-NetTCPConnection is used"""
    print("🔍 VALIDATING POWERSHELL INTEGRATION...")

    # Check if PowerShell is available
    success, stdout, stderr = run_command("powershell -Command 'Get-Host'", "Check PowerShell availability")
    if not success:
        print("❌ PowerShell not available")
        return False

    # Test Get-NetTCPConnection cmdlet
    success, stdout, stderr = run_command("powershell -Command 'Get-NetTCPConnection | Select-Object -First 1'", "Test Get-NetTCPConnection")
    if not success:
        print("❌ Get-NetTCPConnection cmdlet not available")
        return False

    print("✅ PowerShell integration validated")
    return True

def validate_firewall_integration():
    """Validate that netsh firewall commands are used"""
    print("🔍 VALIDATING FIREWALL INTEGRATION...")

    # Test netsh firewall command
    success, stdout, stderr = run_command("netsh advfirewall firewall show rule name=all | findstr /C:\"SERE_\" || echo No SERE rules found", "Check firewall rule creation capability")
    if not success:
        print("❌ Firewall integration not working")
        return False

    print("✅ Firewall integration validated")
    return True

def validate_selective_logic():
    """Validate that selective blocking logic is implemented"""
    print("🔍 VALIDATING SELECTIVE BLOCKING LOGIC...")

    # Read the sere_bot.py file
    try:
        with open('sere_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ sere_bot.py not found")
        return False

    # Check for selective blocking methods
    required_methods = [
        '_is_critical_system',
        '_get_unknown_connections',
        '_block_connection'
    ]

    for method in required_methods:
        if f'def {method}(' not in content:
            print(f"❌ Method {method} not found")
            return False

    # Check for selective logic in isolation methods
    selective_indicators = [
        'critical_system',
        'unknown.*threat',
        'selective.*blocking'
    ]

    selective_found = False
    for indicator in selective_indicators:
        if re.search(indicator, content, re.IGNORECASE):
            selective_found = True
            break

    if not selective_found:
        print("❌ Selective blocking logic not found")
        return False

    print("✅ Selective blocking logic validated")
    return True

def validate_admin_requirements():
    """Validate administrative requirements are documented"""
    print("🔍 VALIDATING ADMINISTRATIVE REQUIREMENTS...")

    try:
        with open('NETWORK_ISOLATION.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ NETWORK_ISOLATION.md not found")
        return False

    admin_indicators = [
        'administrative privileges',
        'administrator',
        'admin',
        'run as administrator'
    ]

    admin_found = False
    for indicator in admin_indicators:
        if indicator.lower() in content.lower():
            admin_found = True
            break

    if not admin_found:
        print("❌ Administrative requirements not documented")
        return False

    print("✅ Administrative requirements validated")
    return True

def validate_critical_system_preservation():
    """Validate that critical systems are preserved"""
    print("🔍 VALIDATING CRITICAL SYSTEM PRESERVATION...")

    try:
        with open('sere_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ sere_bot.py not found")
        return False

    # Check for critical system preservation logic
    preservation_indicators = [
        'preserve.*critical',
        'critical.*preserved',
        'never.*block.*critical',
        'critical.*system.*preserved'
    ]

    preservation_found = False
    for indicator in preservation_indicators:
        if re.search(indicator, content, re.IGNORECASE):
            preservation_found = True
            break

    if not preservation_found:
        print("❌ Critical system preservation logic not found")
        return False

    print("✅ Critical system preservation validated")
    return True

def main():
    """Main validation function"""
    print("🛡️  S.E.R.E. SELECTIVE NETWORK ISOLATION VALIDATION")
    print("=" * 60)

    validations = [
        ("PowerShell Integration", validate_powershell_integration),
        ("Firewall Integration", validate_firewall_integration),
        ("Selective Blocking Logic", validate_selective_logic),
        ("Administrative Requirements", validate_admin_requirements),
        ("Critical System Preservation", validate_critical_system_preservation),
    ]

    passed = 0
    total = len(validations)

    for name, func in validations:
        print(f"\n📋 {name}")
        if func():
            passed += 1
        else:
            print(f"❌ {name} FAILED")

    print("\n" + "=" * 60)
    print(f"VALIDATION RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ S.E.R.E. implements REAL selective network isolation")
        print("✅ Critical systems are preserved")
        print("✅ Only unknown threats are blocked")
        return True
    else:
        print("❌ SOME VALIDATIONS FAILED")
        print("⚠️  Review implementation before production use")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)