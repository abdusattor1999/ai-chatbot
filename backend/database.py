import asyncpg
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
from shared.config import config

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def initialize(self):
        try:
            self.pool = await asyncpg.create_pool(
                config.DATABASE_URL,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            await self._create_tables()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    username VARCHAR(255),
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_conversations_user_id 
                ON conversations(user_id);

                CREATE INDEX IF NOT EXISTS idx_conversations_created_at 
                ON conversations(created_at);
            """)

    async def save_message(
            self,
            user_id: int,
            user_message: str,
            ai_response: str,
            username: Optional[str] = None
    ):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO conversations (user_id, username, user_message, ai_response)
                    VALUES ($1, $2, $3, $4)
                """, user_id, username, user_message, ai_response)
        except Exception as e:
            logger.error(f"Failed to save message: {e}")

    async def get_conversation_history(
            self,
            user_id: int,
            limit: int = 20
    ) -> List[Dict[str, Any]]:
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT user_message, ai_response, created_at
                    FROM conversations
                    WHERE user_id = $1
                    ORDER BY created_at DESC
                    LIMIT $2
                """, user_id, limit)

                return [
                    {
                        "user_message": row["user_message"],
                        "ai_response": row["ai_response"],
                        "created_at": row["created_at"].isoformat()
                    }
                    for row in reversed(rows)
                ]
        except Exception as e:
            logger.error(f"Failed to get conversation history: {e}")
            return []

    async def clear_conversation(self, user_id: int):
        """Очистка истории разговора пользователя"""
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    DELETE FROM conversations WHERE user_id = $1
                """, user_id)
        except Exception as e:
            logger.error(f"Failed to clear conversation: {e}")
            raise

    async def get_usage_stats(self) -> Dict[str, Any]:
        """Получение статистики использования"""
        try:
            async with self.pool.acquire() as conn:
                # Общее количество сообщений
                total_messages = await conn.fetchval("""
                    SELECT COUNT(*) FROM conversations
                """)

                # Уникальные пользователи
                unique_users = await conn.fetchval("""
                    SELECT COUNT(DISTINCT user_id) FROM conversations
                """)

                # Сообщения за последние 24 часа
                messages_24h = await conn.fetchval("""
                    SELECT COUNT(*) FROM conversations
                    WHERE created_at > NOW() - INTERVAL '24 hours'
                """)

                return {
                    "total_messages": total_messages,
                    "unique_users": unique_users,
                    "messages_last_24h": messages_24h
                }
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {}

    async def close(self):
        """Закрытие подключения к БД"""
        if self.pool:
            await self.pool.close()

