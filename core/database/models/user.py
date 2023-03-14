from sqlalchemy import BigInteger, Text, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)

    chats: Mapped[list["Chat"]] = relationship(lazy=False)


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    chat_title = Column(String, nullable=False)

    keywords = Column(Text, nullable=True)

    owner_id = Column(BigInteger, ForeignKey(User.user_id), nullable=False)
