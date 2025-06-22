# backend/ai_agent.py
import openai
from typing import List, Dict, Any, Optional
import logging
from shared.config import config

logger = logging.getLogger(__name__)


class AIAgent:
    """AI Agent для обработки сообщений пользователей"""

    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> str:
        """Системный промпт для AI ассистента"""
        return """Ты опытный AI-ассистент программист, специализирующийся на помощи разработчикам.
            Твои возможности:
            - Объяснение концепций программирования простым языком
            - Помощь с отладкой и оптимизацией кода
            - Рекомендации по архитектуре и best practices
            - Ответы на технические вопросы
            - Помощь с выбором технологий и инструментов
            
            Правила общения:
            - Отвечай четко и по существу
            - Приводи примеры кода когда это помогает
            - Объясняй сложные концепции пошагово
            - Если не уверен в ответе, честно об этом скажи
            - Используй эмодзи умеренно для улучшения читаемости
            - Отвечай на том же языке, на котором задан вопрос
            Помни контекст предыдущих сообщений в разговоре."""



    async def process_message(
            self,
            message: str,
            user_id: int,
            conversation_history: List[Dict[str, Any]] = None
    ) -> str:
        """Обработка сообщения пользователя"""
        try:
            # Формируем контекст разговора
            messages = [{"role": "system", "content": self.system_prompt}]

            # Добавляем историю разговора (последние 10 сообщений)
            if conversation_history:
                for item in conversation_history[-10:]:
                    messages.append({"role": "user", "content": item["user_message"]})
                    messages.append({"role": "assistant", "content": item["ai_response"]})

            # Добавляем текущее сообщение
            messages.append({"role": "user", "content": message})

            # Отправляем запрос к OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )

            ai_response = response.choices[0].message.content.strip()
            logger.info(f"AI response generated for user {user_id}")

            return ai_response

        except Exception as e:
            logger.error(f"Error in AI processing: {e}")
            return "❌ Извините, произошла ошибка при обработке вашего запроса. Попробуйте еще раз."