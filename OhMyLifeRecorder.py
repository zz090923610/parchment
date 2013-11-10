__author__ = 'zhangzhao'

from optparse import OptionParser
import time
import os
from EntryElement import *


class FileOperator(object):
    def __init__(self):
        self.data_path = None
        self.init_data_path()
        self.current_job_path = ''

    def create_job(self, job_name):
        print(time.strftime('%Y-%m-%d, %H:%M:%S, new job ', time.localtime(time.time())) + job_name + ' is created')
        self.current_job_path = os.path.join(self.data_path, job_name)
        #print(self.current_job_path)
        if not os.path.isfile(self.current_job_path):
            os.popen('touch ' + self.current_job_path)
            print(type(self.current_job_path))
            category = input('specify to a category ')
            create_time = time.localtime(time.time())
            job_entry = EntryElement(job_name, category, 'created', create_time)
            print(job_entry)

            job_entry.save(self.current_job_path)
        else:
            print('Job named ' + job_name + ' already existed')

    def init_data_path(self, data_path=os.path.expanduser('~/OhMyLifeRecorderUserData')):
        self.data_path = data_path
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)


if __name__ == "__main__":
    file_operator = FileOperator()
    parser = OptionParser()
    parser.add_option('-c', '--create', action='store', type='string', dest='new_job_name',
                      help='create a new job you want to do')
    #parser.add_option('-l', '--list', action='store_true', dest='list', help='user account')
    #parser.add_option('-a', '--adapter', action='store', type='string', dest='adapter',
    #                 help='specify which network adapter to use')
    (options, args) = parser.parse_args()
    #if (options.user is not None) & (options.adapter is not None):
    #   options.mode = False
    if options.new_job_name is not None:
        file_operator.create_job(options.new_job_name)
    else:
        #print("None")
        pass
