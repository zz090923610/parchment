import subprocess

__author__ = 'zhangzhao'

from optparse import OptionParser
import time
import os
import xml
from EntryElement import *
from AliasListControl import *


class FileOperator(object):
    def __init__(self):
        self.data_path = None
        self.init_data_path()
        self.current_job_path = ''
        self.current_job = EntryElement()

    def save_current_job_info(self):
        pass

    def read_current_job_info(self):
        pass

    def create_job(self, job_name):
        print(time.strftime('%Y-%m-%d, %H:%M:%S, new job ', time.localtime(time.time())) + job_name + ' is created')
        self.current_job_path = os.path.join(self.data_path, job_name)
        if not os.path.isfile(self.current_job_path):
            os.popen('touch ' + self.current_job_path)
            print(type(self.current_job_path))
            category = input('specify to a category ')
            create_time = time.time()
            job_entry = EntryElement(job_name, category, 'created', create_time)
            print(job_entry)
            job_entry.save(self.current_job_path)
            alias_controller = AliasListControl()
            alias = 'alias job' + job_name + '=\'python3 ~/PycharmProjects/OhMyLifeRecorder/OhMyLifeRecorder.py -n' + \
                    job_name + '\'\n'
            alias_controller.add_alias(alias)
            self.refresh_aliases()

        else:
            print('Job named ' + job_name + ' already existed')

    def comment_a_job(self, job_name, comment):
        job_path = os.path.join(self.data_path, job_name)
        tree = xml.etree.ElementTree.parse(job_path)
        root = tree.getroot()
        xml.etree.ElementTree.SubElement(root[1], 'comment_element',
                                         {'time': str(time.time()), 'content': comment})
        tree.write(job_path, encoding='utf-8')

    def start_recorder(self):
        alias_controller = AliasListControl()
        os.popen('cp ~/.bash_aliases ~/.bash_aliases.bak')
        os.popen('cat ' + alias_controller.path + '>> ~/.bash_aliases')

    def stop_recorder(self):
        os.popen('mv ~/.bash_aliases.bak ~/.bash_aliases')

    def suspend_job(self, name):
        job_path = os.path.join(self.data_path, name)
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
        job_path = os.path.join(self.data_path, name)
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
        job_path = os.path.join(self.data_path, name)
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

    def refresh_aliases(self):
        self.stop_recorder()
        self.start_recorder()

    def init_data_path(self, data_path=os.path.expanduser('~/OhMyLifeRecorderUserData')):
        self.data_path = data_path
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)


if __name__ == "__main__":
    file_operator = FileOperator()
    parser = OptionParser()
    parser.add_option('-c', '--create', action='store', type='string', dest='new_job_name',
                      help='create a new job you want to do')
    parser.add_option('-m', '--comment', action='store', type='string', dest='comment', help='comment a job')
    parser.add_option('-n', '--name', action='store', type='string', dest='name', help='specify a job name')
    parser.add_option('-s', '--start', action='store_true', dest='start', default=False,
                      help='start last suspended job and add alias')
    parser.add_option('-k', '--kill', action='store_true', dest='kill', default=False,
                      help='Stop Recorder and restore alias')
    parser.add_option('-g', '--go', action='store_true', dest='go', default=False, help='start a job')
    parser.add_option('-p', '--suspend', action='store_true', dest='suspend', default=False, help='suspend a job')
    parser.add_option('-f', '--finalize', action='store_true', dest='finalize', default=False,
                      help='mark a job as finished')
    (options, args) = parser.parse_args()
    if options.new_job_name is not None:
        file_operator.create_job(options.new_job_name)
    elif (options.name is not None) & (options.comment is not None):
        file_operator.comment_a_job(options.name, options.comment)
    elif options.start is True:
        file_operator.start_recorder()
    elif options.kill is True:
        file_operator.stop_recorder()
    elif options.suspend is True:
        file_operator.suspend_job(options.name)
    elif (options.name is not None) & (options.go is True):
        file_operator.proceeding_job(options.name)
    elif (options.name is not None) & (options.finalize is True):
        file_operator.finalize_job(options.name)
    else:
        pass
