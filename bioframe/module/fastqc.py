# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

from bioframe.core.flame import Module
import os

class Fastqc(Module):
    def __init__(self):
        Module.__init__(self)
        self.dict = dict()
        self.program = dict()

    @Module.dumpstatus
    def main(self):
        self.prepare()
        self.execute()

    @Module.dumpstatus
    def prepare(self):
        self.dict['fastq'] = self.operator.get_fastq_dict(self.path('fastq_dir'))
        self.program['fastqc'] = self.config('program', 'default', 'fastqc')
        self.set_path('outdir', os.path.join(self.path('cwd'), 'outdir'))
        os.makedirs(self.path('outdir'))
        self.executor.set(max_workers=int(self.config('module', 'fastqc', 'max_workers')))

    @Module.dumpstatus
    def execute(self):
        for sample, fastqs in self.dict['fastq'].items():
            for i, fastq in enumerate(fastqs):
                outdir = os.path.join(self.path('outdir'), sample)
                os.makedirs(outdir)
                name = 'fastqc_{}_{}'.format(sample, i)
                command = '{} -o {} {}'.format(self.program['fastqc'], outdir, fastq)
                self.executor.add_command(name, command)
        else:
            self.executor.run_command()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Analytical Framework Module for fastqc.')
    parser.add_argument('-i', dest='fastq_dir', type=str, help='input fastq directory', required=True)
    args = parser.parse_args()

    inst = Fastqc()
    inst.set_path('fastq_dir', args.fastq_dir, True)
    inst.main()
