import sqlalchemy
import datetime
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    message: Mapped[str]
    time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
