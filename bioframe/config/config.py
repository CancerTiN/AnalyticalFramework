# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import configparser
import os

class Config():
    def __init__(self):
        self._dir = os.path.dirname(__file__)
        self._configs = {
            'program': configparser.ConfigParser(),
            'script': configparser.ConfigParser()
        }
        for name in self._configs:
            self._load(name)

    def _load(self, name):
        filename = os.path.join(self._dir, '{}.ini'.format(name))
        self._configs[name].read(filename)

    def program(self, option, section='default'):
        config = self._configs['program']
        return config[section][option]

    def script(self, option, section='default'):
        config = self._configs['script']
        return config[section][option]

if __name__ == '__main__':
    c = Config()
    print(c.program('fastqc'))