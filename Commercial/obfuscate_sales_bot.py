# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
PyArmor Obfuscation Script for Sales Bot IP Protection

Obfuscates Python code to protect trade secrets.
Result: .pyc files that run but are unreadable.

Easier than Cython (no compilation), works cross-platform.
"""

import subprocess
import sys
from pathlib import Path

def obfuscate_sales_bot():
    """Obfuscate proprietary sales bot code with PyArmor"""
    
    print("="*80)
    print("🔒 SALES BOT IP PROTECTION - PyArmor Obfuscation")
    print("="*80)
    
    # Check if PyArmor is installed
    try:
        result = subprocess.run(
            ["pyarmor", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print("\n❌ PyArmor not installed.")
            print("\nInstall with:")
            print("   py -3.11 -m pip install pyarmor")
            print("\nFor maximum protection, upgrade to PyArmor Pro ($69/year):")
            print("   https://pyarmor.dashingsoft.com/")
            return False
            
        print(f"\n✅ PyArmor installed: {result.stdout.strip()}")
        
    except FileNotFoundError:
        print("\n❌ PyArmor not found in PATH")
        print("\nInstall with:")
        print("   py -3.11 -m pip install pyarmor")
        return False
    
    # Files to obfuscate (proprietary IP)
    files_to_protect = [
        "sales_bot_with_soul.py",
        "sales_bot_ssip_governance.py", 
        "autonomous_sales_bot.py",
        "email_assistant.py"
    ]
    
    print("\n📁 Files to obfuscate:")
    for f in files_to_protect:
        if Path(f).exists():
            print(f"   ✅ {f}")
        else:
            print(f"   ❌ {f} (not found)")
    
    # Obfuscate each file
    print("\n🔒 Obfuscating...")
    
    for file in files_to_protect:
        if not Path(file).exists():
            print(f"   ⏭️  Skipping {file} (not found)")
            continue
        
        print(f"\n   🔐 Obfuscating {file}...")
        
        # PyArmor command: obfuscate with restrictions
        result = subprocess.run(
            [
                "pyarmor",
                "gen",
                "--restrict",  # Prevent import from other scripts
                "--output", "dist",  # Output to dist/ folder
                file
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"   ✅ {file} → dist/{file}")
        else:
            print(f"   ❌ Failed: {result.stderr}")
    
    # Create customer delivery package
    print("\n📦 Creating customer package...")
    
    dist_path = Path("dist")
    if dist_path.exists():
        print("\n✅ Customer Delivery Package Ready:")
        print(f"   Location: {dist_path.absolute()}")
        print("\n   Files to deliver:")
        for f in dist_path.glob("*.py"):
            print(f"      - {f.name} (obfuscated)")
        
        print("\n   📋 Also include:")
        print("      - requirements.txt")
        print("      - README.md (setup instructions)")
        print("      - License key (generate separately)")
        
        print("\n🔐 IP Protection Applied:")
        print("   ✅ Code is obfuscated (unreadable)")
        print("   ✅ Restricted imports (can't be stolen)")
        print("   ✅ Original .py files NOT included")
        
        print("\n💡 Next Steps:")
        print("   1. Test obfuscated code: py -3.11 dist/sales_bot_with_soul.py")
        print("   2. Generate license key for customer")
        print("   3. Zip dist/ folder for delivery")
        print("   4. Invoice customer ($500-$5,000)")
        
        return True
    else:
        print("\n❌ Obfuscation failed - dist/ folder not created")
        return False


if __name__ == "__main__":
    success = obfuscate_sales_bot()
    
    if success:
        print("\n" + "="*80)
        print("✅ SALES BOT PROTECTED - Ready for Customer Delivery")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ PROTECTION FAILED - Fix errors above")
        print("="*80)
        sys.exit(1)
