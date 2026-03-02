# DVWA CSRF Lab Documentation Index

This folder contains a local lab for **Damn Vulnerable Web Application (DVWA)** and **Cross-Site Request Forgery (CSRF)**.

## Which README to Use

- [README-DOCKER-SETUP-AND-TEST.md](README-DOCKER-SETUP-AND-TEST.md)
Purpose: environment setup, container start/stop, port checks, database initialization.
Use it when: you need to boot the lab or reset it.

- [walkthrough/README-WALKTHROUGH.md](walkthrough/README-WALKTHROUGH.md)
Purpose: run tests one by one in execution order.
Use it when: you want a complete manual run from start to cleanup.

- [README-CSRF.md](README-CSRF.md)
Purpose: explain CSRF mechanics and why each DVWA security level behaves differently.
Use it when: you need theory and level-specific security analysis.

- [README-POC.md](README-POC.md)
Purpose: explain what each Proof of Concept (PoC) file does and what result to expect.
Use it when: you are choosing or editing a PoC file.

- [README-DVWA-STRUCTURE.md](README-DVWA-STRUCTURE.md)
Purpose: explain relevant DVWA source files and request flow (`setup.php`, CSRF module files).
Use it when: you need implementation details from the project structure.

## Safety Scope

- localhost only
- controlled educational environment only
- no real target testing
