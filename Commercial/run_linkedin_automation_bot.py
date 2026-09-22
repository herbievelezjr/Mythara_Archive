# Copyright © 2025 Herbert Velez Jr. All rights reserved.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from mythara_linkedin_automation_bot import *

if __name__ == "__main__":
    bot = LinkedInAutomationBot()
    bot.run()
