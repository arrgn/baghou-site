import sqlalchemy
from server.data.db_session import SqlAlchemyBase


class UserChat(SqlAlchemyBase):
    __tablename__ = "user_chat"

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id"))

    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint("user_id", "chat_id"),
        {},
    )
