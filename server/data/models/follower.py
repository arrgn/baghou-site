import sqlalchemy

from sqlalchemy import orm
from server.data.db_session import SqlAlchemyBase


class Follower(SqlAlchemyBase):
    __tablename__ = "followers"

    follower_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    followed_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('follower', 'followed'),
        {},
    )
