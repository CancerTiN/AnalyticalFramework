# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from src.core.flame import Workflow

class ChipSeq(Workflow):
    def __init__(self, cfg_file):
        Workflow.__init__(self, cfg_file)

    def set_class(self):
        self.set_fastqc()

    def set_fastqc(self):
        Fastqc = self.add_class('module', 'fastqc', 'Fastqc')
        self.module_fastqc = Fastqc()

    def set_logic(self):
        self.set_event(self.module_fastqc, 'begin')
