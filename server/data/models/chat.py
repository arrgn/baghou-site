import sqlalchemy
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    about: Mapped[str]
    avatar: Optional[Mapped[bytes]]
