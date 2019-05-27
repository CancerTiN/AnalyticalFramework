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
        pass

    def execute_command(self, name, command, path):
        os.chdir(path)
        proc = subprocess.Popen(
            command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        retcode = proc.wait()
        outs, errs = proc.communicate()
        open('{}.out'.format(name), 'w').write(outs)
        open('{}.err'.format(name), 'w').write(errs)
        if retcode:
            raise Exception('ERROR: fail to excecute -> {} (returncode {})'.format(command, retcode))
        else:
            print('INFO: succeed in executing -> {}'.format(command))

    def parallel_thread(self, commands: dict, max_workers: int, path: str):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_command = {executor.submit(self.execute_command, name, command, path): command
                                 for name, command in commands.items()}
            for future in concurrent.futures.as_completed(future_to_command):
                command = future_to_command[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('{} generated an exception: {}'.format(command, exc))
                else:
                    print('{} is done and return {} bytes'.format(command, len(data)))
        return True