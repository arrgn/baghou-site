import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class ChatMessage(Base):
    __tablename__ = "chat_message"

    chat_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("chats.id"), primary_key=True)
    message_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("messages.id"))
    message_number: Mapped[int] = mapped_column(primary_key=True)
