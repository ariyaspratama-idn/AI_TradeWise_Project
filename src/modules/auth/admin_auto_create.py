# src/modules/auth/admin_auto_create.py
import os
import json
import hashlib

class AdminAutoCreator:
    def __init__(self, data_path="data/users.json"):
        self.data_path = data_path
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w") as f:
                json.dump([], f)

    def create_default_admin(self):
        with open(self.data_path, "r") as f:
            users = json.load(f)

        if any(u["role"] == "admin" for u in users):
            return {"status": True, "msg": "Admin already exists."}

        default_admin = {
            "username": "admin",
            "password": hashlib.sha256("admin123".encode()).hexdigest(),
            "role": "admin",
            "email": "admin@aitradewise.local",
            "created_at": "auto"
        }
        users.append(default_admin)
        with open(self.data_path, "w") as f:
            json.dump(users, f, indent=4)

        return {"status": True, "msg": "Default admin created (admin / admin123)."}
