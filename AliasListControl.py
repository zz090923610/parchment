import os

__author__ = 'zhangzhao'


class AliasListControl(object):
    def __init__(self, path=os.path.expanduser('~/OhMyLifeRecorderUserData/alias')):
        self.path = path
        if not os.path.isfile(self.path):
            os.popen('touch ' + self.path)

    def add_alias(self, alias):
        with open(self.path, mode='a', encoding='utf-8') as a_file:
            a_file.write(alias)