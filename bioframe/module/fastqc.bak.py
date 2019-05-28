# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from bioframe.core.flame import Module
from bioframe.core.element import IO
import os
import shutil
from collections import OrderedDict
import configparser

class Fastqc(Module):
    def __init__(self, options):
        Module.__init__(self)
        self.def_io(IO([
            {'name': 'fastq_dir', 'type': 'dir'},
            {'name': 'out_dir', 'type': 'dir'}
        ]), options)

    def main(self):
        self.bind(dict, 'fastq', self.object('operator').get_fastq_dict(self.io('fastq_dir')))
        self.bind(dict, 'command', self.prepare_command())
        self.object('executor')._run(self.dict('command'),
                                     int(self.object('config').argument('max_workers')))

    def prepare_command(self):
        if os.path.isdir(self.io('out_dir')):
            shutil.rmtree(self.io('out_dir'))
        os.makedirs(self.io('out_dir'))
        cmds = OrderedDict()
        for k, v in self.dict('fastq').items():
            outdir = os.makedirs(os.path.join(self.io('out_dir'), k))
            for n, fastq in enumerate(v):
                cmds['fastqc_{}_{}'.format(k, n)] = '{} -o {} {}'.format(
                    self.object('config').program('fastqc'), outdir, fastq
                )
        else:
            return cmds


    def main(self, opts):
        cmd = '{} {}'.format(self.program('fastqc'))

    # def bind(self, obj, key):
    #     self._bind_object[key] = obj

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