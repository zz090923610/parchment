
# All local data should be stored in storage_root = /home/<user>/.lRecorder/
# Job data should be in $storage_root/jobs
# Alias path = $storage_root/alias
# Other config = $storage_root/config.json

import os


def os_touch(path):
    with open(path, 'a'):
        os.utime(path, None)


class ConfigHDL:
    def __init__(self):
        self.storage_root = os.path.expanduser("~/.lRecorder/")
        self.job_root = os.path.join(self.storage_root, "jobs")
        self.alias_path = os.path.join(self.storage_root, "alias")
        self.config_path = os.path.join(self.storage_root, "config.json")
        self.digest_path = '/tmp/OhMyLifeRecorderDigest'
        self.init_local_data_path()

    def __del__(self):
        pass

    def init_local_data_path(self):
        os.makedirs(self.storage_root, exist_ok=True)
        os.makedirs(self.job_root, exist_ok=True)
        os.makedirs(self.digest_path, exist_ok=True)
        os_touch(self.alias_path)
        os_touch(self.config_path)

    def clear_local_data(self):
        os.system('rm -rf %s' % self.storage_root)
