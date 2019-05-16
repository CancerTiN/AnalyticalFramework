# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from gevent.event import Event
import gevent

class Option():
    def __init__(self):
        pass

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
