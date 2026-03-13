"""
Lab 1 Homework - Simulate Authentication using bcrypt

Steps:
1. Hash a password string with a salt (bcrypt handles salt internally)
2. Store users (username + hashed password) in a JSON file
3. Authenticate a user by comparing their input against the stored hash
"""

import bcrypt
import json
import os

USERS_FILE = "users.json"


# --- 1. Hash a password with a bcrypt salt ---

def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    bcrypt generates and embeds a random salt inside the hash automatically,
    so the salt does not need to be stored separately.
    Returns the hash as a UTF-8 string suitable for JSON storage.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def hash_password_verbose(plain_password: str) -> str:
    """
    Same as hash_password but prints each step so you can see what bcrypt
    is doing under the hood.

    A bcrypt hash string looks like this:
        $2b$12$<22 chars of salt><31 chars of digest>

    Fields:
        $2b$   - algorithm version (2b is the current standard)
        12     - cost factor (2^12 = 4096 rounds of hashing)
        next 22 chars - the salt, base64-encoded by bcrypt
        last 31 chars - the actual password digest

    The salt and digest are both stored together in one string,
    which is why bcrypt.checkpw() does not need the salt passed separately.
    """
    # Step 1: generate a random salt.
    # gensalt() returns a 29-byte prefix like b'$2b$12$<22 base64 chars>'
    # which bcrypt uses both as the salt input and as the prefix of the final hash.
    salt = bcrypt.gensalt()

    print(f"  [1] Raw salt bytes  : {salt}")

    # Step 2: hash the password with that salt.
    # bcrypt internally: encodes the password, runs the Blowfish key schedule
    # using the salt to initialise it, then iterates 2^cost times.
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    hash_str = hashed.decode("utf-8")

    print(f"  [2] Full hash string: {hash_str}")

    # Step 3: break the hash string into its three parts.
    # Format: $<version>$<cost>$<22-char salt><31-char digest>
    # The first 29 characters are always the prefix (version + cost + salt).
    parts = hash_str.split("$")  # ['', '2b', '12', '<salt+digest>']
    version   = parts[1]         # '2b'
    cost      = parts[2]         # '12'
    salt_and_digest = parts[3]   # 53 chars total
    embedded_salt  = salt_and_digest[:22]  # first 22 chars = salt
    digest         = salt_and_digest[22:]  # remaining 31 chars = hash

    print(f"  [3] Algorithm       : ${version}$")
    print(f"  [4] Cost factor     : {cost}  (2^{cost} = {2**int(cost)} iterations)")
    print(f"  [5] Embedded salt   : {embedded_salt}  (base64, 22 chars)")
    print(f"  [6] Digest          : {digest}  (base64, 31 chars)")
    print(f"  [7] To verify later : bcrypt.checkpw() re-extracts the salt from")
    print(f"      the stored hash and re-hashes the candidate password with it.")

    return hash_str


# --- 2. Store users in a JSON file ---

def load_users() -> dict:
    """Load the user database from the JSON file. Returns {} if the file is missing."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users: dict) -> None:
    """Persist the user database back to the JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user(username: str, plain_password: str) -> None:
    """Register a new user by storing their username and hashed password."""
    users = load_users()
    if username in users:
        print(f"[!] User '{username}' already exists - skipping registration.")
        return
    users[username] = hash_password(plain_password)
    save_users(users)
    print(f"[+] User '{username}' registered successfully.")


# --- 3. Authenticate - compare input password against stored hash ---

def authenticate(username: str, plain_password: str) -> None:
    """
    Compare the provided plain-text password against the stored bcrypt hash.
    Prints AUTHENTICATED or INVALID PASSWORD accordingly.
    """
    users = load_users()

    if username not in users:
        print(f"[!] User '{username}' not found.")
        return

    stored_hash = users[username].encode("utf-8")
    if bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash):
        print(f"[OK] '{username}' -> AUTHENTICATED")
    else:
        print(f"[FAIL] '{username}' -> INVALID PASSWORD")


# --- Demo / entry point ---

if __name__ == "__main__":

    print("=== Verbose salting walkthrough ===")
    print(f"Hashing password: 'hunter2'")
    hash_password_verbose("hunter2")
    print()

    print("=== Registering users ===")
    register_user("alice",   "SuperSecret42!")
    register_user("bob",     "hunter2")
    register_user("charlie", "C0mplex#Pass")

    print()

    print("=== Authentication attempts (correct passwords) ===")
    authenticate("alice",   "SuperSecret42!")
    authenticate("bob",     "hunter2")
    authenticate("charlie", "C0mplex#Pass")

    print()

    print("=== Authentication attempts (wrong passwords) ===")
    authenticate("alice",   "wrongpassword")
    authenticate("bob",     "Hunter2")         # bcrypt is case-sensitive
    authenticate("charlie", "C0mplex#Pass ")   # trailing space matters

    print()

    print("=== Non-existent user ===")
    authenticate("dave", "doesntmatter")
