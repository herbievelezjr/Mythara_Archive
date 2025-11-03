# GitHub Copilot Instructions for Mythara Engine

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

---

## Project Context

This is a **proprietary, private repository** for the Mythara Engine - a symbolic safety integrity protocol (SSIP) orchestration system with FastAPI implementation.

---

## Code Standards

### Copyright Headers

**ALL new files must include this header:**

```python
# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.
```

For markdown files:
```markdown
**Copyright © 2025 Herbert Velez Jr. All rights reserved.**  
**Proprietary and Confidential.**
```

---

## Architecture Patterns

### API Endpoints
- Follow REST conventions
- Use Bearer token authentication
- Return integrity hashes with responses
- Include SSIP compliance metrics

### Clause Invocation
- Emotional fidelity calculations required
- Blessings reservoir updates on each invocation
- Fallback to Shadow_Resolver on errors
- Generate unique invocation IDs

### Security
- Never hardcode production API keys
- Use environment variables for secrets
- Validate all inputs with Pydantic models
- Log all invocations with timestamps

---

## File Organization

```
core/source_proprietary/  # API implementation
tests/                    # Validation suite
docs/                     # Documentation
Legal/Compliance/         # Regulatory docs
```

---

## Dependencies

- Python 3.11+
- FastAPI 0.104+
- Pydantic 2.5+
- All dependencies pinned in requirements files

---

## Licensing

This is **proprietary software**. Do not suggest:
- Open source licenses
- Public distribution methods
- Removing copyright headers
- Weakening authentication

---

## Suggestions Welcome For

✅ Performance optimizations  
✅ Security hardening  
✅ SSIP compliance improvements  
✅ Error handling  
✅ Test coverage  
✅ Documentation clarity

---

**Remember: This is a private, NDA-protected codebase for enterprise licensing.**
