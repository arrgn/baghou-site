import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class UserChat(Base):
    __tablename__ = "user_chat"

    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("chats.id"), primary_key=True)
