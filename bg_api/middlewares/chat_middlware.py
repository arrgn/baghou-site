from functools import wraps

from flask import abort, request

from bg_api.data.__all_models import Chat, ChatRole, User, UserChat
from bg_api.data.db_session import create_session


class ChatMiddleware:
    @staticmethod
    def check_access(f):
        """
        Check if a user has access to chat.
        User and chat must be in kwargs.

        :param f: Function.
        :return: f or http error.
        """

        @wraps(f)
        def decorated(*args, **kwargs):
            # get data from kwargs
            user: User = kwargs["user"]
            chat: Chat = kwargs["chat"]

            with create_session() as dao:
                # get data about user in the chat
                user_chat = dao.query(UserChat).filter(UserChat.user_id == user.id, UserChat.chat_id == chat.id).first()
                # check access
                if not user_chat:
                    abort(403, {"msg": "Отказано в доступе!"})

            return f(*args, **kwargs)

        return decorated

    @staticmethod
    def check_admin(f):
        """
        Check if a user has admin access to chat.
        User and chat must be in kwargs.

        :param f: Function.
        :return: f or http error.
        """

        @wraps(f)
        def decorated(*args, **kwargs):
            # get data from kwargs
            user: User = kwargs["user"]
            chat: Chat = kwargs["chat"]

            with create_session() as dao:
                # get admin role
                admin = dao.query(ChatRole).filter(ChatRole.name == "ADMIN").first()
                # get data about user in the chat
                user_role = dao.query(ChatRole).join(UserChat, UserChat.role_id == ChatRole.id).filter(
                    UserChat.user_id == user.id, UserChat.chat_id == chat.id).first()
                # check for access to chat
                if not user_role:
                    abort(403, {"msg": "Отказано в доступе!"})
                # check for admin access to chat
                elif user_role.id != admin.id:
                    abort(403, {"msg": "Отказано в доступе!"})

            return f(*args, **kwargs)

        return decorated

    @staticmethod
    def get_chat(f):
        """
        If found chat - add it to kwargs.
        Else - abort an error.

        :param f: Function.
        :return: f or http error.
        """

        @wraps(f)
        def decorated(*args, **kwargs):
            # get chat_tag
            if "chat_tag" in kwargs:
                chat_tag = kwargs["chat_tag"]
            else:
                chat_tag = request.json["chat_tag"]

            # end of chat's name
            eon = chat_tag.rfind("-")
            chat_name, chat_id = chat_tag[:eon], chat_tag[eon + 1:]

            with create_session() as dao:
                # get chat
                chat = dao.query(Chat).filter(Chat.id == chat_id, Chat.name == chat_name).first()
                # check for chat exists
                if not chat:
                    abort(400, {"msg": f"Чат {chat_name}#{chat_id} не был найден!", "error": "GE#CNF"})

            return f(chat=chat, *args, **kwargs)

        return decorated
