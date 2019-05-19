# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from src.core.flame import Module
import configparser

class Fastqc(Module):
    def __init__(self, options):
        self._bind_object = dict()
        [{'name': 'raw_data', 'type': 'dir'}]

    def init_options(self, fmt_opts):
        pass

    def main(self, opts):
        cmd = '{} {}'.format(self.program('fastqc'))

    def bind(self, obj, key):
        self._bind_object[key] = obj

    def get(self, key):
        return self._bind_object[key]

    def stop(self):
        self._bind_object['event'].set()

class CallFastqc(io):
    def __init__(self):
        pass

if __name__ == '__main__':
    fastqc = CallFastqc()
