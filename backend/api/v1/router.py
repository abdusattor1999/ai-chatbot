import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from backend.ai_agent import AIAgent
from backend.database import DatabaseManager
from backend.utils import get_db_manager, get_ai_agent
from shared.config import logger


router_v1 = APIRouter(prefix='/api/v1', tags=['ToDo'])

class ChatRequest(BaseModel):
    user_id: int
    message: str
    username: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None


@router_v1.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest,
               ai_agent: AIAgent = Depends(get_ai_agent),
               db_manager: DatabaseManager = Depends(get_db_manager)):
    """Основной endpoint для обработки сообщений"""
    try:
        logger.info(f"Chat request from user {request.user_id}: {request.message[:100]}...")
        conversation_history = await db_manager.get_conversation_history(request.user_id)
        ai_response = await ai_agent.process_message(
            message=request.message,
            user_id=request.user_id,
            conversation_history=conversation_history
        )

        await db_manager.save_message(
            user_id=request.user_id,
            user_message=request.message,
            ai_response=ai_response,
            username=request.username
        )

        return ChatResponse(response=ai_response)

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router_v1.delete("/conversations/{user_id}")
async def clear_conversation(user_id: int, db_manager: DatabaseManager = Depends(get_db_manager)):
    """Очистка истории разговора пользователя"""
    try:
        await db_manager.clear_conversation(user_id)
        logger.info(f"Cleared conversation for user {user_id}")
        return {"message": "Conversation cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear conversation")


@router_v1.get("/conversations/{user_id}/history")
async def get_conversation_history(user_id: int, limit: int = 50, db_manager: DatabaseManager = Depends(get_db_manager)):
    """Получение истории разговора"""
    try:
        history = await db_manager.get_conversation_history(user_id, limit)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")


@router_v1.get("/stats")
async def get_stats(db_manager: DatabaseManager = Depends(get_db_manager)):
    """Статистика использования"""
    try:
        stats = await db_manager.get_usage_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")
