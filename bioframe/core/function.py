# -*- coding: utf-8 -*-
# __author__ = 'qinjincheng'

class Operator:
    '''
    opr
    '''
    def __init__(self):
        pass

    def get_fastq_dir_info(self, fastq_dir):
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
    '''
    exe
    '''
    def __init__(self):
        pass

