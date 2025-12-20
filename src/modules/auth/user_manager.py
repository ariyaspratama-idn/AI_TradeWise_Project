# src/modules/auth/user_manager.py
import json
import os
import hashlib
from datetime import datetime

class UserManager:
    def __init__(self, data_path="data/users.json"):
        self.data_path = data_path
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w") as f:
                json.dump([], f, indent=4)

    def _load_users(self):
        with open(self.data_path, "r") as f:
            return json.load(f)

    def _save_users(self, users):
        with open(self.data_path, "w") as f:
            json.dump(users, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, role="user", email=None):
        users = self._load_users()
        if any(u["username"] == username for u in users):
            return {"status": False, "msg": "Username already exists."}

        user_data = {
            "username": username,
            "password": self.hash_password(password),
            "role": role,
            "email": email,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": None
        }

        users.append(user_data)
        self._save_users(users)
        return {"status": True, "msg": f"User '{username}' registered successfully."}

    def verify_login(self, username, password):
        users = self._load_users()
        hashed = self.hash_password(password)
        for u in users:
            if u["username"] == username and u["password"] == hashed:
                u["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_users(users)
                return {"status": True, "user": u}
        return {"status": False, "msg": "Invalid username or password."}

    def list_users(self):
        return self._load_users()

    def delete_user(self, username):
        users = self._load_users()
        new_users = [u for u in users if u["username"] != username]
        self._save_users(new_users)
        return {"status": True, "msg": f"User '{username}' deleted."}