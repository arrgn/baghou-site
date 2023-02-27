from json import load
from dotenv import load_dotenv

from server.funcs.path_module import path_to_file

load_dotenv()

with open(path_to_file("config.json"), "r") as f:
    config = load(f)
