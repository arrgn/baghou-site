from flask import request, make_response, abort

from bg_api.data.__all_models import Chat, UserChat, ChatRole, User, Message, ChatMessage
from bg_api.data.db_session import create_session
from bg_api.services.user_service import UserService


class ChatService:
    @staticmethod
    def create_chat(user: User):
        name = request.json["name"]
        about = request.json["about"]

        with create_session() as dao:
            dao.expire_on_commit = False
            admin = dao.query(ChatRole).filter(ChatRole.name == "ADMIN").first()

            chat = Chat(name=name, about=about)
            user_chat = UserChat(user_id=user.id, role_id=admin.id, chat=chat)
            dao.add(chat)
            dao.add(user_chat)
            dao.commit()

        res = make_response({"msg": f"Чат {chat.name}#{chat.id} успешно создан!"})

        return res

    @staticmethod
    def delete_chat(chat: Chat):
        with create_session() as dao:
            dao.delete(chat)
            dao.commit()

        res = make_response({"msg": f"Чат {chat.name}#{chat.id} был удален!"})

        return res

    @staticmethod
    def add_user_to_chat(chat: Chat):
        gtag = request.json["gtag"]
        username, user_id = UserService.parse_gtag(gtag)

        with create_session() as dao:
            add_user = dao.query(User).filter(User.id == user_id, User.name == username).first()
            if not add_user:
                abort(400, {"msg": f"Пользователь {gtag} не был найден!"})

            user_chat = UserChat(chat_id=chat.id, user_id=add_user.id)

            dao.add(user_chat)
            dao.commit()

        res = make_response({"msg": f"Пользователь {gtag} был успешно добавлен в чат {chat.name}#{chat.id}!"})

        return res

    @staticmethod
    def delete_user_from_chat(chat: Chat):
        gtag = request.json["gtag"]
        username, user_id = UserService.parse_gtag(gtag)

        with create_session() as dao:
            del_user = dao.query(User).filter(User.id == user_id, User.name == username).first()
            if not del_user:
                abort(400, {"msg": f"Пользователь {gtag} не был найден!"})

            user_chat = dao.query(UserChat).filter(UserChat.user_id == del_user.id, UserChat.chat_id == chat.id).first()

            dao.delete(user_chat)
            dao.commit()

        res = make_response({"msg": f"Пользователь {gtag} был успешно удален из чата {chat.name}#{chat.id}!"})

        return res

    @staticmethod
    def leave_chat(user: User, chat: Chat):
        with create_session() as dao:
            user_chat = dao.query(UserChat).filter(UserChat.chat_id == chat.id, UserChat.user_id == user.id).first()
            if not user_chat:
                abort(400, {"msg": f"Пользователь {user.name}#{user.id} не был найден в чате {chat.name}#{chat.id}!"})

            dao.delete(user_chat)
            dao.commit()

        res = make_response(
            {"msg": f"Пользователь {user.name}#{user.id} успешно покинул чат {chat.name}#{chat.id}!"})

        return res

    @staticmethod
    def change_role(chat: Chat):
        gtag = request.json["gtag"]
        role = request.json["new_role"]

        with create_session() as dao:
            change_user = UserService.get_user(gtag)

            user_chat = dao.query(UserChat).filter(UserChat.chat_id == chat.id,
                                                   UserChat.user_id == change_user.id).first()
            if not user_chat:
                abort(400, {"msg": f"Пользователь {gtag} не найден в чате {chat.name}#{chat.id}!"})

            new_role = dao.query(ChatRole).filter(ChatRole.name == role).first()
            if not new_role:
                abort(400, {"msg": f"Роль {role} не была найдена!"})

            user_chat.role_id = new_role.id
            dao.commit()

        res = make_response({"msg": f"Роль пользователя {gtag} успешно изменена на {role}!"})

        return res

    @staticmethod
    def send_message(user: User, chat: Chat):
        text = request.json["message"]

        with create_session() as dao:
            dao.expire_on_commit = False

            message = Message(user_id=user.id, message=text)
            chat_message = ChatMessage(chat_id=chat.id, message=message)

            dao.add(message)
            dao.add(chat_message)
            dao.commit()

        res = make_response({"msg": "Сообщение было успешно отправлено!"})

        return res

    @staticmethod
    def delete_message(user: User, chat: Chat):
        message_number = int(request.json["number"])

        with create_session() as dao:
            message = dao.query(Message).join(ChatMessage, ChatMessage.message_id == Message.id).filter(
                Message.user_id == user.id, ChatMessage.chat_id == chat.id,
                ChatMessage.message_number == message_number).first()
            if not message:
                abort(400, {"msg": f"Сообщение с номером {message_number} от пользователя {user.name}#{user.id} "
                                   f"в чате {chat.name}#{chat.id} не найдено!"})

            dao.delete(message)
            dao.commit()

        res = make_response(
            {"msg": f"Сообщение с номером {message_number} в чате {chat.name}#{chat.id} успешно удалено!"})

        return res

    @staticmethod
    def get_users_chats(user: User):
        with create_session() as dao:
            chats_unparsed = dao.query(Chat).join(UserChat, UserChat.chat_id == Chat.id).filter(
                UserChat.user_id == user.id).all()

        res = make_response(list(map(lambda chat: {
            "chat-tag": f"{chat.name}#{chat.id}",
            "about": chat.about,
            "avatar": chat.avatar
        }, chats_unparsed)))

        return res

    @staticmethod
    def get_messages(chat: Chat):
        offset = int(request.json["offset"])
        count = int(request.json["count"])

        with create_session() as dao:
            messages_unparsed = dao \
                .query(Message.message, User.name, User.id, ChatMessage.message_number) \
                .join(User, User.id == Message.user_id) \
                .join(ChatMessage, ChatMessage.message_id == Message.id) \
                .filter(ChatMessage.chat_id == chat.id) \
                .order_by(ChatMessage.message_number.desc()) \
                .slice(offset, offset + count) \
                .all()

        res = make_response(list(map(lambda message: {
            "number": message.message_number,
            "gtag": f"{message.name}#{message.id}",
            "text": message.message
        }, messages_unparsed)))

        return res
