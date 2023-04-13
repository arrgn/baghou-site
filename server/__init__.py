from json import load

from bcrypt import gensalt
from dotenv import load_dotenv
from flask import Flask

from server.data.db_session import global_init
from server.funcs.path_module import path_to_file

# load configuration and .env
load_dotenv()
with open(path_to_file("config.json"), "r") as f:
    config = load(f)

# init flask, database, etc
app = Flask(__name__)
global_init()
salt = gensalt()
