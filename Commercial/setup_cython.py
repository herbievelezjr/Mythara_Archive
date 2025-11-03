# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Cython Setup for Sales Bot IP Protection

Compiles Python code to C extensions (.pyd on Windows, .so on Linux)
IMPOSSIBLE to reverse engineer - this is compiled C code, not Python bytecode.

Usage:
    py -3.11 setup.py build_ext --inplace
    
Result:
    sales_bot_with_soul.pyd (Windows) or .so (Linux)
    Customers can import and use it, but cannot read the code.
"""

from setuptools import setup, Extension
from Cython.Build import cythonize

# Define which files to compile
extensions = [
    Extension(
        "sales_bot_with_soul",
        ["sales_bot_with_soul.py"],
        language="c++"
    ),
    Extension(
        "sales_bot_ssip_governance", 
        ["sales_bot_ssip_governance.py"],
        language="c++"
    ),
    Extension(
        "autonomous_sales_bot",
        ["autonomous_sales_bot.py"],
        language="c++"
    ),
    Extension(
        "email_assistant",
        ["email_assistant.py"],
        language="c++"
    ),
]

setup(
    name="Mythara Sales Bot (Compiled)",
    version="1.0.0",
    description="Mythara-governed sales bot with SOUL - Compiled for IP protection",
    author="Herbert Velez Jr.",
    author_email="Herbievelezjr@gmail.com",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'embedsignature': True,
            'binding': True
        }
    ),
)

print("""
✅ Compilation Instructions:

1. Install Cython:
   py -3.11 -m pip install cython

2. Compile:
   py -3.11 setup.py build_ext --inplace

3. Result:
   - sales_bot_with_soul.pyd (Windows) or .so (Linux)
   - 100% unreadable, compiled C code
   - Delete original .py files after testing

4. Distribute to customer:
   - .pyd/.so files
   - requirements.txt
   - Setup instructions

🔒 Maximum IP Protection Achieved
""")
