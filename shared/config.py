import os
from pydantic_settings import BaseSettings
import logging


class Config(BaseSettings):
    # Telegram Bot
    TELEGRAM_TOKEN: str = os.environ.get("TELEGRAM_TOKEN")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # Backend
    BACKEND_URL: str = "http://backend:8000"
    DATABASE_URL: str = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_DB')}:{os.getenv('DB_PORT')}/chatbot_db"

    # Redis (для кеширования)
    REDIS_URL: str = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT', '6379')}"

    # Логирование
    LOG_LEVEL: str = "INFO"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


    def __post_init__(self):
        logger.info(f"Backend URL: {self.BACKEND_URL}")
        logger.info(f"Database URL: {self.DATABASE_URL[:50]}...")

        if not self.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN is required")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")


# Создаем глобальный экземпляр конфигурации
config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)