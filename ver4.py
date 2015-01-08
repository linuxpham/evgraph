#!/usr/bin/env python
"""
Creat on January 8, 2015
"""
__author__='Trung Huynh' 
__contact__= 'hmtrung.0110@gmail.com'
__version__='1.0'
__date__='01-01-2015'

"""
This tool is aimed to make a pipeline for user to use easily and automatically.
Users only need to supply the fastq input files and choose whether idba or spased to assembly.
The tool will use C-Sibelia to find variants from assembly genome and reference genome
and the results can be summarised by snpEff.
"""


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
# SnpEff option
parser.add_option("-s", "--snpeff", action = 'store_true', dest='snpeff', help='Make varian summary by snpEff') )
# Set output directory
parser.add_option("-o", "--output", dest = "out_dir", help='output directory')

options, args = parser.parse_args()



# Because idba and spades have different output contig file, so it is necessary to define a name for C-Sibelia input
CONTIG_FILE=''

# snpEff
def snpEff(ref_file):
    # Find name of the reference genome to find database in snpEff.config
    FIRST_LINE=open(ref_file).readline()
    TEMP=[]
    for i in range(1, len(FIRST_LINE)):
        if FIRST_LINE[i]=='|': # Find positions of letter '|'
            TEMP.append(i)
    NAME=FIRST_LINE[TEMP[2]+1:TEMP[3]-2] # Genome's name is between the third '|' and forth '|'
    # Find name of genome in database:
    DATABASE=open('snpEff.config').readlines()
    LIB=''
    for i in range(1, len(DATABASE)):
        if DATABASE[i].find(NAME)!=-1:
            LIB=DATABASE[i][0:DATABASE[i].find('.')] # The name of used database is the part before '.genome'
	    break
    if LIB!='':
	print('Downloading database for snpEff. Please wait...')
        call(['java -jar snpEff.jar '+LIB+' variant.vcf > variant.eff.vcf'], shell=True)
    else: print('Unsupported database, snpEff need database to execute!')
    return

# IDBA block
def main():
    if options.choose == 'idba':
        # Convert from fastq files into fasta files and merge them:
        call(["fq2fa --merge --filter "+options.file_name[0]+" "+options.file_name[1]+" input.fa"], shell=True)
        
        # Run idba assembly
        call(["idba --read input.fa -o "+options.out_dir], shell=True)
        CONTIG_FILE='contig.fa'

    #SPADes block
    if options.choose == "spades":
        # Run SPAdes to assembly two input files
        call(["python spades.py --pe1-1 "+options.file_name[0]
             +" --pe1-2 "+options.file_name[1]+" -o "+options.out_dir], shell=True)
        CONTIG_FILE='contigs.fasta'

    # Sibelia block:
    # Move referrence file to output directory
    shutil.copy(options.ref_file, options.out_dir)
    shutil.move('snpEff', options.out_dir)
    # Go to output directory
    os.chdir(options.out_dir)
    # Run C-Sibelia to find out variants
    call(["C-Sibelia.py "+options.ref_file+" "+CONTIG_FILE], shell=True)
    if options.snpeff == True:
        # Copy variant.vcf file to snpEFF dir
        shutil.move('variant.vcf', 'snpEff')
        shutil.move(options.ref_file, 'snpEff')
        # Run snpEff
        os.chdir('snpEff')
        snpEff(options.ref_file)
    print('Operation is finished. Thank you...')


if __name__=='__main__':
    sys.exit(main())

        
        
