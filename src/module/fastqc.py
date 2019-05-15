# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from src.core.flame import Module
import configparser

class Fastqc(Module):
    def __init__(self, options):

        [{'name': 'raw_data', 'type': 'dir'}]

    def init_options(self, fmt_opts):
        pass
