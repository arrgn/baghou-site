from json import load

from server.funcs.path_module import path_to_file

with open(path_to_file("config.json"), "r") as f:
    config = load(f)
