from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from server.data.data_types import str255, text, json
from server.data.db_session import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str255] = mapped_column(index=True)
    about: Mapped[str255]
    avatar: Mapped[Optional[bytes]]

    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="chat")
    users: Mapped[List["UserChat"]] = relationship(back_populates="chat")


class ChatMessage(Base):
    __tablename__ = "chat_message"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    message_number: Mapped[int] = mapped_column(primary_key=True)

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    message: Mapped["Message"] = relationship(back_populates="chats")


class Follower(Base):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    message: Mapped[str255]

    chats: Mapped[List["ChatMessage"]] = relationship(back_populates="message")
    sender: Mapped["User"] = relationship(back_populates="messages")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str255] = mapped_column(index=True)
    bio: Mapped[str255] = mapped_column(default="")
    email: Mapped[str255] = mapped_column(unique=True)
    password: Mapped[str255]
    isactivated: Mapped[bool] = mapped_column(default=False)
    useotp: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[Optional[bytes]]

    messages: Mapped[List["Message"]] = relationship(back_populates="sender")
    chats: Mapped[List["UserChat"]] = relationship(back_populates="user")
    tokens: Mapped[List["Token"]] = relationship(back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    refresh_token: Mapped[text] = mapped_column(primary_key=True)

    user: Mapped["User"] = relationship(back_populates="tokens")


class UserChat(Base):
    __tablename__ = "user_chat"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    time: Mapped[datetime] = mapped_column(default=datetime.now())

    user: Mapped["User"] = relationship(back_populates="chats")
    chat: Mapped["Chat"] = relationship(back_populates="users")


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str255]

    statistics: Mapped[List["CharacterStatistic"]] = relationship(back_populates="character")


class CharacterStatistic(Base):
    __tablename__ = "characters_statistic"

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    statistics: Mapped[json]

    character: Mapped["Character"] = relationship(back_populates="statistics")


class GameSession(Base):
    __tablename__ = "games_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    statistics1_id: Mapped[int] = mapped_column(ForeignKey("characters_statistic.id"))
    statistics2_id: Mapped[int] = mapped_column(ForeignKey("characters_statistic.id"))
    general_data: Mapped[json]
