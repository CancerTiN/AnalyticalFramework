# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')
print('config: {}'.format(conf))

sections = conf.sections()
print('sections: {}'.format(sections))

options = conf.options('sequence')
print('options("sequence"): {}'.format(options))

items = conf.items('mysql')
print('items("mysql"): {}'.format(items))

sequence_type = conf.get('sequence', 'type')
print('sequence_type: {}'.format(sequence_type))

setting = dict(conf.items('setting'))
sem = setting['sem']
print('setting sem value: {}'.format(sem))
print('setting sem type: {}'.format(type(sem)))