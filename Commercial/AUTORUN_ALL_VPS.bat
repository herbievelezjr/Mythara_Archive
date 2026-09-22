@echo off
REM Copyright (c) 2025 Herbert Velez Jr. All rights reserved.
REM 
REM Schedule all Mythara VP bots in Windows Task Scheduler
REM Run this script as Administrator

echo ============================================================
echo MYTHARA VP AUTORUN SCHEDULER
echo ============================================================
echo.
echo This script will schedule all 6 VP bots:
echo   1. VP of Sales ^& Marketing - Daily 8am
echo   2. VP of DevOps - Hourly
echo   3. VP of Logistics - Hourly
echo   4. VP of Finance - Daily 7am
echo   5. VP of Customer Success - Daily 10am
echo   6. VP of Public Affairs - Every 4 hours
echo.
pause

cd /d "%~dp0"

REM Finance VP - Daily 7am
echo.
echo [1/6] Scheduling Finance VP (Daily 7am)...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 run_finance_vp.py' -WorkingDirectory '%cd%'; $trigger = New-ScheduledTaskTrigger -Daily -At 7am; Register-ScheduledTask -TaskName 'Mythara_Finance_VP' -Action $action -Trigger $trigger -Force"
if %errorlevel%==0 (echo    [OK] Scheduled) else (echo    [ERROR] Failed)

REM Customer Success VP - Daily 10am
echo.
echo [2/6] Scheduling Customer Success VP (Daily 10am)...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 run_customer_success_vp.py' -WorkingDirectory '%cd%'; $trigger = New-ScheduledTaskTrigger -Daily -At 10am; Register-ScheduledTask -TaskName 'Mythara_Customer_Success_VP' -Action $action -Trigger $trigger -Force"
if %errorlevel%==0 (echo    [OK] Scheduled) else (echo    [ERROR] Failed)

REM Public Affairs VP - Every 4 hours
echo.
echo [3/6] Scheduling Public Affairs VP (Every 4 hours)...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 run_public_affairs_vp.py' -WorkingDirectory '%cd%'; $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 4); Register-ScheduledTask -TaskName 'Mythara_Public_Affairs_VP' -Action $action -Trigger $trigger -Force"
if %errorlevel%==0 (echo    [OK] Scheduled) else (echo    [ERROR] Failed)

REM Sales & Marketing VP - Daily 8am (update existing or create)
echo.
echo [4/6] Scheduling Sales ^& Marketing VP (Daily 8am)...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 mythara_vp_bot.py' -WorkingDirectory '%cd%'; $trigger = New-ScheduledTaskTrigger -Daily -At 8am; Register-ScheduledTask -TaskName 'Mythara_Sales_Marketing_VP' -Action $action -Trigger $trigger -Force"
if %errorlevel%==0 (echo    [OK] Scheduled) else (echo    [ERROR] Failed)

REM DevOps VP - Hourly
echo.
echo [5/6] Scheduling DevOps VP (Hourly)...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 run_devops_vp.py' -WorkingDirectory '%cd%'; $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1); Register-ScheduledTask -TaskName 'Mythara_DevOps_VP' -Action $action -Trigger $trigger -Force"
if %errorlevel%==0 (echo    [OK] Scheduled) else (echo    [ERROR] Failed)

REM Logistics VP - Hourly
echo.
echo [6/6] Scheduling Logistics VP (Hourly)...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'py' -Argument '-3.11 run_logistics_vp.py' -WorkingDirectory '%cd%'; $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1); Register-ScheduledTask -TaskName 'Mythara_Logistics_VP' -Action $action -Trigger $trigger -Force"
if %errorlevel%==0 (echo    [OK] Scheduled) else (echo    [ERROR] Failed)

echo.
echo ============================================================
echo SCHEDULING COMPLETE
echo ============================================================
echo.
echo All 6 VP bots are now scheduled.
echo.
echo To view scheduled tasks:
echo   taskschd.msc
echo.
echo To manually run a VP:
echo   schtasks /Run /TN "Mythara_Finance_VP"
echo.
pause
