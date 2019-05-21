# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from src.core.flame import Module
from src.core.element import IO
import configparser

class Fastqc(Module):
    def __init__(self, options):
        self._io_object = IO([
            {'name': 'fastq_dir', 'type': 'dir'},
            {'name': 'out_dir', 'type': 'dir'}
        ])
        Module.__init__(self, options)

    def init_options(self, fmt_opts):
        pass

    def main(self, opts):
        cmd = '{} {}'.format(self.program('fastqc'))

    def bind(self, obj, key):
        self._bind_object[key] = obj

    def get(self, key):
        return self._bind_object[key]

    def stop(self):
        self._bind_object['event'].set()

def main():
    options = {'raw_data': ''}
    fastqc = Fastqc(options)
    pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Analytical Framework Module for fastqc.')
    parser.add_argument('-i', dest='fastq_dir', type=str, help='input fastq directory', required=True)
    parser.add_argument('-o', dest='out_dir', type=str, help='output result directory', required=True)
    args = parser.parse_args()

    opts = {'fastq_dir': args.fastq_dir, 'out_dir': args.out_dir}
    inst = Fastqc(opts)