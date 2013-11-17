import time

__author__ = 'zhangzhao'
from EntryElement import *


class MarkDownGenerator(object):
    def __init__(self, job_entry: EntryElement, out_file_path: str):
        self.final_string = ''
        self.out_put_path = out_file_path
        self.entry = job_entry

    def generate_job_header(self):
        self.final_string += '<h1>OhMyLifeRecorder Digest</h1>\n'
        self.final_string += '<h2>' + self.entry.name + '</h2>\n'
        self.final_string += 'Created: ' + time.strftime(
            '%Y-%m-%d, %H:%M:%S ', time.localtime(self.entry.create_time)) + '\n\n'
        self.final_string += 'Status: ' + self.entry.status + ' since ' + time.strftime(
            '%Y-%m-%d, %H:%M:%S ', time.localtime(self.entry.status_change_time)) + '\n\n'

    def generate_status_change_data(self):
        self.final_string += '<h3>Status change history: </h3>\n<ul>\n'
        for loop in self.entry.status_change_list:
            self.final_string += '<li>' + time.strftime('%m-%d, %H:%M:%S: ', time.localtime(float(loop['time']))) + \
                                 'status changed from ' + \
                                 loop['from'] + ' to ' + loop['to'] + '</li>\n'
        self.final_string += '\n</ul>\n'

    def generate_comments(self):
        self.final_string += '<h3>Diary: </h3>\n<ul>\n'
        for loop in self.entry.comment_list:
            self.final_string += '<li>' + time.strftime('%m-%d, %H:%M:%S: ',
                                                        time.localtime(float(loop['time']))) + loop['content'] + \
                                 '</li>\n'

    def write_out(self):
        with open(self.out_put_path, mode='w', encoding='utf-8') as a_file:
            a_file.write(self.final_string)

    def generate_process(self):
        self.generate_job_header()
        self.generate_status_change_data()
        self.generate_comments()
        self.write_out()