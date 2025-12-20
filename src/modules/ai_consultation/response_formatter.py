# src/modules/ai_consultation/response_formatter.py
import textwrap

class ResponseFormatter:
    def __init__(self, platform="web"):
        self.platform = platform

    def format_text(self, text):
        if self.platform == "telegram":
            return f"💬 *AI TradeWise*\n{textwrap.fill(text, 70)}"
        elif self.platform == "web":
            return f"<div class='ai-response'><p>{text}</p></div>"
        else:
            return text

    def format_rich(self, data):
        if self.platform == "web":
            return f"""
            <div class='ai-report'>
                <h3>🧠 AI TradeWise Consultation</h3>
                <p>{data.get('response', '')}</p>
                <small>Confidence: {data.get('confidence', 'N/A')}</small>
            </div>
            """
        return self.format_text(data.get("response", ""))
