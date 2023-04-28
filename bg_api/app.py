import logging.config
import sys
import traceback

from flask import make_response
from jwt import ExpiredSignatureError
from werkzeug.exceptions import HTTPException

from bg_api import app
from bg_api import config
from bg_api.funcs.path_module import path_to_file, create_dir
from bg_api.loggers import logger
from bg_api.middlewares.auth_middleware import AuthMiddleware
from bg_api.middlewares.chat_middlware import ChatMiddleware
from bg_api.services.chat_service import ChatService
from bg_api.services.user_service import UserService


@app.post("/auth/reg")
def reg():
    return UserService.reg()


@app.post("/auth/login")
def login():
    return UserService.login()


@app.get("/auth/logout")
@AuthMiddleware.token_required
def logout(user):
    return UserService.logout(user)


@app.get("/auth/refresh")
def refresh():
    return UserService.refresh_access_token()


@app.get("/players/profile/<gtag>")
def get_profile_data(gtag):
    return UserService.get_profile_data(gtag)


@app.get("/players/profile/<gtag>/followers")
def get_followers(gtag):
    return UserService.get_followers(gtag)


@app.get("/players/search")
def get_users_by_name():
    return UserService.get_users_by_name()


@app.post("/players/follow")
@AuthMiddleware.token_required
def follow_user(user, **kwargs):
    return UserService.follow(user)


@app.post("/players/unfollow")
@AuthMiddleware.token_required
def unfollow_user(user, **kwargs):
    return UserService.unfollow(user)


@app.post("/chats/create")
@AuthMiddleware.token_required
def create_chat(user, **kwargs):
    return ChatService.create_chat(user)


@app.post("/chats/delete")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_admin
def delete_chat(chat, **kwargs):
    return ChatService.delete_chat(chat)


@app.post("/chats/<chat_tag>/add_user")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_admin
def add_user_to_chat(chat, **kwargs):
    return ChatService.add_user_to_chat(chat)


@app.post("/chats/<chat_tag>/delete_user")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_admin
def delete_user_from_chat(chat, **kwargs):
    return ChatService.delete_user_from_chat(chat)


@app.post("/chats/<chat_tag>/leave")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
def leave_from_chat(user, chat, **kwargs):
    return ChatService.leave_chat(user, chat)


@app.post("/chats/<chat_tag>/promote")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_admin
def promote_user(chat, **kwargs):
    return ChatService.change_role(chat)


@app.post("/chats/<chat_tag>/send_message")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_access
def send_message(user, chat, **kwargs):
    return ChatService.send_message(user, chat)


@app.post("/chats/<chat_tag>/delete_message")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_access
def delete_message(user, chat, **kwargs):
    return ChatService.delete_message(user, chat)


@app.get("/chats")
@AuthMiddleware.token_required
def get_users_chats(user, **kwargs):
    return ChatService.get_users_chats(user)


@app.get("/chats/<chat_tag>")
@AuthMiddleware.token_required
@ChatMiddleware.get_chat
@ChatMiddleware.check_access
def get_messages(chat, **kwargs):
    return ChatService.get_messages(chat)


@app.errorhandler(HTTPException)
def http_error_handler(e):
    res = make_response(e.description)
    res.status = e.code
    return res


@app.errorhandler(ExpiredSignatureError)
def expired_signature_error(e):
    res = make_response({"msg": "Пользователь не авторизован!"})
    res.status = 401
    return res


@app.errorhandler(Exception)
def something_went_wrong_error(e):
    logger.exception(e)
    res = make_response({"msg": "Что-то пошло не так."})
    res.status = 500
    return res


def log_handler(exctype, value, tb):
    """
    Custom exception handler.
    All critical errors will be logged with tag [ERROR]
    """
    logger.exception(''.join(traceback.format_exception(exctype, value, tb)))


# Create folder for log and load log configuration
create_dir("logs")

logging.config.fileConfig(fname=path_to_file("logging.conf"), disable_existing_loggers=False)
if not config["debug"]:
    logging.disable(level=logging.WARNING)
sys.excepthook = log_handler

if __name__ == "__main__":
    app.run(debug=config["debug"])
