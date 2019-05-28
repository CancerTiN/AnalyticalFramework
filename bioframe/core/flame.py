# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import os
import configparser
import importlib
import gevent
from gevent.lock import BoundedSemaphore
from gevent.pool import Pool
from collections import defaultdict
from bioframe.config.config import Config
import datetime
import random
from bioframe.core.function import Operator
from bioframe.core.function import Executor
import pickle

class Workflow():
    def __init__(self, cfg_file):
        if os.path.isfile(cfg_file):
            self._cfg_file = cfg_file
            self._init_cfg()
        else:
            raise FileNotFoundError('ERROR: can not find {}'.format(cfg_file))
        self._setting = dict(self.config.items('setting'))
        if 'sem' in self._setting and self._setting['sem'].isdigit():
            self._sem = BoundedSemaphore(int(self._setting['sem']))
            self._pool = Pool()
        self._events = dict()
        self._node_events = {'begin': list(), 'final': list()}

    def _init_cfg(self):
        self._cfg = configparser.ConfigParser()
        self._cfg.read(self._cfg_file)
        if 'setting' not in self._cfg.sections():
            raise KeyError('ERROR: can not find setting section in {}'.format(cfg_file))

    @property
    def config(self):
        return self._cfg

    def add_class(self, c_kind, c_file, c_name):
        module_path = 'src.{}.{}'.format(c_kind, c_file)
        module = importlib.import_module(module_path)
        c_class = getattr(module, c_name)
        if c_kind == 'module':
            importlib.import_module()
            pass

    def set_event(self, e_func, e_type=None):
        self._check_event(e_func)
        if not e_type:
            pass
        elif e_type in ['begin', 'final']:
            self._node_events[e_type].append(e_func.name)
        else:
            raise ValueError('ERROR: find unsupported event type -> {}'.format(e_type))

    def _check_event(self, e_func):
        if e_func.name in self._events:
            raise KeyError('ERROR: do not allow add repeating event -> {}'.format(e_func.name))
        else:
            self._events.update({e_func.name: e_func})

    @property
    def events(self, e_type):
        if e_type in ['begin', 'final']:
            return [self._events[e_name] for e_name in self._node_events[e_type]]

    def activate(self, e_func):
        e_func.run()

    def run(self, check=True):
        self._pool.map(self.activate, self.events('begin'))

class Module():
    def __init__(self):
        self._name = self.__class__.__name__.lower()
        self._config = Config()
        self._path = dict()
        self.set_path('workspace', self.config('module', 'path', 'workspace'))
        self.set_path('cwd', os.path.join(self.path('workspace'), datetime.datetime.now().strftime('%Y%m%d'),
            'module.{}.{}'.format(self._name, datetime.datetime.now().strftime('%H%M%S'))))
        os.makedirs(self.path('cwd'))
        os.chdir(self.path('cwd'))
        self._operator = Operator()
        self._executor = Executor()

    def config(self, name, section, option):
        return self._config.get(name, section, option)

    def set_path(self, name, path, check=False):
        if check:
            if not os.path.exists(path):
                raise Exception('ERROR: can not find {}'.format(path))
        self._path.update({name: path})

    def path(self, name):
        return self._path[name]

    @property
    def name(self):
        return self._name

    @property
    def operator(self):
        return self._operator

    @property
    def executor(self):
        return self._executor

    @staticmethod
    def dumpstatus(func):
        def wrapper(*args, **kwargs):
            begin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('{} INFO: begin of the function ({})'.format(begin_time, func.__qualname__))
            pickle.dump(True, open('{}.status.pk'.format(func.__qualname__), 'wb'))
            result = func(*args, **kwargs)
            pickle.dump(True, open('{}.status.pk'.format(func.__qualname__), 'wb'))
            final_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('{} INFO: final of the function ({})'.format(final_time, func.__qualname__))
            return result
        return wrapper


    #     self._str = defaultdict(str)
    #     self._list = defaultdict(list)
    #     self._dict = defaultdict(dict)
    #     self._object = defaultdict(object)
    #     self.bind(object, 'config', Config())
    #     self.bind(object, 'operator', Operator())
    #     self.bind(object, 'executor', Executor())
    #
    # def bind(self, cls, key, val):
    #     {str: self._str, list: self._list, dict: self._dict, object: self._object}[cls][key] = val
    #
    # @property
    # def str(self, key):
    #     return self._str[key]
    #
    # @property
    # def list(self, key):
    #     return self._list[key]
    #
    # @property
    # def dict(self, key):
    #     return self._dict[key]
    #
    # @property
    # def object(self, key):
    #     return self._object[key]
    #
    # def def_io(self, io_object, options):
    #     self.bind(object, 'io', io_object)
    #     self.object('io').set(options)
    #
    # @property
    # def io(self, name):
    #     path = self.object('io').get(name)
    #     return path
    #
    # @property
    # def name(self):
    #     return self._name
    #
    # # def bind(self, obj, key):
    # #     self._bind_object[key] = obj
    #
    # def get(self, key):
    #     return self._bind_object[key]
    #
    # def stop(self):
    #     self._bind_object['event'].set()
    #     print('{} is stop'.format(self.name))
    #
    # def run(self):
    #     for i in range(3):
    #         gevent.sleep(1)
    #         print('{} is running'.format(self.name))
    #     else:
    #         self.stop()