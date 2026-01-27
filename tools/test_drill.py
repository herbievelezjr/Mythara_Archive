#!/usr/bin/env python3
"""Quick drill test - Copyright © 2025 Herbert Velez Jr."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sere_security_system
bot = sere_bot.SERESecuritySystem()
bot.full_sere_drill()
print("\n✓ Test complete - drill executed successfully")
