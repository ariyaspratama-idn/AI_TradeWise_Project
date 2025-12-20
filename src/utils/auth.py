import json, os, jwt, hashlib
from datetime import datetime, timedelta
from src.utils.config import settings
from src.utils.logger import logger

USERS_FILE = "src/data/users.json"

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def read_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def write_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def create_default_admin():
    users = read_users()
    if not any(u["email"] == settings.DEFAULT_ADMIN_EMAIL for u in users):
        admin_user = {
            "email": settings.DEFAULT_ADMIN_EMAIL,
            "password": hash_password(settings.DEFAULT_ADMIN_PASSWORD),
            "role": "admin",
            "created_at": str(datetime.utcnow())
        }
        users.append(admin_user)
        write_users(users)
        logger.info("Admin default dibuat otomatis")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_user(email: str, password: str):
    users = read_users()
    for u in users:
        if u["email"] == email and u["password"] == hash_password(password):
            return u
    return None

def register_user(email: str, password: str):
    users = read_users()
    if any(u["email"] == email for u in users):
        return False
    new_user = {
        "email": email,
        "password": hash_password(password),
        "role": "user",
        "created_at": str(datetime.utcnow())
    }
    users.append(new_user)
    write_users(users)
    return True
