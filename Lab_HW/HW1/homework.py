import bcrypt
import json
import os

USERS_FILE = "users.json"


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def authenticate(username: str, plain_password: str) -> None:
    users = load_users()

    if username not in users:
        print(f"{username}: not found")
        return

    stored_hash = users[username].encode("utf-8")
    if bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash):
        print(f"{username}: ok")
    else:
        print(f"{username}: failed")


if __name__ == "__main__":

    users = load_users()
    users["alice"]   = hash_password("SuperSecret42!")
    users["bob"]     = hash_password("hunter2")
    users["charlie"] = hash_password("C0mplex#Pass")
    save_users(users)
    print()

    authenticate("alice",   "SuperSecret42!")
    authenticate("bob",     "hunter2")
    authenticate("charlie", "C0mplex#Pass")
    print()

    authenticate("alice",   "wrongpassword")
    authenticate("bob",     "Hunter2")
    authenticate("charlie", "C0mplex#Pass ")
    print()

    authenticate("dave", "doesntmatter")
