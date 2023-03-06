import sqlalchemy
from server.data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'friends'

    user1 = sqlalchemy.Column(sqlalchemy.ForeignKey("user.id"))
    user2 = sqlalchemy.Column(sqlalchemy.ForeignKey("user.id"))