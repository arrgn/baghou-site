import sqlalchemy
from server.data.db_session import SqlAlchemyBase


class UserChat(SqlAlchemyBase):
    __tablename__ = "user_chat"

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id"), primary_key=True)
