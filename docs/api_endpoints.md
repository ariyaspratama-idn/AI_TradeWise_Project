# API Endpoints (local)

Base: http://localhost:5000/api

POST /api/chat
  Request JSON:
  {
    "messages": [{"role":"user","content":"..."}],
    "model": "gpt-4o-mini"
  }
  Response:
  { "response": "AI text" }

GET /api/market/stocks
  Query: ?symbol=AAPL (optional)

GET /api/market/forex

GET /api/alerts
POST /api/alerts
  Request:
  { "symbol":"AAPL", "condition":"price > 200" }
