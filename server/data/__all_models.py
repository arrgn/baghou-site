from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import mapped_column, Mapped
from server.data.db_session import Base
from data_types import str255


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str255] = mapped_column(index=True)
    about: Mapped[str255]
    avatar: Optional[Mapped[bytes]] = mapped_column(nullable=True)


class ChatMessage(Base):
    __tablename__ = "chat_message"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    message_number: Mapped[int] = mapped_column(primary_key=True)


class Follower(Base):
    __tablename__ = "followers"

    follower: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followed: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    message: Mapped[str255]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str255] = mapped_column(index=True)
    about: Mapped[str255]
    email: Mapped[str255] = mapped_column(unique=True)
    password: Mapped[str255]
    isactivated: Mapped[bool] = mapped_column(default=False)
    useotp: Mapped[bool] = mapped_column(default=False)
    avatar: Optional[Mapped[bytes]] = mapped_column(nullable=True)


class UserChat(Base):
    __tablename__ = "user_chat"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    time: Mapped[datetime] = mapped_column(default=datetime.now())


class Characters(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str255]


class CharactersStatistics(Base):
    __tablename__ = "characters_statistic"

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    statistics: Mapped[JSON]


class GamesSessions(Base):
    __tablename__ = "games_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    statistics1_id: Mapped[int] = mapped_column(ForeignKey("characters_statistic.id"))
    statistics2_id: Mapped[int] = mapped_column(ForeignKey("characters_statistic.id"))
    general_data: Mapped[JSON]
