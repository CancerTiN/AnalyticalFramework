# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import configparser
import os

class Config():
    def __init__(self):
        self._dir = os.path.dirname(__file__)
        self._configs = dict()

    def _load(self, name):
        filename = os.path.join(self._dir, '{}.ini'.format(name))
        if name in self._configs:
            pass
        else:
            self._configs.update({name: configparser.ConfigParser()})
            self._configs[name].read(filename)
        return self._configs[name]

    def get(self, name, section, option):
        config = self._load(name)
        if section in config.sections():
            if option in config.options(section):
                return config.get(section, option)
            else:
                raise Exception('ERROR: can not find {} in {} at config {}'.format(option, section, name))
        else:
            raise Exception('ERROR: can not find {} at config {}'.format(section, name))
    #
    #
    # def program(self, option, section='default'):
    #     config = self._configs['program']
    #     return config[section][option]
    #
    # def script(self, option, section='default'):
    #     config = self._configs['script']
    #     return config[section][option]

if __name__ == '__main__':
    c = Config()
    print(c.program('fastqc'))