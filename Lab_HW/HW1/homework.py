# Lab 1 Homework - Simulate Authentication using bcrypt

import bcrypt
import json
import os

USERS_FILE = "users.json"


def hash_password(plain_password: str) -> str:
    # bcrypt generates a random salt and embeds it into the returned hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def hash_password_verbose(plain_password: str) -> str:
    # same as hash_password but prints each part of the hash so you can see what is happening

    # gensalt returns something like b'$2b$12$<22 base64 chars>'
    salt = bcrypt.gensalt()
    print(f"  [1] Raw salt: {salt}")

    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    hash_str = hashed.decode("utf-8")
    print(f"  [2] Full hash: {hash_str}")

    # bcrypt hash format: $<version>$<cost>$<22 char salt><31 char digest>
    parts = hash_str.split("$")
    version = parts[1]
    cost = parts[2]
    salt_and_digest = parts[3]
    embedded_salt = salt_and_digest[:22]
    digest = salt_and_digest[22:]

    print(f"  [3] Algorithm: ${version}$")
    print(f"  [4] Cost factor: {cost}  (2^{cost} = {2**int(cost)} iterations)")
    print(f"  [5] Embedded salt: {embedded_salt}  (22 chars, base64)")
    print(f"  [6] Digest: {digest}  (31 chars, base64)")
    print(f"  [7] checkpw() re-extracts the salt from the hash to verify")

    return hash_str


def load_users() -> dict:
    # returns empty dict if the file does not exist yet
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user(username: str, plain_password: str) -> None:
    users = load_users()
    if username in users:
        print(f"[!] User '{username}' already exists - skipping registration.")
        return
    users[username] = hash_password(plain_password)
    save_users(users)
    print(f"[+] User '{username}' registered successfully.")


def authenticate(username: str, plain_password: str) -> None:
    # checkpw re-hashes the input using the salt embedded in stored_hash
    users = load_users()

    if username not in users:
        print(f"[!] User '{username}' not found.")
        return

    stored_hash = users[username].encode("utf-8")
    if bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash):
        print(f"[OK] '{username}' -> AUTHENTICATED")
    else:
        print(f"[FAIL] '{username}' -> INVALID PASSWORD")


if __name__ == "__main__":

    print("=== Verbose salting walkthrough ===")
    hash_password_verbose("hunter2")
    print()

    print("=== Registering users ===")
    register_user("alice",   "SuperSecret42!")
    register_user("bob",     "hunter2")
    register_user("charlie", "C0mplex#Pass")
    print()

    print("=== Correct passwords ===")
    authenticate("alice",   "SuperSecret42!")
    authenticate("bob",     "hunter2")
    authenticate("charlie", "C0mplex#Pass")
    print()

    print("=== Wrong passwords ===")
    authenticate("alice",   "wrongpassword")
    authenticate("bob",     "Hunter2")
    authenticate("charlie", "C0mplex#Pass ")
    print()

    print("=== Non-existent user ===")
    authenticate("dave", "doesntmatter")
