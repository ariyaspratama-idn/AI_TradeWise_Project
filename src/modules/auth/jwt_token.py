# src/modules/auth/jwt_token.py
import jwt
from datetime import datetime, timedelta

class JWTHandler:
    def __init__(self, secret_key="supersecret", algorithm="HS256", expiry_minutes=60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiry_minutes = expiry_minutes

    def create_token(self, username, role):
        payload = {
            "username": username,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=self.expiry_minutes),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token):
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return {"status": True, "data": decoded}
        except jwt.ExpiredSignatureError:
            return {"status": False, "msg": "Token expired."}
        except jwt.InvalidTokenError:
            return {"status": False, "msg": "Invalid token."}
