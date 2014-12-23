import sys
from subprocess import call

file=sys.argv[1] #Input file
call(["idba_hybrid -r" + file + " -o"+" file_out"],shell=True)
call(["cd "+file+"_out"], shell=True)
call(["Sibelia -s loose " + file +" -o " + file+"_out"], shell=True)
