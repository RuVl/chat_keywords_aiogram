from sqlalchemy import update

from core.database import session_maker
from core.database.models import Chat
from core.parsers import parse_keywords


async def update_chat_keywords(keywords: set[str], id_chat: int) -> Chat:
    async with session_maker.begin() as session:
        query = update(Chat).where(Chat.id == id_chat)\
            .values(keywords=';'.join(keywords)).returning(Chat)

        return await session.scalar(query)


async def add_chat_keywords(keywords: set[str], chat: Chat) -> Chat:
    chat_keywords = parse_keywords(chat.keywords)
    all_keywords = keywords.union(chat_keywords)

    return await update_chat_keywords(all_keywords, chat.id)


async def delete_chat_keywords(keywords: set[str], chat: Chat) -> Chat:
    chat_keywords = parse_keywords(chat.keywords)
    all_keywords = chat_keywords.difference(keywords)

    return await update_chat_keywords(all_keywords, chat.id)


async def update_chat_condition(raw: str, parsed: str, id_chat: int) -> Chat:
    async with session_maker.begin() as session:
        query = update(Chat).where(Chat.id == id_chat)\
            .values(raw_conditions=raw, parsed_conditions=parsed).returning(Chat)

        return await session.scalar(query)


async def add_chat_condition(raw_condition: str, parsed_condition: str, chat: Chat) -> Chat:
    if chat.raw_conditions:
        raw = f'{chat.raw_conditions}^{raw_condition}'
    else:
        raw = raw_condition

    if chat.parsed_conditions:
        parsed = f'{chat.parsed_conditions[:-1]}|{parsed_condition})'
    else:
        parsed = f'(?:{parsed_condition})'

    return await update_chat_condition(raw, parsed, chat.id)


async def delete_chat_condition(raw_condition: str, parsed_condition: str, chat: Chat) -> Chat:
    def _del(before: str, after: str, sep: str, empty='') -> str:
        if after and after[0] == sep:  # Remove sep
            after = after[1:]
        elif before and before[-1] == sep:
            before = before[:-1]

        result = before + after
        return result if result != empty else ''

    r = chat.raw_conditions.split(raw_condition, 1)
    before, after = (r[0], r[1] if len(r) == 2 else '')
    raw = _del(before, after, '^')

    p = chat.parsed_conditions.split(parsed_condition, 1)
    before, after = (p[0], p[1] if len(p) == 2 else '')
    parsed = _del(before, after, '|', '(?:)')

    return await update_chat_condition(raw, parsed, chat.id)
