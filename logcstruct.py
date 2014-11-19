#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

sfile = './s.h'
tfile = './t.h'

class Field:

    def __init__(self, type, en_name, cn_name):
        self.type = type
        self.en_name = en_name
        self.cn_name = cn_name

    def print_field(self):
        format = {'string':'%s', 'int':'%d', 'long':'%ld','double':'%.4f', 'float':'%.4f', 'short': '%d', 'char':'%c'}
        print '\tdlogInfo("\t' + self.en_name + '(' + self.cn_name + '):[' + format[self.type] + ']", s->' + self.en_name + ');'

def type_list():
    f = file(tfile, 'r');
    types = {}
    for line in f:
        line = line.replace('\n', '')
        if line.startswith('typedef'):
            if line.find('enum') != -1:
                continue
            c = line.split(' ')
            type = c[1];
            name = c[2]
            if name.find('[') != -1:
                type = 'string'
            name = re.sub('[0-9]','', name)
            name = name.replace(';', '')
            name = name.replace('[', '')
            name = name.replace(']', '')
            types[name] = type
    return types;

types = type_list();
f = file(sfile, 'r');
prev_line = ''
struct_name = ''
for line in f:
    line = line.replace('\n','');
    if line.startswith('typedef struct {'):
        field_list = []
        continue
    elif line.find('}')  != -1:
        c = line.split(' ');
        struct_name = c[1].replace(';','');
        func_name = 'void log' + struct_name.replace('Field','') + '(' + struct_name + ' *s)'

        print func_name + ';';

        print func_name + ' {'
        print '\tdlogInfo("start ' + struct_name + ' log:");'
        for field in field_list:
            field.print_field()
        print '\tdlogInfo("end ' + struct_name + ' log.");'
        print '}'
    elif line.find('Type')  != -1:
        c = line.split('\t');
        type = c[0].replace(' ','');
        name = c[1];
        real_type = types[type];
        cn_name = prev_line.replace('///','')
        cn_name = cn_name.replace(' ','')
        cn_name = cn_name.replace('\t', '')
        en_name = name.replace(';', '')
        field = Field(real_type, en_name, cn_name)
        field_list.append(field)
    else:
        prev_line = line
