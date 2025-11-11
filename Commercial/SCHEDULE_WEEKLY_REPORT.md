# SCHEDULE_WEEKLY_REPORT.py — Internal Usage Notes

This file previously contained Windows Task Scheduler setup instructions as a Python string. For clarity and script validity, these instructions are now in this markdown file.

## How to Schedule Weekly Analytics Report (Windows)

1. Open Task Scheduler:
   - Press Windows + R
   - Type: `taskschd.msc`
   - Press Enter
2. Create New Task:
   - Name: "Mythara Weekly Sales Analytics"
   - Description: "Sends weekly sales bot performance report PDF every Sunday"
   - Set trigger: Weekly, Sunday, 6:00 PM MT
   - Set action: Start program, point to your Python 3.11 executable, run `weekly_analytics_report.py`
   - Set working directory to the `Commercial` folder
3. Configure properties:
   - Run with highest privileges
   - Run whether user is logged on or not
   - Set restart on failure options as needed
4. Save and enter your Windows password if prompted.

✅ Task will send weekly reports automatically.
