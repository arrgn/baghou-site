import sqlalchemy
from server.data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Chat(SqlAlchemyBase):
    __tablename__ = "chats"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    about = sqlalchemy.Column(sqlalchemy.String)
    avatar = sqlalchemy.Column(sqlalchemy.BINARY, nullable=True)
