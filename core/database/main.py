from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.misc import DBKeys

engine = create_async_engine(DBKeys.connection_string)
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)
