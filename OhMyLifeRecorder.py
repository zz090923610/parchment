import glob

__author__ = 'zhangzhao'

from optparse import OptionParser
import time
import os
import xml
from EntryElement import *
from AliasListControl import *
from MarkdownGenerator import *
from datetime import date


class FileOperator(object):
    def __init__(self):
        self.data_path = os.path.expanduser('~/OhMyLifeRecorderUserData')
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)
        self.digest_path = os.path.expanduser('~/OhMyLifeRecorderDigest')
        if not os.path.isdir(self.digest_path):
            os.mkdir(self.digest_path)
        self.current_job_path = ''
        self.current_job = EntryElement()

    def save_current_job_info(self):
        pass

    def read_current_job_info(self):
        pass

    def create_job(self, job_name):
        print(time.strftime('%Y-%m-%d, %H:%M:%S, new job ', time.localtime(time.time())) + job_name + ' is created')
        self.current_job_path = os.path.join(self.data_path, job_name + '.xml')
        if not os.path.isfile(self.current_job_path):
            os.popen('touch ' + self.current_job_path)
            category = input('specify to a category ')
            create_time = time.time()
            job_entry = EntryElement(job_name, category, 'created', create_time)
            job_entry.status_change_time = create_time
            print(job_entry)
            job_entry.save(self.current_job_path)
            alias_controller = AliasListControl()
            alias = 'alias job' + job_name + '=\'recorder -n' + \
                    job_name + '\'\n'
            alias_controller.add_alias(alias)

        else:
            print('Job named ' + job_name + ' already existed')

    def comment_a_job(self, job_name, comment):
        job_path = os.path.join(self.data_path, job_name + '.xml')
        tree = xml.etree.ElementTree.parse(job_path)
        root = tree.getroot()
        xml.etree.ElementTree.SubElement(root[1], 'comment_element',
                                         {'time': str(time.time()), 'content': comment})
        tree.write(job_path, encoding='utf-8')

    def init_recorder(self):
        self.__init__()
        alias_controler = AliasListControl()

    def suspend_job(self, name):
        job_path = os.path.join(self.data_path, name + '.xml')
        tree = xml.etree.ElementTree.parse(job_path)
        root = tree.getroot()
        status = None
        suspend_time = str(time.time())
        for it in root.iter('status'):
            status = it.text
            it.text = 'suspended'
        for it in root.iter('status_change_time'):
            it.text = suspend_time
        if status != 'suspended':
            xml.etree.ElementTree.SubElement(root[1], 'status_changed',
                                             {'from': status, 'to': 'suspended', 'time': suspend_time})
        tree.write(job_path, encoding='utf-8')
        self.read_current_job_info()
        if self.current_job.name == name:
            self.current_job = EntryElement()
        self.save_current_job_info()

    def proceeding_job(self, name):
        job_path = os.path.join(self.data_path, name + '.xml')
        tree = xml.etree.ElementTree.parse(job_path)
        root = tree.getroot()
        status_change_time = str(time.time())
        status = None
        for it in root.iter('status_change_time'):
            it.text = status_change_time
        for it in root.iter('status'):
            status = it.text
            it.text = 'proceeding'
        if status != 'proceeding':
            xml.etree.ElementTree.SubElement(root[1], 'status_changed',
                                             {'from': status, 'to': 'proceeding', 'time': status_change_time})
        tree.write(job_path, encoding='utf-8')
        self.read_current_job_info()
        if self.current_job.name == name:
            self.current_job = EntryElement()
            self.current_job.read_from_xml(job_path)
        elif (self.current_job.name != name) & (self.current_job.status == 'proceeding'):
            self.suspend_job(self.current_job.name)
            self.current_job = EntryElement()
            self.current_job.read_from_xml(job_path)
        self.save_current_job_info()

    def finalize_job(self, name):
        job_path = os.path.join(self.data_path, name + '.xml')
        tree = xml.etree.ElementTree.parse(job_path)
        root = tree.getroot()
        status = None
        finished_time = str(time.time())
        for it in root.iter('status'):
            status = it.text
            it.text = 'finished'
        for it in root.iter('status_change_time'):
            it.text = finished_time
        if status != 'finished':
            xml.etree.ElementTree.SubElement(root[1], 'status_changed',
                                             {'from': status, 'to': 'finished', 'time': finished_time})
        tree.write(job_path, encoding='utf-8')
        self.read_current_job_info()
        if self.current_job.name == name:
            self.current_job = EntryElement()
        self.save_current_job_info()

    def show_comments(self, name):
        job_path = os.path.join(self.data_path, name + '.xml')
        entry = EntryElement()
        entry.read_from_xml(job_path)
        print(entry)

    def dump_md_file(self, name):
        job_path = os.path.join(self.data_path, name + '.xml')
        entry = EntryElement()
        entry.read_from_xml(job_path)
        digest_path = os.path.join(self.digest_path, name + '.md')
        generator = MarkDownGenerator(os.path.expanduser(digest_path))
        generator.entry = entry
        generator.generate_process()

    def dump_daily_digest(self):
        date_today = date.fromtimestamp(time.time())
        os.chdir(self.data_path)
        file_name_list = glob.glob('*.xml')
        digest_path = os.path.join(self.digest_path, 'DailyDigest' + str(date_today) + '.md')
        generator = MarkDownGenerator(os.path.expanduser(digest_path),date_today)
        for a_file in file_name_list:
            job_path = os.path.join(self.data_path, a_file)
            entry = EntryElement()
            entry.read_from_xml(job_path)
            status_modified_today = False
            comment_modified_today = False
            for loop in entry.status_change_list:
                if date.fromtimestamp(float(loop['time'])) == date_today:
                    status_modified_today = True
                    break
            for loop in entry.comment_list:
                if date.fromtimestamp(float(loop['time'])) == date_today:
                    comment_modified_today = True
                    break
            if (comment_modified_today is True) | (status_modified_today is True):
                generator.generate_daily_digest_an_entry(entry)
        generator.generate_daily_digest()



    def show_daily_digest(self):
        print("============ What I've done today: ============")
        date_today = date.fromtimestamp(time.time())
        os.chdir(self.data_path)
        file_name_list = glob.glob('*.xml')
        final_status_string = ''
        final_diary_string = ''
        for a_file in file_name_list:
            (short_name, extension) = os.path.splitext(a_file)
            job_path = os.path.join(self.data_path, a_file)
            entry = EntryElement()
            entry.read_from_xml(job_path)
            temp_status_string = ''
            temp_comment_string = ''
            status_modified_today = False
            comment_modified_today = False
            for loop in entry.status_change_list:
                if date.fromtimestamp(float(loop['time'])) == date_today:
                    status_modified_today = True
                    temp_status_string += time.strftime('\t%H:%M:%S: ',
                                                        time.localtime(float(loop['time']))) + loop['to'] + '\n'
            if status_modified_today is True:
                final_status_string += 'Spent time on ' + short_name + ':\n' + temp_status_string
            for loop in entry.comment_list:
                if date.fromtimestamp(float(loop['time'])) == date_today:
                    comment_modified_today = True
                    temp_comment_string += time.strftime('\t%H:%M:%S: ', time.localtime(float(loop['time']))) + \
                                           loop['content'] +'\n'
            if comment_modified_today is True:
                final_diary_string += 'Comments about ' + short_name + ':\n' +\
                                      temp_comment_string

        print(final_status_string)
        print("====== What I wanted to remember today: ======")
        print(final_diary_string)


if __name__ == "__main__":
    file_operator = FileOperator()
    parser = OptionParser()
    parser.add_option('-c', '--create', action='store', type='string', dest='new_job_name',
                      help='create a new job you want to do')
    parser.add_option('-m', '--comment', action='store', type='string', dest='comment', help='comment a job')
    parser.add_option('-n', '--name', action='store', type='string', dest='name', help='specify a job name')
    parser.add_option('-i', '--init', action='store_true', dest='init', default=False,
                      help='initiate operation for the first time run')
    parser.add_option('-g', '--go', action='store_true', dest='go', default=False, help='start a job')
    parser.add_option('-p', '--suspend', action='store_true', dest='suspend', default=False, help='suspend a job')
    parser.add_option('-f', '--finalize', action='store_true', dest='finalize', default=False,
                      help='mark a job as finished')
    parser.add_option('-o', '--show', action='store_true', dest='show', default=False, help='show comments')
    parser.add_option('-d', '--dump', action='store_true', dest='dump', default=False,
                      help='specify a .md file path to generate a markdown format diary')
    (options, args) = parser.parse_args()
    if options.new_job_name is not None:
        file_operator.create_job(options.new_job_name)
    elif (options.name is not None) & (options.comment is not None):
        file_operator.comment_a_job(options.name, options.comment)
    elif options.init is True:
        file_operator.init_recorder()
    elif options.suspend is True:
        file_operator.suspend_job(options.name)
    elif (options.name is not None) & (options.go is True):
        file_operator.proceeding_job(options.name)
    elif (options.name is not None) & (options.finalize is True):
        file_operator.finalize_job(options.name)
    elif (options.name is not None) & (options.show is True):
        file_operator.show_comments(options.name)
    elif (options.name is not None) & (options.dump is True):
        file_operator.dump_md_file(options.name)
    elif (options.name is None) & (options.dump is True):
        file_operator.dump_daily_digest()
    elif (options.name is None) & (options.show is True):
        file_operator.show_daily_digest()
    else:
        pass
