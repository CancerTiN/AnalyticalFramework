# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

class A:
    def __init__(self):
        print('Here is class A')
        print(self.foo)

class B(A):
    def __init__(self):
        print('Here is class B')
        self.foo = 'Can you see me?'
        A.__init__(self)

class C(A):
    def __init__(self):
        print('Here is class C')
        A.__init__(self)
        self.foo = 'Can you see me?'

if __name__ == '__main__':
    inst = B()
    try:
        inst = C()
    except Exception as e:
        print(e)
    finally:
        print('superclass can not call a variable in subclass before that is defined')
