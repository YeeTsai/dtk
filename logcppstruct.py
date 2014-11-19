#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

sfile = './s.h'

class Field:

    def __init__(self, en_name, cn_name):
        self.en_name = en_name
        self.cn_name = cn_name

    def print_field(self):
        print '\tVLOG(_level) << "\t' + self.en_name + '(' + self.cn_name + '):[" << ' + "_s->" + self.en_name + ' << "]";'

f = file(sfile, 'r');
prev_line = ''
struct_name = ''
for line in f:
    line = line.replace('\n','');
    if line.startswith('struct CThostFtdc'):
        field_list = []
        c = line.split(' ');
        struct_name = c[1];
    elif line.find('}')  != -1:
        func_name = 'void log' + struct_name.replace('Field','').replace('CThostFtdc','') + '(int _level, ' + struct_name + ' *_s)'

        print func_name + ';';

        print func_name + ' {'
        print '\tVLOG(_level) << "start log' + struct_name + ':";'
        for field in field_list:
            field.print_field()
        print '\tVLOG(_level) << "end log' + struct_name + '.";'
        print '}'
    elif line.find('TThostFtdc') != -1:
        c = line.split('\t');
        name = c[2];
        cn_name = prev_line.replace('///','')
        cn_name = cn_name.replace(' ','')
        cn_name = cn_name.replace('\t', '')
        en_name = name.replace(';', '')
        field = Field(en_name, cn_name)
        field_list.append(field)
    else:
        prev_line = line
