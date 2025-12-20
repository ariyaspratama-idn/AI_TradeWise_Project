# src/modules/ai_consultation/ai_brain.py
from ..multi_model import MultiAIModel

class AIBrain:
    def __init__(self, signal_service=None):
        self.signal_service = signal_service
        self.multi_ai = MultiAIModel()

    def analyze_question(self, question: str) -> str:
        q = question.lower()
        if "harga" in q and "bitcoin" in q:
            return "price_request"
        elif "beli" in q or "jual" in q:
            return "trading_advice"
        elif "sentimen" in q:
            return "sentiment_request"
        elif "rekomendasi" in q or "saran" in q:
            return "recommendation"
        else:
            return "general"

    def consult(self, question: str, context: dict = None):
        intent = self.analyze_question(question)
        context = context or {}
        
        # Construct enhanced prompt based on intent
        if intent == "price_request":
            prompt = f"User bertanya tentang harga Bitcoin. Data pasar saat ini: {context.get('market_data', 'Tidak tersedia')}. Berikan analisis singkat."
        elif intent == "trading_advice":
            prompt = f"User meminta saran trading. Sinyal sistem: {context.get('signal_data', 'Netral')}. Sentimen: {context.get('sentiment', 'Netral')}. Berikan saran hati-hati."
        elif intent == "sentiment_request":
            prompt = f"Jelaskan sentimen pasar berdasarkan data ini: {context.get('sentiment', 'Netral')}."
        elif intent == "recommendation":
            prompt = f"Berikan rekomendasi investasi berdasarkan sinyal: {context.get('signal_data', 'Netral')}."
        else:
            prompt = question

        # Delegate to Multi-Model AI
        # User could specify model in context, default to gpt-4o
        model = context.get("preferred_model", "gpt-4o")
        return self.multi_ai.generate_response(prompt, context, model_name=model)
