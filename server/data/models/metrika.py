import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class Metrika(Base):
    __tablename__ = "metrika"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data: Mapped[sqlalchemy.JSON]
