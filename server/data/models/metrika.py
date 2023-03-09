import sqlalchemy
from server.data.db_session import SqlAlchemyBase


class Metrika(SqlAlchemyBase):
    __tablename__ = "metrika"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    data = sqlalchemy.Column(sqlalchemy.JSON)
