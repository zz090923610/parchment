# configs are stored in json files, we define the save / load functions here.

import json
import os


def config_load(path=None):
    if path is None:
        path = os.path.expanduser("~/.parchment.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        data = json.load(f)
        return data


def config_save(conf_dict, path=None):
    if path is None:
        path = os.path.expanduser("~/.parchment.json")
    with open(path, "w") as f:
        json.dump(conf_dict, f)
