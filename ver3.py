#!/usr/bin/env python
"""
Creat on January 1, 2015
"""
__author__='Trung Huynh' 
__contact__= 'hmtrung.0110@gmail.com'
__version__='1.0'
__date__='01-01-2015'

import os, shutil, sys
from optparse import OptionParser
from subprocess import call

### Get all arguments data
parser = OptionParser()
# Choose idba or SPAdes
parser.add_option('-c', "--choose", type='choice', choices=['idba', 'spades'],
                  help="choose idba or spades to assembler", dest='choose')
# Import input files
parser.add_option('-f', '--file', action='store', dest='file_name', nargs=2, help='fastq input file(s) (2 files max)')
# Import reference files
parser.add_option('-r', '--ref', action='store', dest='ref_file', help='referrence file')
# Set output directory
parser.add_option("-o", "--output", dest = "out_dir", help='output directory')
options, args = parser.parse_args()


# Because idba and spades have different output contig file, so it is necessary to define a name for C-Sibelia input
contig_file=''
# IDBA block
def main():
    if options.choose == 'idba':
        # Convert from fastq files into fasta files and merge them:
        call(["fq2fa --merge --filter "+options.file_name[0]+" "+options.file_name[1]+" input.fa"], shell=True)
        
        # Run idba assembly
        call(["idba --read input.fa -o "+options.out_dir], shell=True)
        contig_file='contig.fa'

    #SPADes block
    if options.choose == "spades":
        # Run SPAdes to assembly two input files
        call(["python spades.py --pe1-1 "+options.file_name[0]
             +" --pe1-2 "+options.file_name[1]+" -o "+options.out_dir], shell=True)
        contig_file='contigs.fasta'

    # Sibelia block:
    # Move referrence file to output directory
    shutil.move(options.ref_file, options.out_dir)
    # Go to output directory
    os.chdir(options.out_dir)
    # Run C-Sibelia to find out variants
    call(["C-Sibelia.py "+options.ref_file+" "+contig_file], shell=True)
if __name__=='__main__':
    sys.exit(main())

        
        
