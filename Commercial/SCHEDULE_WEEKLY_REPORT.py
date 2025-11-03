# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Windows Task Scheduler Setup for Weekly Analytics Report

Automatically runs weekly_analytics_report.py every Sunday at 6:00 PM MT
Sends PDF report to Herbievelezjr@gmail.com
"""

SETUP_INSTRUCTIONS = """
================================================================================
📅 SCHEDULE WEEKLY ANALYTICS REPORT (Windows Task Scheduler)
================================================================================

1. Open Task Scheduler:
   - Press Windows + R
   - Type: taskschd.msc
   - Press Enter

2. Create New Task:
   - Click "Create Basic Task" (right sidebar)
   - Name: "Mythara Weekly Sales Analytics"
   - Description: "Sends weekly sales bot performance report PDF every Sunday"
   - Click Next

3. Set Trigger (When):
   - Select: "Weekly"
   - Click Next
   - Start date: (Today's date)
   - Start time: 18:00:00 (6:00 PM MT)
   - Recur every: 1 week
   - Select: Sunday
   - Click Next

4. Set Action (What):
   - Select: "Start a program"
   - Click Next
   - Program/script: C:\\Users\\HVele\\AppData\\Local\\Microsoft\\WindowsApps\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\python.exe
   - Add arguments: -3.11 weekly_analytics_report.py
   - Start in: C:\\Users\\HVele\\OneDrive\\Desktop\\Mythara_Archive\\Commercial
   - Click Next

5. Review and Finish:
   - Review settings
   - Check "Open the Properties dialog when I click Finish"
   - Click Finish

6. Configure Properties:
   - On General tab:
     - Select "Run whether user is logged on or not"
     - Check "Run with highest privileges"
   - On Settings tab:
     - Check "Run task as soon as possible after a scheduled start is missed"
     - Check "If the task fails, restart every: 10 minutes, Attempt to restart up to: 3 times"
   - Click OK
   - Enter your Windows password when prompted

================================================================================
✅ TASK SCHEDULED - Weekly reports will be sent automatically
================================================================================

📧 What Happens Every Sunday 6pm:
   1. Script runs automatically
   2. Analyzes last 7 days of bot activity
   3. Generates PDF report
   4. (Once Gmail OAuth configured) Emails PDF to Herbievelezjr@gmail.com

📋 Report Includes:
   - Emails sent/received
   - Response rates
   - Blessings score
   - Deals closed
   - Governance violations
   - Performance strengths
   - Recommended improvements

💡 To Test Now:
   - Right-click task in Task Scheduler
   - Click "Run"
   - Check Commercial folder for PDF

================================================================================
"""

print(SETUP_INSTRUCTIONS)

# Alternative: Create task via PowerShell command
POWERSHELL_COMMAND = """
# PowerShell command to create task (run as Administrator):

$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 weekly_analytics_report.py' -WorkingDirectory 'C:\\Users\\HVele\\OneDrive\\Desktop\\Mythara_Archive\\Commercial'

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 6:00PM

Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Mythara Weekly Sales Analytics" -Description "Sends weekly sales bot performance report PDF every Sunday at 6pm MT"
"""

print("\n📌 ALTERNATIVE: PowerShell One-Liner")
print("="*80)
print(POWERSHELL_COMMAND)
print("="*80)
