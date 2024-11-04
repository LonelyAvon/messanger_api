

from sqlalchemy import UUID


def get_chat_name_by_2_persons(user_id_1: UUID, user_id_2: UUID) -> str:
    return f"chat_{user_id_1}_{user_id_2}"