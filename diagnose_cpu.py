#!/usr/bin/env python3
"""Quick diagnostic of CPU investigation system"""
import os
import json
import psutil
from sere_security_system import SERESecuritySystem

print('\n' + '='*70)
print('DIAGNOSING CPU ANOMALY DETECTION & REPAIR')
print('='*70)

# Current system state
print('\n[1] Current System State:')
cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent
print(f'  Current CPU: {cpu}%')
print(f'  Current Memory: {memory}%')

# Initialize bot
print('\n[2] Initializing SERE Bot...')
bot = SERESecuritySystem()
baseline = getattr(bot, 'baseline_cpu', None)
print(f'  Baseline CPU: {baseline}%')
if baseline:
    print(f'  Anomaly Threshold: >85% OR >3x baseline ({baseline*3:.1f}%)')
else:
    print(f'  Anomaly Threshold: >85%')

# Check investigation reports
print('\n[3] Investigation Report History:')
report_file = 'sere_cpu_investigation_report.json'
if os.path.exists(report_file):
    with open(report_file, 'r') as f:
        reports = json.load(f)
    print(f'  Total investigations: {len(reports)}')
    if reports:
        latest = reports[-1]
        print(f'  Latest: {latest.get("timestamp", "N/A")}')
        print(f'  Status: {latest.get("resolution_status", "N/A")}')
        print(f'  CPU at time: {latest.get("cpu_usage", "N/A")}%')
        if latest.get('suspicious_processes'):
            print(f'  Processes found: {len(latest["suspicious_processes"])}')
else:
    print('  No reports yet (first run)')

# Check threat detection
print('\n[4] Running Threat Detection Now:')
threats = bot.detect_threats()
print(f'  Threats detected: {len(threats)}')
if threats:
    for t in threats:
        print(f'    - {t.attack_type.value}: {t.severity.name}')

# Check actual CPU usage on system
print('\n[5] Top CPU Consuming Processes:')
top_procs = []
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
        if pinfo['cpu_percent'] and pinfo['cpu_percent'] > 5:
            top_procs.append(pinfo)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

top_procs = sorted(top_procs, key=lambda x: x['cpu_percent'], reverse=True)[:5]
if top_procs:
    for p in top_procs:
        print(f'  {p["name"]} (PID: {p["pid"]}): {p["cpu_percent"]}%')
else:
    print('  No processes >5% CPU')

print('\n' + '='*70)
print('DIAGNOSIS & RECOMMENDATION:')
print('='*70)

if cpu > 85:
    print('CPU is HIGH (>85%) - Investigation should auto-trigger')
elif baseline and cpu > baseline * 3:
    print(f'CPU is ELEVATED (>{baseline*3:.1f}%) - Investigation should auto-trigger')
else:
    print('CPU is NORMAL - System operating within expected parameters')
    print('\nIMPORTANT: The investigation system is REACTIVE, not PREVENTIVE')
    print('It only triggers when CPU spikes above threshold.')
    print('\nTo PROACTIVELY reduce CPU spikes:')
    print('1. Identify what processes are using CPU (see list above)')
    print('2. Check if they are legitimate or malicious')
    print('3. Kill problematic processes manually')
    print('4. System will investigate high spikes when they occur')

print('='*70)
