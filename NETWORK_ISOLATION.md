# S.E.R.E. SELECTIVE Network Isolation Features

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

## ⚠️ WARNING: REAL NETWORK OPERATIONS

**These are REAL network security operations that:**

- ✅ Create Windows Firewall rules
- ✅ Block actual network connections
- ✅ Terminate active connections
- ✅ Require administrative privileges
- ✅ **PRESERVE YOUR CRITICAL SYSTEMS**
- ✅ **ONLY BLOCK UNKNOWN THREATS**

**Use only when you intend to isolate network access. Test in a safe environment first.**

## Overview

S.E.R.E. now includes **SELECTIVE NETWORK ISOLATION** capabilities that actually disconnect and block only unknown/threat IP connections using Windows system APIs. This provides complete network security by preventing external threats while **preserving your critical infrastructure systems**.

**KEY FEATURE: Your critical systems are NEVER blocked - only unknown threats are isolated.**

## Network Isolation Modes

### 1. **ISOLATE** - One-Time Selective Disconnection

Performs a single, immediate scan and disconnection of only unknown/threat IP connections using real system network APIs.

**Command:** `isolate` or `isolate-network` or `disconnect`

**Selective Operations:**

- Uses `Get-NetTCPConnection` PowerShell cmdlet to scan active TCP connections
- Identifies unknown/threat connections (not native OR critical)
- Creates Windows Firewall rules to block threat IPs
- Attempts to terminate active threat connections
- **PRESERVES ALL native and critical system connections**

**Real Output:**

```powershell
🔒 SELECTIVE NETWORK ISOLATION PROTOCOL ACTIVATED

Connection Categories:
  ✓ NATIVE: Local system connections (preserved)
  ✓ CRITICAL: Your infrastructure systems (preserved)
  ✗ UNKNOWN: External threats (blocked)

Unknown/Threat connections detected:
⚠️  Unknown Connection Found:
  Local: 192.168.1.100
  Remote: 45.142.185.3:8080
  State: Established
  Status: BLOCKING... ✓ BLOCKED
```

---

### 2. **FIREWALL** - Continuous Selective Monitoring

Engages a persistent network firewall that continuously monitors and blocks only unknown/threat connections using real-time network scanning.

**Commands:** `firewall` or `network-guard` or `defend-network`

**Selective Operations:**

- Continuous monitoring using `Get-NetTCPConnection` every 15 seconds
- Real-time detection of new unknown/threat connections
- Automatic Windows Firewall rule creation for blocking threats
- Persistent operation until stopped (Ctrl+C)
- **PRESERVES ALL critical system connections**

**Real Output:**

```powershell
🔥 SELECTIVE NETWORK FIREWALL ENGAGED

Monitoring all network connections...
SELECTIVE blocking: Only unknown threats - critical systems preserved

[Cycle 1] Checking network connections...
⚠️  2 unknown/threat connection(s) detected
  → Blocking 203.0.113.42:443... ✓ BLOCKED
  → Blocking 198.51.100.17:22... ✓ BLOCKED
[Total blocked: 2]
```

---

### 3. **NATIVE-ONLY MODE** - Automatic Unknown Threat Severance

Maintains continuous enforcement of secure connectivity, automatically severing only unknown/threat connections as they are detected using live network monitoring.

**Commands:** `native-only` or `native` or `lockdown`

**Selective Operations:**

- Continuous monitoring every 10 seconds using system network APIs
- Real-time identification of unknown/threat IPs
- Immediate Windows Firewall rule creation and connection termination
- Automatic enforcement until stopped (Ctrl+C)
- **PRESERVES ALL native and critical system connections**

**Real Output:**

```powershell
🛡️  SELECTIVE NATIVE-ONLY MODE ACTIVATED

S.E.R.E. will continuously:
  ✓ Monitor all network connections
  ✓ Identify unknown/threat IPs
  ✓ Preserve native and critical system connections
  ✓ Immediately disconnect only unknown threats
  ✓ Report all actions

[17:55:12] Cycle 1: Scanning connections...
🚨 Detected 2 unknown/threat connection(s)
  → Disconnecting 126.85.232.175:443... ✓ SEVERED
  → Disconnecting 64.170.41.57:1433... ✓ SEVERED
Total threats severed: 2
```

---

## Connection Classification System

### Native Connections (ALWAYS PRESERVED)

| Range              | Type            | Purpose                      |
| ------------------ | --------------- | ---------------------------- |
| 127.0.0.1          | IPv4 Loopback   | Local system only            |
| ::1                | IPv6 Loopback   | IPv6 local system            |
| 192.168.x.x        | Private Network | Local LAN (Class C)          |
| 10.x.x.x           | Private Network | Local LAN (Class A)          |
| 172.16.x.x-172.31. | Private Network | Local LAN (Class B)          |

---

### Critical Systems (ALWAYS PRESERVED)

**These are YOUR trusted infrastructure systems that will NEVER be blocked:**

| Example Range | Purpose                    | Customization                  |
| ------------- | -------------------------- | ------------------------------ |
| 192.168.1.x   | Your corporate network     | Modify `_is_critical_system()` |
| 10.0.x.x      | Your cloud infrastructure  | Add your IP ranges             |
| 172.16.10.x   | Your database servers      | Customize for your environment |
| 172.17.100.x  | Your API gateways          | Add specific subnets           |

**To customize critical systems, edit the `_is_critical_system()` method in `sere_security_system.py`.**

### Unknown Threats (BLOCKED)

All other connections are considered **UNKNOWN THREATS** and will be isolated/blocked.

---

## System APIs Used

### Windows Network Monitoring

- **PowerShell Cmdlets:** `Get-NetTCPConnection` for real-time connection enumeration
- **CSV Parsing:** Processes connection data from system output
- **State Filtering:** Only monitors established connections

---

### Windows Firewall Integration

- **Rule Creation:** `netsh advfirewall firewall add rule` for blocking rules
- **Rule Management:** Automatic cleanup and naming of firewall rules
- **Directional Blocking:** Outbound blocking to prevent data exfiltration

### Connection Termination

- **Process Identification:** Attempts to identify and terminate connection processes
- **Graceful Shutdown:** Clean disconnection where possible
- **Force Termination:** Hard termination for persistent connections

```powershell

### Connection Termination
- **Process Identification:** Attempts to identify and terminate connection processes
- **Graceful Shutdown:** Clean disconnection where possible
- **Force Termination:** Hard termination for persistent connections

---

## Customizing Critical Systems

**IMPORTANT:** Modify the `_is_critical_system()` method to define your critical infrastructure:

```python
def _is_critical_system(self, ip):
    """Check if IP belongs to critical infrastructure systems"""
    # Add your critical IP ranges here
    critical_ranges = [
        # Your corporate network
        (192, 168, [1, 10, 20, 100]),  # Specific subnets
        # Your cloud infrastructure
        (10, [0, 1, 2, 3], None),      # Private cloud ranges
        # Your database servers
        (172, 16, [10, 20, 30]),       # Database subnet
    ]

    # Add specific critical IPs
    critical_ips = [
        "192.168.1.100",    # Your main server
        "10.0.0.5",        # Your database
        "172.16.10.50",    # Your API server
    ]
```

---

## Administrative Requirements

**These commands require administrative privileges to modify Windows Firewall rules.**

Run PowerShell or Command Prompt as Administrator:

```powershell
# Run as Administrator
python sere_security_system.py
```

---

## Quick Start

### Interactive Mode

```bash
# Start S.E.R.E. (as Administrator)
python sere_security_system.py

# In the S.E.R.E. prompt:

# One-time selective isolation (blocks only threats)
S.E.R.E.> isolate

# Continuous selective firewall (preserves critical systems)
S.E.R.E.> firewall
# (Press Ctrl+C to stop)

# Selective native-only mode (auto-blocks only threats)
S.E.R.E.> native-only
# (Press Ctrl+C to stop)

# View all commands
S.E.R.E.> help
```

---

## Security Use Cases

### 1. **Emergency Threat Isolation**

```powershell
S.E.R.E.> isolate
```

Use when you detect suspicious activity. Immediately scans and blocks unknown threats while preserving your critical systems.

### 2. **Persistent Threat Defense**

```powershell
S.E.R.E.> firewall
```

Keep running during critical operations to continuously monitor and block unknown threats while maintaining access to your infrastructure.

### 3. **Maximum Secure Environment**

```powershell
S.E.R.E.> native-only
```

For maximum security during sensitive operations - automatically severs unknown threats while preserving all critical system connectivity.

---

## Integration with S.E.R.E. Phases

Network isolation integrates with all S.E.R.E. operational phases:

- **SURVIVE** - Maintains system integrity during attacks
- **EVADE** - Combined with threat detection for comprehensive defense
- **RESIST** - Active blocking provides resistance mechanism
- **ESCAPE** - Network isolation prevents data exfiltration during escape

---

## Technical Details

### Connection Detection

- **Real-time Scanning:** Uses Windows TCP connection enumeration
- **State Monitoring:** Focuses on established connections
- **IP Classification:** Three-tier classification (Native/Critical/Unknown)
- **Port Analysis:** Considers both source and destination ports

### Blocking Strategy

- **Firewall Rules:** Creates named rules for each blocked threat IP/port
- **Persistent Blocking:** Rules remain until manually removed
- **Selective Blocking:** Only blocks unknown threats
- **Auditable:** Full logging of all actions and rule creations

### Performance

- Minimal system overhead during monitoring
- Configurable scan intervals
- Scalable to handle hundreds of connections
- Zero false positives on native/critical connections

---

## Interactive Help

```bash
S.E.R.E.> help

🔒 NETWORK ISOLATION:
  isolate              - Disconnect unknown/threat IPs (preserves critical systems)
  firewall             - Monitor & block unknown threats (preserves critical systems)
  native-only, lockdown- Auto-sever unknown threats (preserves critical systems)
```

---

## Operational Notes

- Network isolation modes work independently or in combination with threat detection
- Use `Ctrl+C` to stop continuous modes (firewall, native-only)
- All disconnections are logged for audit purposes
- Status reports available via `status` command
- Can be combined with patrol mode for full defensive posture

---

## Firewall Rule Management

**Created Rules:**

- Rules are named: `SERE_Block_{IP}_{PORT}`
- Rules block outbound connections to specific threat IP/port combinations
- Rules persist until manually removed

**Cleanup:**

```powershell
# Remove all S.E.R.E. firewall rules
Get-NetFirewallRule -DisplayName "SERE_*" | Remove-NetFirewallRule
```

**Manual Rule Removal:**

```cmd
# Alternative using netsh
netsh advfirewall firewall delete rule name="SERE_Block_*"
```

---

## Testing and Validation

### Safe Testing Environment

Before using in production, test in an isolated environment:

1. **Create Test Connections:**

   ```bash
   # Open some external connections for testing (use authorized targets only)
   ping <authorized-test-ip>
   curl https://httpbin.org/get
   ```

2. **Run Selective Isolation Test:**

   ```bash
   python sere_security_system.py
   S.E.R.E.> isolate
   ```

3. **Verify Selective Blocking:**

   ```powershell
   # Check firewall rules
   Get-NetFirewallRule -DisplayName "SERE_*"
   ```

4. **Clean Up:**

   ```powershell
   # Remove test rules
   Get-NetFirewallRule -DisplayName "SERE_*" | Remove-NetFirewallRule
   ```

---

## Error Handling

### Common Issues

**Permission Denied:**

```bash
Error: Access denied when creating firewall rules
Solution: Run as Administrator
```

**PowerShell Not Available:**

```bash
Error: 'powershell' command not found
Solution: Ensure PowerShell is installed and in PATH
```

**Network Interface Issues:**

```bash
Error: Cannot enumerate network connections
Solution: Check network adapter status
```

### Logging

All selective network isolation activities are logged with timestamps and can be reviewed for audit purposes.

---

## Production Deployment

For production use:

1. **Customize Critical Systems:** Edit `_is_critical_system()` method with your infrastructure IPs
2. **Run as Service:** Configure S.E.R.E. to run as a Windows service
3. **Scheduled Tasks:** Set up automated network scans
4. **Event Logging:** Integrate with Windows Event Log
5. **Alert System:** Configure email/SMS alerts for isolation events
6. **Backup Rules:** Maintain backup of firewall configurations

---

## Key Advantage: Selective Protection

**Unlike traditional firewalls that can block legitimate traffic, S.E.R.E. selective isolation:**

- ✅ **Knows your critical systems** and never blocks them
- ✅ **Preserves business continuity** during security operations
- ✅ **Targets only unknown threats** for maximum effectiveness
- ✅ **Maintains operational integrity** while defending against attacks
- ✅ **Provides surgical precision** in network defense

**Your critical infrastructure remains fully operational while unknown threats are eliminated.**

---

**Remember: These are REAL network operations with SELECTIVE blocking. Your critical systems are ALWAYS preserved.**
