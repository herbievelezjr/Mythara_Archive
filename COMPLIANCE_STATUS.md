# Mythara Compliance Status — Single Source of Truth

> **Read this before writing any compliance claim in this repo.**
> Every document, bot, widget, and sales page must agree with this file.
> If it contradicts this file, this file wins.

## What is implemented (controls mapped)

- Soul Cradle governance: standing matrix, membrane authorization, will-checked decisions, integrity-hashed judgments.
- HIPAA Security Rule (45 CFR 164 Subpart C): technical, administrative, and physical safeguard controls mapped — see `Legal/Compliance/International/Multi_Jurisdiction_Matrix.md`.
- FDA 21 CFR Part 11: electronic records and signature rule tables versioned — see `soul_cradle/health.py`.
- SOC 2 Type II and ISO 27001: controls implemented per the governance docs.
- Internal medical-AI governance checklist: Herb's own framework, labeled as such.

## What is NOT claimed

- **No independent audit has been completed.** Not SOC 2, not ISO 27001, not HIPAA, not GDPR, not FedRAMP, not CMMC, not ITAR.
- **No certification is claimed.** Compliance products are sold as **readiness assessments** — mapping controls against a framework — never as certification.
- **DrMythara is not a medical professional.** Compliance guidance only; never medical advice.
- **No indemnification is offered.** No insurance backs this software. See LICENSE.md.
- **No entity exists.** Mythara Labs LLC is planned, not formed; the Soul Cradle Foundation does not exist. Licenses are granted by Herbert Velez Jr. personally. An unsigned IP-assignment draft is held at `Legal/IP_Assignment_Agreement.md` for formation day.

## Rules for claims

1. Say **"readiness"**, never **"certified"** — unless an actual audit certificate exists, in which case update this file first.
2. Never fabricate customers, pilots, metrics, testimonials, or outcomes. Fictional examples must be labeled fictional.
3. Every compliance judgment must cite the rule version it was evaluated under.
4. `soul_cradle/will.py` enforces Herb's forbidden-claim patterns on VP Marketing output automatically.

*Last updated 2026-09-22. This is a project status document, not legal advice.*
