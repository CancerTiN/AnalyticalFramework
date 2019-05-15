# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import gevent
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore

sem = BoundedSemaphore(3)

def worker1(n):
    sem.acquire()
    print('Worker %i acquired semaphore' % n)
    gevent.sleep(1)
    sem.release()
    print('Worker %i released semaphore' % n)

pool = Pool()
pool.map(worker1, range(0, 10))
