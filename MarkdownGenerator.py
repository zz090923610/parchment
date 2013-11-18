from datetime import date
import os
import time

__author__ = 'zhangzhao'
from EntryElement import *


class MarkDownGenerator(object):
    def __init__(self, out_file_path: str, the_date=None):
        self.date = the_date
        self.final_string = ''
        self.out_put_path = out_file_path
        self.entry = EntryElement()
        self.final_status_string = ''
        self.final_comment_string = ''
        self.meta = '\n<h6>This digest is generated automatically by OhMyLifeRecorder.</h6>\n' \
                    'You can get more information here: https://github.com/zz090923610/OhMyLifeRecorder'

    def generate_daily_digest_header(self):
        self.final_string += '<h1>OhMyLifeRecorder Daily Digest: ' + str(self.date) + '</h1>\n'


    def generate_daily_digest_an_entry(self, job_entry: EntryElement):
        entry = job_entry
        temp_status_string = '\t\t<ul>\n'
        temp_comment_string = '\t\t<ul>\n'
        status_modified_today = False
        comment_modified_today = False
        for loop in entry.status_change_list:
            if date.fromtimestamp(float(loop['time'])) == self.date:
                status_modified_today = True
                temp_status_string += '\t\t\t<li>' + time.strftime('`%H:%M:%S`',
                                                                   time.localtime(float(loop['time']))) + loop[
                                          'to'] + '</li>\n'
        temp_status_string += '\t\t</ul>\n'
        if status_modified_today is True:
            self.final_status_string += '\t<li>Spent time on ' + entry.name + ':\n' + temp_status_string + '\t</li>\n'

        for loop in entry.comment_list:
            if date.fromtimestamp(float(loop['time'])) == self.date:
                comment_modified_today = True
                temp_comment_string += '\t\t\t<li>' + time.strftime('`%H:%M:%S`',
                                                                    time.localtime(float(loop['time']))) + \
                                       loop['content'] + '</li>\n'
        temp_comment_string += '\t\t</ul>\n'
        if comment_modified_today is True:
            self.final_comment_string += '\t<li>Story about ' + entry.name + ':\n' + \
                                         temp_comment_string + '\t</li>\n'

    def generate_daily_digest(self):
        self.generate_daily_digest_header()
        if (self.final_status_string == '') & (self.final_comment_string == ''):
            self.final_string += '\n<h3><Nothing happened today./h3>'
        if self.final_status_string != '':
            self.final_string += '<h3>What I\'ve done today: </h3>\n'
            self.final_string += '\n<ul>\n' + self.final_status_string + '</ul>\n'
        if self.final_comment_string != '':
            self.final_string += '<h3>Diary: </h3>\n'
            self.final_string += '\n<ul>\n' + self.final_comment_string + '</ul>\n'
        self.final_string += self.meta
        self.write_out()

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