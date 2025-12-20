# src/modules/market_analysis/report_generator.py
from datetime import datetime

class ReportGenerator:
    def __init__(self, asset_name="Unknown", signal_data=None, sentiment="Neutral"):
        self.asset_name = asset_name
        self.signal_data = signal_data or {"signal": "HOLD", "confidence": "Neutral"}
        self.sentiment = sentiment

    def set_data(self, asset_name, signal_data, sentiment):
        self.asset_name = asset_name
        self.signal_data = signal_data
        self.sentiment = sentiment

    def generate_text_report(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"""
        === AI TRADEWISE ANALYSIS REPORT ===
        Asset: {self.asset_name}
        Date: {now}

        🔹 Sentiment: {self.sentiment.upper()}
        🔹 Recommendation: {self.signal_data['signal']}
        🔹 Confidence Level: {self.signal_data['confidence']}

        Insight:
        {self._generate_insight()}
        """
        return report.strip()

    def _generate_insight(self):
        sig = self.signal_data["signal"]
        conf = self.signal_data["confidence"]
        if sig == "BUY":
            return f"Potensi kenaikan harga terdeteksi. Keyakinan {conf.lower()}."
        elif sig == "SELL":
            return f"Tekanan jual tinggi. Disarankan untuk berhati-hati. Keyakinan {conf.lower()}."
        return "Pasar stabil. Belum ada sinyal kuat untuk aksi beli atau jual."

    def generate_html_report(self):
        return f"""
        <div class="report-card">
            <h2>📊 AI TradeWise Analysis</h2>
            <p><strong>Asset:</strong> {self.asset_name}</p>
            <p><strong>Sentiment:</strong> {self.sentiment.upper()}</p>
            <p><strong>Signal:</strong> <span class="signal-{self.signal_data['signal'].lower()}">{self.signal_data['signal']}</span></p>
            <p><strong>Confidence:</strong> {self.signal_data['confidence']}</p>
            <p>{self._generate_insight()}</p>
            <small>Generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</small>
        </div>
        """
