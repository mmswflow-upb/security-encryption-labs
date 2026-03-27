# CLAUDE.md - Security and Encryption Labs

Repository for the Security and Encryption course at UNSTPB FILS, Year IV, Semester II.

## Repository Structure

```
security-encryption-labs/
    Labs/
        Lab_1/          - Hashing vs Encryption concepts, bcrypt authentication homework
    HW/
        HW_1/           - DVWA CSRF lab (Docker-based)
```

## Python Environment

All Python scripts in this repo use the `sec-labs` conda environment.

Activate it before running any script:

```bash
conda activate sec-labs
```

Install a new package into it:

```bash
conda run -n sec-labs pip install <package>
```

## Labs

### Lab_1 - Hashing vs Encryption

**Location:** `Labs/Lab_1/`

**Topics covered:**
- Difference between hashing and encryption
- Why passwords are hashed (not encrypted) for storage
- Salting to prevent rainbow table attacks

**Files:**
- `main.py` - Basic SHA-256 hashing demo using the standard library `hashlib`
- `homework.py` - Homework solution: bcrypt-based password hashing and authentication simulation
- `hashes.txt` - Output file from `main.py` containing raw SHA-256 hashes
- `users.json` - Output file from `homework.py` containing usernames and bcrypt hashes (generated at runtime)

**Run the homework:**

```bash
conda run -n sec-labs python Labs/Lab_1/homework.py
```

**Key concepts in `homework.py`:**
- `bcrypt.gensalt()` generates a random salt per password
- The salt is embedded inside the bcrypt hash string, so it does not need separate storage
- `bcrypt.checkpw()` handles extracting the salt and re-hashing internally during comparison
- Passwords are case-sensitive and whitespace-sensitive


## Notes for the AI Assistant

- Python scripts belong to the `sec-labs` conda environment. Use `conda run -n sec-labs python <script>` to run them.
- Do not use `pip install` directly; always scope package installs to the conda environment.
- Do not add emoji or non-ASCII characters to Python files or markdown files in this repo.
- `users.json` and `hashes.txt` are runtime-generated output files; they are gitignored and should not be committed.
- Keep comments plain and simple. Use `# plain sentence` style. No decorative borders, section lines, or fancy layouts.
