# ------------------------------------------------------------
# Author: Linpeng Mao
# Description: User authentication module (login & registration).
# ------------------------------------------------------------

import storage

USERS_FILE = "users.json"


def load_users():
    """Load all user accounts from storage."""
    return storage.load_json(USERS_FILE, default={})


def save_users(users):
    """Save all user accounts back to storage."""
    storage.save_json(USERS_FILE, users)


def check_login(username, password):
    """Verify whether username/password is valid."""
    if not username or not password:
        return False
    users = load_users()
    return username in users and users[username]["password"] == password


def register_user(username, password):
    """
    Register a new user.
    Return (success: bool, message: str).
    """
    if not username or not password:
        return False, "Username and password cannot be empty."

    users = load_users()
    if username in users:
        return False, "Username already exists."

    users[username] = {"password": password}
    save_users(users)
    return True, "User registered successfully."
