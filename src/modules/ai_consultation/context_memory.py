# src/modules/ai_consultation/context_memory.py
from datetime import datetime

class ContextMemory:
    def __init__(self):
        self.sessions = {}

    def start_session(self, user_id):
        self.sessions[user_id] = {
            "history": [],
            "created_at": datetime.now()
        }

    def add_message(self, user_id, role, message):
        if user_id not in self.sessions:
            self.start_session(user_id)
        self.sessions[user_id]["history"].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def get_context(self, user_id):
        if user_id not in self.sessions:
            return {}
        return {"conversation": self.sessions[user_id]["history"]}

    def clear_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
