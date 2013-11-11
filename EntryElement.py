__author__ = 'zhangzhao'
import time
from xml.etree import ElementTree as et


class EntryElement(object):
    def __init__(self, name='None', category='unspecified', status='None', create_time='None'):
        self.name = name
        self.create_time = create_time
        self.finish_time = 0
        self.category = category
        self.status = status
        self.comment_list = {}
        self.tree = None
        self.root = None

    def __str__(self):
        result = 'Name: ' + self.name + '\nCategory: ' + self.category + '\nCreated time: ' + time.strftime(
            '%Y-%m-%d, %H:%M:%S ', self.create_time) + '\nStatus: ' + self.status
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
            {'name': self.name, 'create_time': str(self.create_time), 'category': self.category, 'status': self.status},
            'meta'))
        self.root.append(self.dict_to_elem(self.comment_list, 'comments'))
