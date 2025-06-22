from fastapi import FastAPI
from typing import Optional
from contextlib import asynccontextmanager

from .ai_agent import AIAgent
from .database import DatabaseManager
from shared.config import logger

ai_agent: Optional[AIAgent] = None
db_manager: Optional[DatabaseManager] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    global ai_agent, db_manager

    # Инициализация при запуске
    logger.info("Initializing AI Agent and Database...")
    ai_agent = AIAgent()
    db_manager = DatabaseManager()
    await db_manager.initialize()

    yield

    # Очистка при завершении
    logger.info("Shutting down...")
    if db_manager:
        await db_manager.close()


async def get_db_manager():
    if db_manager is None:
        raise RuntimeError("DatabaseManager not initialized")
    return db_manager


async def get_ai_agent():
    if ai_agent is None:
        raise RuntimeError("AIAgent not initialized")
    return ai_agent