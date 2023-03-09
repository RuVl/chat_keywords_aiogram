from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.misc import DBKeys

connection_string = f'postgresql+asyncpg://{DBKeys.USERNAME}:{DBKeys.PASSWORD}@{DBKeys.HOST}:{DBKeys.PORT}/{DBKeys.DATABASE}'

engine = create_async_engine(connection_string)
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)
