# src/modules/ai_consultation/ai_consultation_manager.py
from .ai_brain import AIBrain
from .context_memory import ContextMemory
from .response_formatter import ResponseFormatter

class AIConsultationManager:
    def __init__(self, platform="web", signal_service=None):
        self.brain = AIBrain(signal_service)
        self.memory = ContextMemory()
        self.formatter = ResponseFormatter(platform)

    def handle_user_query(self, user_id, message, context=None):
        # simpan pesan user
        self.memory.add_message(user_id, "user", message)

        # proses konsultasi AI
        response_text = self.brain.consult(message, context or {})

        # simpan jawaban
        self.memory.add_message(user_id, "ai", response_text)

        # format hasil
        formatted = self.formatter.format_text(response_text)
        return {
            "user_id": user_id,
            "response": response_text,
            "formatted": formatted,
            "context": self.memory.get_context(user_id)
        }
