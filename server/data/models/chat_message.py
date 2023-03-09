import sqlalchemy
from server.data.db_session import SqlAlchemyBase


class ChatMessage(SqlAlchemyBase):
    __tablename__ = "chat_message"

    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id"), primary_key=True)
    message_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("messages.id"))
    message_number = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
