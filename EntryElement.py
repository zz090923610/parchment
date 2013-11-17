__author__ = 'zhangzhao'
import time
from xml.etree import ElementTree as et


class EntryElement(object):
    def __init__(self, name='None', category='unspecified', status='None', create_time='None'):
        self.name = name
        self.create_time = create_time
        self.status_change_time = 0
        self.category = category
        self.status = status
        self.comment_list = []
        self.status_change_list = []
        self.tree = None
        self.root = None

    def __str__(self):
        result = 'Name: ' + self.name + '\nCategory: ' + self.category + '\nCreated time: ' + time.strftime(
            '%Y-%m-%d, %H:%M:%S ', time.localtime(self.create_time)) + '\nStatus: ' + self.status + ' since '+ time.strftime(
            '%Y-%m-%d, %H:%M:%S ', time.localtime(self.status_change_time))
        result += '\n***** Status change history *****'
        for loop in self.status_change_list:
            result += '\n\t' + time.strftime('%m-%d, %H:%M:%S: ',
                                             time.localtime(float(loop['time']))) + 'status changed from ' +\
                      loop['from'] + ' to ' + loop['to']
        result += '\n***** Comments *****'
        for loop in self.comment_list:
            result += '\n' + time.strftime('%m-%d, %H:%M:%S: ', time.localtime(float(loop['time']))) + loop['content']

        return result

    def save(self, path):
        self.generate_xml()
        self.tree.write(path, encoding='utf-8')
        #with open(path, mode='w', encoding='utf-8') as a_file:
        #   a_file.write(self.__str__())

    def dict_to_elem(self, dictionary, element_name):
        item = et.Element(element_name)
        for key in dictionary:
            field = et.Element(key.replace(' ', ''))
            field.text = dictionary[key]
            item.append(field)
        return item

    def generate_xml(self):
        self.root = et.Element('job_element')     # create the element first...
        self.tree = et.ElementTree(self.root)
        self.root.append(self.dict_to_elem(
            {'name': self.name, 'create_time': str(self.create_time), 'category': self.category, 'status': self.status,
             'status_change_time': str(self.status_change_time)},
            'meta'))
        self.root.append(self.dict_to_elem(self.comment_list, 'comments'))

    def read_from_xml(self, xml_path):
        tree = et.parse(xml_path)
        root = tree.getroot()
        for name in root.iter('name'):
            self.name = name.text
        for create_time in root.iter('create_time'):
            self.create_time = float(create_time.text)
        for category in root.iter('category'):
            self.category = category.text
        for status in root.iter('status'):
            self.status = status.text
        for status_change_time in root.iter('status_change_time'):
            self.status_change_time = float(status_change_time.text)
        for status_changed in root.iter('status_changed'):
            self.status_change_list.append(status_changed.attrib)
        for comment_element in root.iter('comment_element'):
            self.comment_list.append(comment_element.attrib)
