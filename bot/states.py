from aiogram.fsm.state import State, StatesGroup

class ConversationState(StatesGroup):
    waiting_for_message = State()
