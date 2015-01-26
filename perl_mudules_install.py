#!/usr/bin/env python
'''
This will install automatically perl modules which circos needs to execute.
'''
from subprocess import call

MODULES=open('perl_modules.txt').readlines()
for i in range(0, len(MODULES)):
    call(['perl -MCPAN -e \'install '+MODULES[i]+'\''], shell=True)
print('---------------------------------------------------------')
print('Finish installing perl modules')
    
