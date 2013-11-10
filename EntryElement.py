__author__ = 'zhangzhao'
import time


class EntryElement(object):
    def __init__(self, name='None', category='unspecified', status='None', create_time='None'):
        self.name = name
        self.create_time = create_time
        self.finish_time = 0
        self.category = category
        self.status = status
        self.comment_list = {}

    def __str__(self):
        result = 'Name: ' + self.name + '\nCategory: ' + self.category + '\nCreated time: ' + time.strftime(
            '%Y-%m-%d, %H:%M:%S ', self.create_time) + '\nStatus: ' + self.status
        return result

    def save(self, path):
        with open(path, mode='w', encoding='utf-8') as a_file:
            a_file.write(self.__str__())
