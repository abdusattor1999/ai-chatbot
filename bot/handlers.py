import httpx

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from bot.states import ConversationState
from shared.config import config, logger



bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        "🤖 Привет! Я AI-ассистент для помощи с программированием.\n\n"
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/clear - Очистить контекст разговора\n\n"
        "Просто напишите ваш вопрос, и я постараюсь помочь!"
    )
    await state.set_state(ConversationState.waiting_for_message)


@dp.message(Command("help"))
async def help_handler(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "🆘 Помощь:\n\n"
        "Я могу помочь вам с:\n"
        "• Объяснением концепций программирования\n"
        "• Отладкой кода\n"
        "• Рекомендациями по архитектуре\n"
        "• Ответами на технические вопросы\n\n"
        "Просто отправьте сообщение с вашим вопросом."
    )


@dp.message(Command("test"))
async def test_handler(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")

    try:
        # Отправляем запрос в backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.BACKEND_URL}/api/v1/test-chat",
                json={
                    "user_id": message.from_user.id,
                    "message": message.text,
                    "username": message.from_user.username or "Unknown"
                },
                timeout=30.0
            )
            print(444444, response.json())
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "Не удалось получить ответ.")

                # Разбиваем длинные сообщения
                if len(ai_response) > 4000:
                    chunks = [ai_response[i:i + 4000] for i in range(0, len(ai_response), 4000)]
                    for chunk in chunks:
                        await message.answer(chunk)
                else:
                    await message.answer(ai_response)
            else:
                await message.answer("❌ Ошибка при обработке запроса.")

    except httpx.TimeoutException:
        await message.answer("⏱ Превышено время ожидания. Попробуйте еще раз.")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")





@dp.message(Command("clear"))
async def clear_handler(message: Message, state: FSMContext):
    """Очистка контекста разговора"""
    user_id = message.from_user.id
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{config.BACKEND_URL}/api/v1/conversations/{user_id}",
                timeout=10.0
            )
            if response.status_code == 200:
                await message.answer("🗑 Контекст разговора очищен.")
            else:
                await message.answer("⚠️ Не удалось очистить контекст.")
    except Exception as e:
        logger.error(f"Error clearing context: {e}")
        await message.answer("❌ Ошибка при очистке контекста.")


@dp.message(ConversationState.waiting_for_message)
async def message_handler(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений"""
    user_id = message.from_user.id
    user_message = message.text

    # Отправляем "печатает..."
    await bot.send_chat_action(message.chat.id, "typing")

    try:
        # Отправляем запрос в backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.BACKEND_URL}/api/v1/chat",
                json={
                    "user_id": user_id,
                    "message": user_message,
                    "username": message.from_user.username or "Unknown"
                },
                timeout=30.0
            )

            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "Не удалось получить ответ.")

                # Разбиваем длинные сообщения
                if len(ai_response) > 4000:
                    chunks = [ai_response[i:i + 4000] for i in range(0, len(ai_response), 4000)]
                    for chunk in chunks:
                        await message.answer(chunk)
                else:
                    await message.answer(ai_response)
            else:
                await message.answer("❌ Ошибка при обработке запроса.")

    except httpx.TimeoutException:
        await message.answer("⏱ Превышено время ожидания. Попробуйте еще раз.")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
