# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import importlib

Controller = getattr(importlib.import_module('src.core.element'), 'Controller')
Module = getattr(importlib.import_module('src.core.flame'), 'Module')

c = Controller()
mod1 = Module('m1')
mod2 = Module('m2')
mod3 = Module('m3')
mod4 = Module('m4')

c.add_event(mod1)
c.add_event(mod2)
c.add_event(mod3)
c.add_event(mod4)

c.add_dependency(mod2, [mod1])
c.add_dependency(mod3, [mod1, mod2])
c.add_dependency(mod4, [mod1])

c.act(['m1', 'm2'])

