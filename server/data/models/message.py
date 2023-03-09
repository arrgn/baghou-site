import sqlalchemy
import datetime
from server.data.db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = "messages"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    message = sqlalchemy.Column(sqlalchemy.Text)
    time_sent = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.datetime.now())
