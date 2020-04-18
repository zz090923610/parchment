import hashlib
import json
import logging
import os
import shutil
import sys
import time

from src.config import config_load, config_save, get_conf, parchment_data_dir
from src.repo_mgr import config_path, RepoHDL

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO)


class TopicHDL:
    """
    Topic is a logic abstract to group words, short paragraphs and reference documents.
    The underlying structure is actually a repo.
    """

    def __init__(self, repo_root, name="topic name", create_date=None, last_update_date=None):
        """
        :param repo_root:

        template of meta data:
        {"create_date": None,
         "marking_date": None,
         "type": "words",
         "topic": "",
         "store_hash": None}
        """
        self.logger = logging.getLogger('TopicHDL')
        self.repo_root = os.path.expanduser(repo_root)
        self.name = name
        self.create_date = create_date
        self.last_update_date = last_update_date
        self.meta_data = {}
        self.load_meta()

    def __del__(self):
        self.save_meta()

    def load_meta(self):
        meta_dir = os.path.join(self.repo_root, self.name)
        if not os.path.isdir(meta_dir):
            print("#####################################")
            self.save_meta()  # initialization
        if not os.path.exists(os.path.join(meta_dir, "meta.json")):
            print("#####################################")
            self.save_meta()  # initialization

        with open(os.path.join(meta_dir, "meta.json"), "r") as f:
            meta_dict = json.load(f)
            self.name = meta_dict["name"]
            self.create_date = meta_dict["create_date"]
            self.last_update_date = meta_dict["last_update_date"]
            self.meta_data = meta_dict["meta"]
            self.logger.info("Topic Found with %d records." % len(self.meta_data))

    def save_meta(self):
        """
        Meta data are store in path: /self.repo_root/self.name/meta.json
        This will initialize meta.json if not found.
        :return:
        """
        meta_dir = os.path.join(self.repo_root, self.name)
        os.makedirs(meta_dir, exist_ok=True)
        with open(os.path.join(meta_dir, "meta.json"), "w") as f:
            json.dump({
                "name": self.name,
                "create_date": self.create_date,
                "last_update_date": self.last_update_date,
                "meta": self.meta_data
            }
                , f)
            f.flush()
            f.close()

    def create_piece(self, piece_type, content=None, ref_path=None, para_name=None):
        new_meta = {
            "create_date": time.time(),
            "marking_date": None,
            "type": piece_type,
            "topic": self.name,
        }
        new_meta["store_hash"] = hashlib.sha224(json.dumps(new_meta).encode("utf8")).hexdigest()
        if piece_type == "words":
            with open(os.path.join(self.repo_root, self.name, "%s.txt" % new_meta["store_hash"]), "w") as f:
                f.write(content)
        elif piece_type == "para":
            file_path = os.path.join(self.repo_root, self.name, "%s_%s.txt" % (new_meta["store_hash"], para_name))
            with open(file_path, "w") as f:
                f.write("\n")
            os.system("xdg-open %s" % file_path)
            new_meta["title"] = para_name
        elif piece_type == "ref":
            file_name = os.path.split(ref_path)[1]
            new_file_name = "%s_%s" % (new_meta["store_hash"], file_name)
            shutil.copyfile(ref_path, os.path.join(self.repo_root, self.name, new_file_name))
            new_meta["title"] = file_name
        self.meta_data[new_meta["store_hash"]] = new_meta
        print(self.meta_data)
        self.save_meta()

    def delete_piece(self, store_hash):
        if store_hash not in self.meta_data:
            return
        meta = self.meta_data[store_hash]
        if "title" in meta:
            if meta["type"] == "ref":
                file_name = "%s_%s" % (store_hash, meta["title"])
            else:  # meta["type"] == "para":
                file_name = "%s_%s.txt" % (store_hash, meta["title"])

        else:
            file_name = "%s.txt" % store_hash
        full_path = os.path.join(self.repo_root, self.name, file_name)
        try:
            os.remove(full_path)
        except Exception as e:
            self.logger.error("%s" % e)
        del self.meta_data[store_hash]
        self.save_meta()

    def marking_piece(self, store_hash):
        if store_hash not in self.meta_data:
            return
        meta = self.meta_data[store_hash]
        meta["marking_date"] = time.time()
        self.meta_data[store_hash] = meta
        self.save_meta()

    def read_piece(self, store_hash):
        import datetime
        if store_hash not in self.meta_data:
            return
        meta = self.meta_data[store_hash]
        if meta["type"] == "ref":
            file_name = "%s_%s" % (store_hash, meta["title"])
        elif meta["type"] == "para":
            file_name = "%s_%s.txt" % (store_hash, meta["title"])
        else:  # meta["type"] == "words":
            file_name = "%s.txt" % store_hash
        full_path = os.path.join(self.repo_root, self.name, file_name)
        if meta["type"] == "ref":
            os.system("xdg-open %s" % full_path)
        else:  # meta["type"] == "words":
            item_date = datetime.datetime.fromtimestamp(int(meta["create_date"])).strftime('%Y-%m-%d %H:%M:%S')
            title = "%s" % meta['title'] if 'title' in meta else ""

            os.system("echo \'%s\'" % "\n<<<<<<<<< %s %s\n" % (title, item_date))
            os.system("cat %s" % full_path)
            # with open(full_path, "r") as f:
            #    l = f.readline()
            #    print(l)
            os.system("echo \'%s\'" % "\n<<<<<<<<< EOF %s %s\n" % (title, item_date))


# noinspection DuplicatedCode
def parchment_words():
    # parchment_words "topic" "content"
    if len(sys.argv) != 3:
        exit()
    topic = sys.argv[1]
    content = sys.argv[2]
    conf = get_conf()
    # check if local repo exists:
    if not os.path.exists(os.path.join(parchment_data_dir, topic)):
        # check if remote repo exists:
        rm = RepoHDL(conf["server_hosts"], conf["key_path"])
        repo_list = rm.list()
        if topic not in repo_list:
            rm.create_repo(topic)
    a = TopicHDL(parchment_data_dir, topic)
    a.create_piece("words", content=content)


# noinspection DuplicatedCode
def parchment_para():
    # parchment_para "topic" "title"
    if len(sys.argv) != 3:
        exit()
    topic = sys.argv[1]
    title = sys.argv[2]
    conf = get_conf()
    # check if local repo exists:
    if not os.path.exists(os.path.join(parchment_data_dir, topic)):
        # check if remote repo exists:
        rm = RepoHDL(conf["server_hosts"], conf["key_path"])
        repo_list = rm.list()
        if topic not in repo_list:
            rm.create_repo(topic)
    a = TopicHDL(parchment_data_dir, topic)
    a.create_piece("para", para_name=title)


# noinspection DuplicatedCode
def parchment_ref():
    # parchment_ref "topic" "ref_path"
    if len(sys.argv) != 3:
        exit()
    topic = sys.argv[1]
    ref_path = sys.argv[2]
    conf = get_conf()
    # check if local repo exists:
    if not os.path.exists(os.path.join(parchment_data_dir, topic)):
        # check if remote repo exists:
        rm = RepoHDL(conf["server_hosts"], conf["key_path"])
        repo_list = rm.list()
        if topic not in repo_list:
            rm.create_repo(topic)
    a = TopicHDL(parchment_data_dir, topic)
    a.create_piece("ref", ref_path=ref_path)


# noinspection DuplicatedCode
def parchment_timeline():
    # parchment_timeline "topic"
    if len(sys.argv) != 2:
        exit()
    topic = sys.argv[1]
    conf = get_conf()
    # check if local repo exists:
    if not os.path.exists(os.path.join(parchment_data_dir, topic)):
        # check if remote repo exists:
        rm = RepoHDL(conf["server_hosts"], conf["key_path"])
        repo_list = rm.list()
        if topic not in repo_list:
            rm.create_repo(topic)
    a = TopicHDL(parchment_data_dir, topic)
    for meta_hash in a.meta_data:
        a.read_piece(meta_hash)
