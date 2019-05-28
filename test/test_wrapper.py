# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

def timethis(func):
    def wrapper(*args, **kwargs):
        print('INFO: begin of the function ({}) at {}'.format(func.__name__, __name__))
        result = func(*args, **kwargs)
        print('INFO: final of the function ({}) at {}'.format(func.__name__, __name__))
        return result
    return wrapper

class Test:
    @staticmethod
    def timethis(func):
        def wrapper(*args, **kwargs):
            print(dir(func))
            for i in dir(func):
                print('{} -> {}'.format(i, getattr(func, i)))
            print('INFO: begin of the function ({}) at {}'.format(func.__name__, func))
            result = func(*args, **kwargs)
            print('INFO: final of the function ({}) at {}'.format(func.__name__, func))
            return result

        return wrapper

class Count:
    @Test.timethis
    def countdown(self, n):
        while n> 0:
            n -= 1

if __name__ == '__main__':
    c = Count()
    c.countdown(1000)
