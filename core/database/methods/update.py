from sqlalchemy import update

from core.database import session_maker
from core.database.models import Chat
from core.misc import parse_keywords


async def update_keywords(keywords: set[str], id_chat: int) -> Chat:
    async with session_maker.begin() as session:
        query = update(Chat).where(Chat.id == id_chat)\
            .values(keywords=';'.join(keywords)).returning(Chat)

        return await session.scalar(query)


async def add_chat_keywords(keywords: set[str], chat: Chat) -> Chat:
    chat_keywords = parse_keywords(chat.keywords or '')
    all_keywords = keywords.union(chat_keywords)

    return await update_keywords(all_keywords, chat.id)


async def delete_chat_keywords(keywords: set[str], chat: Chat) -> Chat:
    chat_keywords = parse_keywords(chat.keywords or '')
    all_keywords = chat_keywords.difference(keywords)

    return await update_keywords(all_keywords, chat.id)
