# src/modules/ai_consultation/__init__.py
"""
Modul Konsultasi AI untuk TradeWise Project
Fungsi utama:
- AI Brain → inti kecerdasan percakapan
- ContextMemory → menyimpan konteks user
- ResponseFormatter → membungkus jawaban agar lebih alami
- AIConsultationManager → mengelola sesi percakapan dan integrasi AI model
"""

from .ai_brain import AIBrain
from .context_memory import ContextMemory
from .response_formatter import ResponseFormatter
from .ai_consultation_manager import AIConsultationManager
