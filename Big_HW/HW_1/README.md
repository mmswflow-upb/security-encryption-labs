# DVWA CSRF Lab Documentation Index

This folder contains a local lab for **Damn Vulnerable Web Application (DVWA)** and **Cross-Site Request Forgery (CSRF)**.

## Submodule

DVWA source code is included as a Git submodule at `dvwa-source/` (official repo: digininja/DVWA).
The lab uses the original `dvwa-source/compose.yml` to pull the pre-built DVWA image.

After cloning, initialize the submodule:

```bash
git submodule update --init
```

## Which README to Use

- [docs/README-DOCKER-SETUP-AND-TEST.md](docs/README-DOCKER-SETUP-AND-TEST.md)
Purpose: environment setup, container start/stop, port checks, database initialization.
Use it when: you need to boot the lab or reset it.

- [walkthrough/README-WALKTHROUGH.md](walkthrough/README-WALKTHROUGH.md)
Purpose: run tests one by one in execution order.
Use it when: you want a complete manual run from start to cleanup.

- [docs/README-CSRF.md](docs/README-CSRF.md)
Purpose: explain CSRF mechanics and why each DVWA security level behaves differently.
Use it when: you need theory and level-specific security analysis.

- [proof-of-concept/](proof-of-concept/)
Purpose: PoC files organized by level (`low`, `medium`, `high`, `impossible`), each with its own `README.md` covering goal, security level behavior, run instructions, and expected results.
Use it when: you are running or editing a PoC file.

- [docs/README-DVWA-STRUCTURE.md](docs/README-DVWA-STRUCTURE.md)
Purpose: explain relevant DVWA source files and request flow (`setup.php`, CSRF module files).
Use it when: you need implementation details from the project structure.

## Safety Scope

- localhost only
- controlled educational environment only
- no real target testing
