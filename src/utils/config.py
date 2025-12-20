from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "AI TradeWise")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    # Provide safe defaults or mark optional
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default-dev-secret-change-in-prod")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))

    DEFAULT_ADMIN_EMAIL: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@tradewise.ai")
    DEFAULT_ADMIN_PASSWORD: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY") 

    WHATSAPP_API_URL: Optional[str] = os.getenv("WHATSAPP_API_URL")
    WHATSAPP_API_KEY: Optional[str] = os.getenv("WHATSAPP_API_KEY")
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

    SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")

    UPDATE_INTERVAL_MINUTES: int = int(os.getenv("UPDATE_INTERVAL_MINUTES", 30))

settings = Settings()
Config = Settings
