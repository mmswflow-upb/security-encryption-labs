# CLAUDE.md - DVWA CSRF Lab

A local web security lab using Damn Vulnerable Web Application (DVWA) to study Cross-Site Request Forgery (CSRF). Runs via Docker Compose.

## Setup

DVWA source is included as a Git submodule. After cloning, initialize it:

```bash
git submodule update --init
```

Start the lab environment using the original DVWA compose file:

```bash
docker compose -f dvwa-source/compose.yml up -d
```

The app is accessible at `http://localhost:4280`.

## Documentation

- `docs/README-DOCKER-SETUP-AND-TEST.md` - Environment setup, starting/stopping containers, database init
- `docs/README-CSRF.md` - CSRF theory and per-security-level analysis
- `docs/README-DVWA-STRUCTURE.md` - Relevant DVWA source files and request flow
- `walkthrough/README-WALKTHROUGH.md` - Step-by-step manual test run
- `proof-of-concept/` - PoC HTML files organized by DVWA security level (`low`, `medium`, `high`, `impossible`)

## Safety Scope

localhost only, controlled educational environment only. Do not test against real targets.

## Notes for the AI Assistant

- This lab uses the original `dvwa-source/compose.yml` from the DVWA repo. Do not create a separate compose file.
- All docker compose commands should use `-f dvwa-source/compose.yml`.
- DVWA runs on port `4280` (localhost only).
- Do not add emoji or non-ASCII characters to files in this folder.
- Keep comments plain and simple. Use `# plain sentence` style. No decorative borders, section lines, or fancy layouts.
