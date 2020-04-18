# configs are stored in json files, we define the save / load functions here.

import json
import os

parchment_data_dir = os.path.expanduser("~/parchment_data")  # STATIC_CONFIG
config_path = os.path.expanduser("~/.parchment.json")  # STATIC_CONFIG


def config_load(path=None):
    if path is None:
        path = "~/.parchment.json"
    if not os.path.exists(os.path.expanduser(path)):
        return {}
    with open(os.path.expanduser(path), "r") as f:
        data = json.load(f)
        return data


def config_save(conf_dict, path=None):
    if path is None:
        path = "~/.parchment.json"
    with open(os.path.expanduser(path), "w") as f:
        json.dump(conf_dict, f)


def get_conf():
    conf = config_load(path=config_path)
    print(conf)
    update_conf = False
    if "server_hosts" not in conf:
        try:
            conf["server_hosts"] = [
                input("Please specify backend server hostname: ").strip().replace("\'", "").replace("\"", "")]
            update_conf = True
        except KeyboardInterrupt:
            exit()
    if "key_path" not in conf:
        try:
            conf["key_path"] = input("Please specify path to git key: ").strip().replace("\'", "").replace("\"", "")
            update_conf = True
        except KeyboardInterrupt:
            exit()
    if update_conf:
        config_save(conf, path=config_path)
    return conf
