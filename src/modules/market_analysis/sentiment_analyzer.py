# src/modules/market_analysis/sentiment_analyzer.py
import requests
import re
# Removed global import of TextBlob to preventing startup crashes on Vercel
# from textblob import TextBlob 

class SentimentAnalyzer:
    def __init__(self, news_api_key=None):
        self.news_api_key = news_api_key

    def clean_text(self, text):
        return re.sub(r"[^a-zA-Z\s]", "", text)

    def analyze_text_sentiment(self, text):
        cleaned = self.clean_text(text)
        try:
            from textblob import TextBlob
            analysis = TextBlob(cleaned)
            polarity = analysis.sentiment.polarity
            if polarity > 0.2:
                return "bullish"
            elif polarity < -0.2:
                return "bearish"
            return "neutral"
        except ImportError:
            # Fallback if textblob missing
            return "neutral"
        except Exception:
            # Fallback for NLTK errors
            return "neutral"

    def fetch_latest_news(self, query="stock market", limit=5):
        if not self.news_api_key:
            return []
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize={limit}&apiKey={self.news_api_key}"
            resp = requests.get(url, timeout=5) # Add timeout
            if resp.status_code != 200:
                return []
            return resp.json().get("articles", [])
        except Exception:
            return []

    def analyze_market_sentiment(self, keyword="bitcoin"):
        articles = self.fetch_latest_news(keyword)
        sentiments = []
        for a in articles:
            text = a["title"] + " " + a.get("description", "")
            label = self.analyze_text_sentiment(text)
            sentiments.append(label)
        if not sentiments:
            return "neutral"
        bullish = sentiments.count("bullish")
        bearish = sentiments.count("bearish")
        if bullish > bearish:
            return "bullish"
        elif bearish > bullish:
            return "bearish"
        return "neutral"
