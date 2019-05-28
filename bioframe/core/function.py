# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

import os
import subprocess
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

class Operator:
    def __init__(self):
        pass

    def get_fastq_dict(self, fastq_dir):
        list_file = os.path.join(fastq_dir, 'list.txt')
        fastq_dict = dict()
        for line in open(list_file):
            items = line.strip().split('\t')
            if len(items) == 2:
                fastq_dict[items[1]] = [os.path.join(fastq_dir, items[0])]
            elif len(items) == 3:
                if items[1] not in fastq_dict:
                    fastq_dict[items[1]] = [os.path.join(fastq_dir, items[0])]
                elif items[2] == 'l':
                    fastq_dict[items[1]] = [os.path.join(fastq_dir, items[0])] + fastq_dict[items[1]]
                elif items[2] == 'r':
                    fastq_dict[items[1]] = fastq_dict[items[1]] + [os.path.join(fastq_dir, items[0])]
        else:
            return fastq_dict

class Executor:
    def __init__(self):
        self._command = dict()
        self._done = set()
        self._max_workers = 4

    def set(self, **kwargs):
        if 'max_workers' in kwargs:
            self._max_workers = int(kwargs['max_workers'])

    def add_command(self, name, command):
        if name in self._command:
            raise Exception('ERROR: can not add command with same name ({}) repeatedly'.format(name))
        else:
            self._command[name] = command

    def run_command(self, path=None):
        commands = dict((name, command) for name, command in self._command.items() if name not in self._done)
        path = path if path else os.getcwd()
        ret = self._run(commands, self._max_workers, path)

    def _run(self, commands: dict, max_workers: int, path: str):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_command = {executor.submit(self._execute_command, name, command, path): (name, command)
                                 for name, command in commands.items()}
            for future in concurrent.futures.as_completed(future_to_command):
                name, command = future_to_command[future]
                try:
                    data = future.result()
                except:
                    raise Exception('ERROR: command ({}) generated at {}'.format(name, future))
                else:
                    fmtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print('{} INFO: {} is done and return {}'.format(fmtime, name, data))
                    self._done.add(name)
        return True

    def _execute_command(self, name, command, path):
        os.chdir(path)
        proc = subprocess.Popen(
            command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        retcode = proc.wait()
        outs, errs = proc.communicate()
        open('{}.out'.format(name), 'wb').write(outs)
        open('{}.err'.format(name), 'wb').write(errs)
        if retcode:
            raise Exception('ERROR: fail to excecute -> {} (returncode {})'.format(command, retcode))
        else:
            fmtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('{} INFO: succeed in executing -> {}'.format(fmtime, command))
            return True
