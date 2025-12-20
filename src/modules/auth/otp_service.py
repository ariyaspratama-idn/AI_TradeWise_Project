# src/modules/auth/otp_service.py
import random
import time
import json
import os
from datetime import datetime, timedelta

class OTPService:
    def __init__(self, storage_path="data/otp.json", expiry_minutes=5):
        self.storage_path = storage_path
        self.expiry_minutes = expiry_minutes
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump({}, f)

    def _load_otp_data(self):
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _save_otp_data(self, data):
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=4)

    def generate_otp(self, user_id):
        otp = str(random.randint(100000, 999999))
        expiry_time = (datetime.now() + timedelta(minutes=self.expiry_minutes)).strftime("%Y-%m-%d %H:%M:%S")
        otp_data = self._load_otp_data()
        otp_data[user_id] = {"otp": otp, "expires": expiry_time}
        self._save_otp_data(otp_data)
        return otp

    def verify_otp(self, user_id, otp_input):
        otp_data = self._load_otp_data()
        if user_id not in otp_data:
            return {"status": False, "msg": "No OTP found."}

        record = otp_data[user_id]
        if datetime.now() > datetime.strptime(record["expires"], "%Y-%m-%d %H:%M:%S"):
            del otp_data[user_id]
            self._save_otp_data(otp_data)
            return {"status": False, "msg": "OTP expired."}

        if record["otp"] == otp_input:
            del otp_data[user_id]
            self._save_otp_data(otp_data)
            return {"status": True, "msg": "OTP verified successfully."}

        return {"status": False, "msg": "Invalid OTP."}
