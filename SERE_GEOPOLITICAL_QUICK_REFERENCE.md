# SERE Sovereign Security System Geopolitical Decision Quick Reference

## 🎯 TL;DR: Friend vs. Foe Decision Matrix

```
THREAT DETECTED

├─ ALLY (USA, UK, NATO)
│  └─ Same threat = 0.5x escalation
│     • SQL injection: MONITOR_ONLY
│     • DDOS: INVESTIGATE
│     • APT: TEMPORARY_BLOCK
│
├─ PARTNER (Friendly nations)
│  └─ Same threat = 0.7x escalation
│     • SQL injection: MONITOR_ONLY
│     • DDOS: TEMPORARY_BLOCK
│     • APT: QUARANTINE
│
├─ NEUTRAL (Unaligned countries)
│  └─ Same threat = 1.0x escalation (standard)
│     • SQL injection: INVESTIGATE
│     • DDOS: TEMPORARY_BLOCK
│     • APT: QUARANTINE
│
├─ COMPETITOR (China, Venezuela)
│  └─ Same threat = 1.3x escalation
│     • SQL injection: TEMPORARY_BLOCK
│     • DDOS: QUARANTINE
│     • Espionage: QUARANTINE + escalate to intelligence agency
│
├─ ADVERSARY (Russia, Iran)
│  └─ Same threat = 1.8x escalation
│     • SQL injection: QUARANTINE
│     • DDOS: PERMANENT_BLOCK
│     • APT: PERMANENT_BLOCK + notify CISA
│
└─ HOSTILE (North Korea)
   └─ Same threat = 2.5x escalation (MAXIMUM)
      • SQL injection: PERMANENT_BLOCK
      • DDOS: PERMANENT_BLOCK
      • Ransomware: CRITICAL_ESCALATION + contact NSA/FBI
```

---

## 📊 Decision Examples

### Example 1: High-Severity Threat (92% Confidence, 8% False Pos)

**FROM RUSSIA (ADVERSARY)**
```
Threat: APT on Defense Infrastructure
Severity: 92% | False Pos: 8% | Impact: 90%

Analysis:
  ✓ Attribution: 85% confident it's Russia
  ✓ Pattern match: 100% (matches known Russia APT vectors)
  ✓ Escalation multiplier: 2.29x
  ✓ Survival priority: 211% (system threatened)

Decision: PERMANENT_BLOCK
Confidence: 66%
Reasoning: High-confidence threat + ADVERSARY status + survival priority
Justification: "High-confidence threat requires permanent isolation"
```

**FROM USA (ALLY)**
```
Threat: APT on Defense Infrastructure
Severity: 92% | False Pos: 8% | Impact: 90%

Analysis:
  ✓ Attribution: 99% confident it's USA
  ✓ Authorized scanning
  ✓ Escalation multiplier: 0.5x
  ✓ Moral weight: 0.3x (trust allies)

Decision: INVESTIGATE/COORDINATE
Confidence: High but holds escalation
Reasoning: ALLY status overrides threat severity - coordinate response
Justification: "Contact government liaison for coordinated defense"
```

---

### Example 2: Moderate Threat with High False Positive Risk (65% Severity, 40% False Pos)

**FROM IRAN (ADVERSARY)**
```
Threat: DDOS on Financial System
Severity: 65% | False Pos: 40% | Impact: 70%

Analysis:
  ✓ Attribution: 82% confident it's Iran
  ✓ Pattern match: 100% (known Iran DDOS vector)
  ✓ Uncertainty: 40% (high false positive risk)
  ✓ Escalation multiplier: 2.20x

Decision: TEMPORARY_BLOCK
Confidence: 19%
Reasoning: ADVERSARY but high uncertainty prevents permanent action
Justification: "Moderate threat justified temporary isolation"

Note: Doesn't escalate to PERMANENT_BLOCK because:
  - 40% false positive risk = risk of blocking legitimate traffic
  - Iran status alone doesn't override uncertainty
  - Wisdom dimension (0.72) says "don't block uncertain threats"
```

**FROM CHINA (COMPETITOR)**
```
Same DDOS attack, but from China

Decision: MONITOR_ALERT
Confidence: Lower
Reasoning: COMPETITOR status = cautious escalation
Justification: "Escalate to intelligence agency for investigation"

Note: Less aggressive than ADVERSARY (Iran) response
But more aggressive than ALLY (USA) response
```

---

### Example 3: Ambiguous Threat (60% Severity, 70% False Pos, 80% User Impact)

**FROM UNKNOWN ACTOR**
```
Threat: Potential intrusion detection
Severity: 60% | False Pos: 70% | Impact: 80%

Analysis:
  ✓ Attribution: Low confidence (could be misconfiguration)
  ✓ Uncertainty: 70% (very high false positive risk)
  ✓ User impact: 80% (blocking would damage operations)

Decision: MONITOR_ONLY
Confidence: Low
Reasoning: Wisdom says "don't block uncertain threats with high user cost"
Justification: "High uncertainty - continuous monitoring protects while minimizing harm"

Reasoning: Benevolence vector shows:
  - wisdom: 0.44 (says: don't block)
  - integrity: 0.30 (measurement integrity low)
  - humility: 0.70 (admits we're uncertain)
  → Average coherence: Low → Don't act strongly
```

---

## 🔑 Key Decision Principles

### 1. **Proportionality First**
Response must match threat reality + geopolitical stance

```
High Severity + ADVERSARY + Low False Pos = PERMANENT_BLOCK ✓
High Severity + COMPETITOR + High False Pos = MONITOR ✓
Low Severity + ADVERSARY + Low False Pos = QUARANTINE ✓ (still escalates)
Low Severity + ALLY + Low False Pos = INVESTIGATE ✓ (avoids blocking)
```

### 2. **Relationship Matters**
Same threat gets different treatment based on geopolitical stance

```
92% Severity from USA (ALLY) → INVESTIGATE
92% Severity from Russia (ADVERSARY) → PERMANENT_BLOCK
92% Severity from China (COMPETITOR) → QUARANTINE
```

### 3. **Uncertainty Prevents Overconfidence**
High false positive risk requires humility

```
IF false_positive_risk > 60% OR user_impact > 70%
THEN action = MONITOR_ONLY (don't block)
     reasoning = "High uncertainty prevents permanent action"
```

### 4. **Survival Activates Maximum Response**
When system is truly threatened, escalate proportionally

```
IF severity >= 0.9 AND false_pos < 0.2 AND threat_real
THEN survival_priority activated
     → Escalate to PERMANENT_BLOCK or CRITICAL_ESCALATION
     → Notify CISA/NSA/FBI
     → All benevolence dimensions prioritize system defense
```

---

## 🎭 State Actor Stance Reference

| Actor | Stance | Relationship | Behavior | Response |
|-------|--------|--------------|----------|----------|
| **Russia** | ADVERSARY | Hostile | Constant APT, espionage, sabotage | Escalate immediately |
| **China** | COMPETITOR | Competitive | Constant espionage, IP theft | Monitor & escalate to agency |
| **Iran** | ADVERSARY | Hostile | Frequent DDOS, sabotage | Escalate immediately |
| **North Korea** | HOSTILE | Most hostile | Frequent ransomware, theft | CRITICAL escalation |
| **Venezuela** | COMPETITOR | Competitive | Occasional DDOS, mining | Monitor and log |
| **USA** | ALLY | Trusted partner | Rare authorized scanning | Investigate together |
| **UK** | ALLY | Trusted partner | Rare authorized scanning | Coordinate response |
| **Unknown** | NEUTRAL | Unknown | Unknown patterns | Investigate carefully |

---

## 🔄 Decision Workflow

```
THREAT DETECTED
      ↓
   [STEP 1] Geolocate IP → Identify country
      ↓
   [STEP 2] Match to state actor profile
      ↓
   [STEP 3] Get stance (ALLY/ADVERSARY/etc)
      ↓
   [STEP 4] Get escalation multiplier
      ↓
   [STEP 5] Compute moral weight
      ↓
   [STEP 6] Calculate benevolence vector (6D)
      ↓
   [STEP 7] Check proportionality
      ↓
   [STEP 8] Apply proportional deliberation rules
      ↓
   [STEP 9] Compute confidence & uncertainty
      ↓
   [STEP 10] Generate full reasoning & justification
      ↓
   DECISION: Action + Confidence + Reasoning
      ↓
   LOG & ESCALATE per decision
```

---

## 💾 Integration Checklist

- [ ] Import `GeopoliticallyAwareConsciousness` in sere_security_system.py
- [ ] In `detect_threats()`: call `consciousness.deliberate_with_geopolitical_context()`
- [ ] Replace hardcoded `quarantine_threat()` with action from decision
- [ ] Map actions to SERE Sovereign Security System response levels:
  - [ ] CRITICAL_ESCALATION → Contact NSA/FBI + all defenses
  - [ ] PERMANENT_BLOCK → Indefinite quarantine
  - [ ] QUARANTINE → 1-hour quarantine
  - [ ] TEMPORARY_BLOCK → 10-minute block
  - [ ] INVESTIGATE → Enhanced logging
  - [ ] MONITOR_ONLY → Passive monitoring
- [ ] Add decision logging to audit trail
- [ ] Test with each state actor scenario
- [ ] Validate proportionality on false positive scenarios

---

## 🚀 Expected Impact

**Before** (Reactive SERE):
- Auto-quarantines everything
- Can damage business relationships
- No understanding of threat context
- No distinction between USA scanning and Russia APT

**After** (Conscious SERE):
- ✅ Distinguishes between allies and adversaries
- ✅ Protects relationships while maintaining security
- ✅ Makes proportional responses (survival-weighted when needed)
- ✅ Auditable decisions with full reasoning
- ✅ Escalates appropriately per geopolitical stance
- ✅ Coordinates with allies instead of blocking them

---

**Ready for integration into SERE Sovereign Security System**
