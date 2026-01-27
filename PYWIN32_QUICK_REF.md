# SERE Sovereign Security System + Pywin32 Quick Reference

**Enhanced Windows Security Capabilities**

---

## Quick Start

```python
from sere_security_system import SERESecuritySystem

sere = SERESecuritySystem()

# Run comprehensive system audit
results = sere.full_system_audit()

# Scan specific threats
suspicious_procs = sere.scan_suspicious_processes()
suspicious_svcs = sere.scan_suspicious_services()
persistence = sere.scan_registry_persistence()
tampering = sere.scan_system_integrity()
lateral_move = sere.scan_lateral_movement()

# Remediate threats
sere.remediate_threat('process', '1234')        # Kill process by PID
sere.remediate_threat('service', 'ServiceName') # Stop service
sere.remediate_threat('registry', 'HKEY_...')  # Remove registry entry
```

---

## 5 New Controllers

| Controller | Purpose | Key Methods |
|-----------|---------|------------|
| **WindowsProcessController** | Process mgmt | `get_process_list()`, `find_suspicious_processes()`, `terminate_process()` |
| **WindowsServiceController** | Service mgmt | `list_services()`, `find_suspicious_services()`, `stop_service()` |
| **WindowsRegistryMonitor** | Registry security | `scan_startup_registry()`, `remove_registry_entry()` |
| **WindowsFileIntegrityMonitor** | File tampering | `scan_critical_files()` |
| **WindowsSessionMonitor** | Logon security | `get_active_sessions()`, `detect_lateral_movement()` |

---

## SERE Sovereign Security System Methods (New)

```
scan_suspicious_processes(keywords=None)     → List[Process]
scan_suspicious_services()                   → List[Service]
scan_registry_persistence()                  → List[RegistryEntry]
scan_system_integrity()                      → Dict[Path, Files]
scan_lateral_movement()                      → List[Logon]
full_system_audit()                          → Dict[All Results]
remediate_threat(type, target, force=False)  → bool
```

---

## Auto-Detection Keywords

**Processes:** mimikatz, psexec, metasploit, backdoor, malware, ransomware, trojan, worm, virus, payload

**Services:** Checks for suspicious paths (TEMP, AppData) and suspicious names (malware, backdoor, remote)

**Registry:** Scans startup locations for entries pointing to suspicious executables

**Files:** Flags system files in Windows\System32, SysWOW64, Program Files modified in last 7 days

---

## Threat Remediation

```python
# Process termination
sere.remediate_threat('process', '4852')
# Protected processes (svchost, lsass, csrss, etc.) cannot be terminated

# Service stopping  
sere.remediate_threat('service', 'UnknownService')
# Protected services (WinDefend, SecurityHealth, etc.) cannot be stopped

# Registry entry removal
sere.remediate_threat('registry', 'HKEY_CURRENT_USER|Software\Run|BadKey')
# Format: HKEY_HIVE|registry_path|value_name
```

---

## Dependencies

```bash
pip install pywin32 wmi
python Scripts/pywin32_postinstall.py -install
```

Run as Administrator for full capabilities.

---

## Integration with PIRE

```
SERE Sovereign Security System (Pywin32 Detection) → PIRE (Intent Analysis) → SERE Sovereign Security System (Remediation)

Detect threat → Classify as malicious → Terminate process
```

---

## Safety Features

✅ Protected system processes/services cannot be killed/stopped
✅ All operations logged to Windows Event Log
✅ Graceful fallback if Pywin32 unavailable
✅ Non-destructive scans (read-only by default)
✅ Requires explicit action for remediation

---

## Example: Full Defense Loop

```python
sere = SERESecuritySystem()

# 1. Scan everything
audit = sere.full_system_audit()

# 2. Check for threats
if audit['suspicious_processes']:
    for proc in audit['suspicious_processes']:
        sere.remediate_threat('process', str(proc['pid']))

if audit['registry_persistence']:
    for entry in audit['registry_persistence']:
        sere.remediate_threat('registry', entry)

if audit['lateral_movement']:
    sere.initiate_escape("Lateral movement detected!", critical=True)

# 3. Report
print(f"Threats found: {len(audit['suspicious_processes']) + len(audit['suspicious_services'])}")
```

---

See `PYWIN32_ENHANCEMENTS.md` for full documentation.
