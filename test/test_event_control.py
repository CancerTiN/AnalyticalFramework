# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import gevent
from gevent.event import Event

class Class1():
    def __init__(self, wait_events, set_events):
        self.w_evt = wait_events
        self.s_evt = set_events

    def start(self):
        for e in self.w_evt:
            e.wait()
        else:
            print('{} is start'.format(self.__class__.__name__))
            self.run()

    def run(self):
        for i in range(4):
            print('{} is running'.format(self.__class__.__name__))
            gevent.sleep(1)
        else:
            self.stop()

    def stop(self):
        for e in self.s_evt:
            e.set()
        else:
            print('{} is stop'.format(self.__class__.__name__))

class Class2():
    def __init__(self, wait_events, set_events):
        self.w_evt = wait_events
        self.s_evt = set_events

    def start(self):
        for e in self.w_evt:
            e.wait()
        else:
            print('{} is start'.format(self.__class__.__name__))
            self.run()

    def run(self):
        for i in range(7):
            print('{} is running'.format(self.__class__.__name__))
            gevent.sleep(1)
        else:
            self.stop()

    def stop(self):
        for e in self.s_evt:
            e.set()
        else:
            print('{} is stop'.format(self.__class__.__name__))

class Class3():
    def __init__(self, wait_events, set_events):
        self.w_evt = wait_events
        self.s_evt = set_events

    def start(self):
        for e in self.w_evt:
            e.wait()
        else:
            print('{} is start'.format(self.__class__.__name__))
            self.run()

    def run(self):
        for i in range(5):
            print('{} is running'.format(self.__class__.__name__))
            gevent.sleep(1)
        else:
            self.stop()

    def stop(self):
        for e in self.s_evt:
            e.set()
        else:
            print('{} is stop'.format(self.__class__.__name__))

class Class4():
    def __init__(self, wait_events, set_events):
        self.w_evt = wait_events
        self.s_evt = set_events

    def start(self):
        for e in self.w_evt:
            e.wait()
        else:
            print('{} is start'.format(self.__class__.__name__))
            self.run()

    def run(self):
        for i in range(2):
            print('{} is running'.format(self.__class__.__name__))
            gevent.sleep(1)
        else:
            self.stop()

    def stop(self):
        for e in self.s_evt:
            e.set()
        else:
            print('{} is stop'.format(self.__class__.__name__))

def main():

    evta = Event()
    evtb = Event()
    evtc = Event()
    evtd = Event()
    evte = Event()
    evtf = Event()
    evtg = Event()

    c1 = Class1([evta, evtb], [evtc, evtd, evte])
    c2 = Class2([evta, evte], [evtf])
    c3 = Class3([evtd], [evtg])
    c4 = Class4([evtf, evtg], [])

    def set_event():
        print('finish gevent.joinall')
        gevent.sleep(1)
        evta.set()
        print('set evta')
        gevent.sleep(1)
        evtb.set()
        print('set evtb')

    func = lambda e: e.set()

    gevent.joinall([
        gevent.spawn(lambda e: e.set(), evta),
        gevent.spawn(c1.start),
        gevent.spawn(c2.start),
        gevent.spawn(c3.start),
        gevent.spawn(c4.start),
        gevent.spawn(func, evtb),
    ])

if __name__ == '__main__':
    main()
