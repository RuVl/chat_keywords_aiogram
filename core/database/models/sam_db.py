from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import Mapped

from . import Base


class SamDB(Base):
    __tablename__ = 'sam_db'

    id: Mapped[int] = Column(Integer, primary_key=True)

    first_name: Mapped[str] = Column(String, nullable=False)
    last_name: Mapped[str] = Column(String, nullable=True)

    number: Mapped[int] = Column(BigInteger, nullable=False)

    def __str__(self):
        return f'{self.first_name}, {self.last_name} - {self.number}' \
            if self.last_name else \
            f'{self.first_name} - {self.number}'
