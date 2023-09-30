from sqlalchemy import BigInteger, Text, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from . import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)

    chats: Mapped[list["Chat"]] = relationship(lazy=False)


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = Column(Integer, primary_key=True)
    chat_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    chat_title: Mapped[str] = Column(String, nullable=False)

    keywords: Mapped[str] = Column(Text, nullable=True)

    raw_conditions: Mapped[str] = Column(String, nullable=True)
    parsed_conditions: Mapped[str] = Column(String, nullable=True)

    owner_id: Mapped[int] = Column(BigInteger, ForeignKey(User.user_id), nullable=False)
