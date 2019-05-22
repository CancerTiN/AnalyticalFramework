# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import os
from gevent.event import Event
import gevent

class IO():
    def __init__(self, records):
        self._options = dict()
        self._check_funcs = dict()
        self._process_records(records)

    def _process_records(self, records: list):
        for dct in records:
            self._options[dct['name']] = {'type': dct['type']}
            self._check_funcs[dct['name']] = {'file': os.path.isfile, 'dir': os.path.isdir}[dct['type']]

    def set(self, name2path: dict):
        for name, path in name2path.items():
            check_func = self._check_funcs[name]
            if check_func(path):
                self._options[name]['path'] = os.path.abspath(path)
            else:
                raise FileNotFoundError('ERROR: can not find {}'.format(path))

    @property
    def get(self, name: str):
        return self._options[name]['path']

class Controller():
    def __init__(self):
        self.events = dict()
        self.modules = dict()

    def add_event(self, module):
        name = module.name
        self.events.update({name: Event()})
        self.modules.update({name: module})
        module.bind(self.events[name], 'event')

    def add_dependency(self, module, dependent_modules):
        module.bind([m.get('event') for m in dependent_modules], 'dependency')

    def start(self, module):
        for e in module.get('dependency'):
            e.wait()
        else:
            module.run()

    def act(self, module_names=None):
        if module_names:
            modules = [self.modules[n] for n in module_names]
        else:
            modules = self.modules.values()
        greenlets = [gevent.spawn(self.start, module) for module in modules]
        gevent.joinall(greenlets)
