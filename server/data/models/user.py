import sqlalchemy
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    about: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    isactivated: Mapped[bool] = mapped_column(default=False)
    avatar: Optional[Mapped[bytes]]
