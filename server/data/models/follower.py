import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class Follower(Base):
    __tablename__ = "followers"

    follower: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"), primary_key=True)
    followed: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"), primary_key=True)
