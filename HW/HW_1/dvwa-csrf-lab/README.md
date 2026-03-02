# DVWA CSRF Lab Docs Index

This folder contains a local **Damn Vulnerable Web Application (DVWA)** lab focused on **Cross-Site Request Forgery (CSRF)**.

Use these guides in order:

1. [walkthrough/README-WALKTHROUGH.md](walkthrough/README-WALKTHROUGH.md) for step-by-step execution, one test at a time.
2. [README-DOCKER-SETUP-AND-TEST.md](README-DOCKER-SETUP-AND-TEST.md) for setup, run, and test flow.
3. [README-CSRF.md](README-CSRF.md) for the security concept.
4. [README-POC.md](README-POC.md) for Proof of Concept (PoC) files and level behavior.
5. [README-DVWA-STRUCTURE.md](README-DVWA-STRUCTURE.md) for DVWA internals relevant to this lab.

## Files

- `compose.yml`: Docker Compose service definition.
- `csrf_poc.html`: Baseline CSRF PoC request.
- `csrf_poc_medium.html`: Medium-level test PoC.
- `csrf_poc_high_missing_token.html`: High-level expected-fail PoC.
- `csrf_poc_high_manual_token.html`: High-level manual token PoC template.
- `csrf_poc_impossible_missing_requirements.html`: Impossible-level expected-fail PoC.
- `csrf_poc_impossible_manual_token.html`: Impossible-level manual token PoC template.

## Safety

- Localhost use only.
- Controlled lab use only.
- Do not use these techniques against systems you do not own or have explicit permission to test.
