# the backend of parchment is actually a git server.
# whenever we create / modify / delete an topic, we are pushing to backend git repos.
# we only support one backend server.

# Designed function:
# topic create delete

# topic sync (pull push):

import os
import time

import paramiko

from src.config import config_load, config_save, parchment_data_dir, config_path, get_conf
from src.ssh_mgr import SSHHdl
import logging
import getpass

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO)




class RepoHDL:
    def __init__(self, server_hosts, key_path):
        self.logger = logging.getLogger('RepoHDL')
        #
        self.server_hosts = server_hosts  # alias of same host
        self.user = "git"
        self.key_path = key_path
        self.local_store_dir = os.path.expanduser(parchment_data_dir)
        os.makedirs(self.local_store_dir, exist_ok=True)
        for h in self.server_hosts:
            if "onion" in h:
                pass  # TODO add Tor proxy support
            try:
                self.ssh_hdl = SSHHdl(h, self.user, self.key_path)
            except paramiko.ssh_exception.SSHException as e:
                self.logger.error("%s" % e)
                exit()
            if self.ssh_hdl.ready():
                self.logger.info("Backend server connected.")
                self.valid_host = h
                break
            else:
                self.ssh_hdl = None
                self.valid_host = None
        if self.ssh_hdl is None:
            self.logger.error("Cannot connect to backend server.")

    def __del__(self):
        if self.ssh_hdl is not None:
            self.ssh_hdl.close()

    # noinspection PyMethodMayBeStatic
    def name_legal(self, name):
        if name is None:
            return False
        if name == "":
            return False
        return True

    def repo_exist(self, name):
        # repo should be listed in home dir of "git" user
        if not self.name_legal(name):
            return False
        res = self.ssh_hdl.exec_cmd("ls | grep .git", ret=True)
        for i in res["stdout"]:
            if name + ".git" == i:
                return True
        return False

    def create_repo(self, name):
        if not self.name_legal(name):
            return
        if self.repo_exist(name):
            self.logger.error("%s is already exist. Abort." % name)
            return
        _ = self.ssh_hdl.exec_cmd("mkdir %s.git; cd %s.git; git init --bare" % (name, name), ret=True)
        self.logger.info("Cloning: git@%s:~/%s.git" % (self.valid_host, name))
        os.system("cd %s; git clone git@%s:~/%s.git" % (self.local_store_dir, self.valid_host, name))
        self.logger.info("%s created." % name)

    def delete_repo(self, name):
        if not self.name_legal(name):
            return
        if input("Are you sure? (Say yes)").strip().upper() != "YES":
            return
        if not self.repo_exist(name):
            self.logger.error("%s doesn't exist. Abort." % name)
            return
        _ = self.ssh_hdl.exec_cmd("rm -rf %s.git" % name, ret=True)
        self.logger.info("%s purged." % name)
        self.logger.info("Please delete manually: %s/%s " % (self.local_store_dir, name))

    def pull(self, name):
        if not self.name_legal(name):
            return
        os.system("cd  %s/%s; git pull" % (self.local_store_dir, name))

    def push(self, name):
        if not self.name_legal(name):
            return
        user = getpass.getuser()
        machine = os.uname()[1]
        date_time = time.asctime(time.localtime(time.time()))
        comment_str = "%s@%s:%s" % (user, machine, date_time)
        os.system(
            "cd  %s/%s; git add --all&& git commit -m\'%s\'&& git push" % (self.local_store_dir, name, comment_str))

    def list(self):
        res = self.ssh_hdl.exec_cmd("ls | grep .git", ret=True)["stdout"]
        res = [i.replace(".git", "") for i in res]
        return res


def main():
    import sys
    # parchment_repo create name
    # parchment_repo delete name
    # parchment_repo push name
    # parchment_repo pull name
    if len(sys.argv) != 3:
        exit()
    cmd = sys.argv[1]
    name = sys.argv[2]
    conf = get_conf()

    a = RepoHDL(conf["server_hosts"], conf["key_path"])
    if cmd == "create":
        a.create_repo(name)
    elif cmd == "delete":
        a.delete_repo(name)
    elif cmd == "push":
        a.push(name)
    elif cmd == "pull":
        a.pull(name)
