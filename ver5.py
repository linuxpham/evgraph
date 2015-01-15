#!/usr/bin/env python
"""
Creat on January 1, 2015
"""
__author__='Trung Huynh' 
__contact__= 'hmtrung.0110@gmail.com'
__version__='1.0'
__date__='15-01-2015'

"""
The tool aims to create a pipeline for some genomic tools comprising SPAdes assembler, idba assembler, snpEff and Sibelia.
The input files are in fastq format, maximum number of files is 2 and the tool supports paired-end and unpaired reads.
Users can chose whether idba or SPAdes to assembly the input files, after that, you can use Sibelia to find synteny blocks of
genome. With the reference file, Sibelia tool also hepls you find out the variants of assemblied genome set and reference genome.
Users can also use snpEff and circos to visualize the results.
"""

import os, shutil, sys, distutils.dir_util
from optparse import OptionParser
from argparse import ArgumentParser
from subprocess import call

### Get all arguments data
parser = ArgumentParser()
# Choose idba or SPAdes
parser.add_argument("-c",action = 'store', dest='choose',default='idba' or 'spades', help='choose SPAdes assembler')
# Import input files: unpaired (up), paired-end (pe)
parser.add_argument('--up',action='store', dest='file_up', nargs='+', help='unpaired reads fastq input file(s) (2 files max)')
parser.add_argument('--pe',action='store', dest='file_pe', nargs='+', help='paired reads fastq input file(s) (2 files max)')
# Import reference files
parser.add_argument('-r', action='store', dest='ref_file', help='referrence file')
# SnpEff option
parser.add_argument("-s",action = 'store_true', dest='snpeff', help='make variant summary by snpEff')
# Circos option
parser.add_argument("-v",action = 'store_true', dest='circos', help='visualise synteny blocks by Circos program')
# Set output directory
parser.add_argument("-o",action='store', dest = "out_dir", help='output directory')
args = parser.parse_args()

# Define input file(s): unpaired or paired
FILE_NAME=[]
if args.file_up == None:
    FILE_NAME = args.file_pe
else: FILE_NAME = args.file_up


# Because idba and spades have different output contig file name, so it is necessary to define a name for C-Sibelia input
CONTIG_FILE=''

# Define snpEff function
def snpEff(ref_file):
    # Find name of the reference genome to find database in snpEff.config
    # For example, find "NC_000913" in the first line of reference file
    # >gi|49175990|ref|NC_000913.2|_Escherichia_coli_str._K-12_substr._MG1655,_complete_genome
    FIRST_LINE=open(ref_file).readline()
    TEMP=[]
    for i in range(1, len(FIRST_LINE)):
        if FIRST_LINE[i]=='|': # Find positions of letter '|'
            TEMP.append(i)
    NAME=FIRST_LINE[TEMP[2]+1:TEMP[3]-2] # Genome's name code is between the third '|' and forth '|'
    # Find name code of genome in database:
    DATABASE=open('snpEff.config').readlines()
    LIB=''
    for i in range(1, len(DATABASE)):
        if DATABASE[i].find(NAME)!=-1:
            LIB=DATABASE[i][0:DATABASE[i].find('.')] # The name of used database is the part before '.genome' : NC_000913.genome : Escherichia_coli
	    break
    if LIB!='':
	print('Downloading database for snpEff')
        call(['java -jar snpEff.jar '+LIB+' variant.vcf > variant.eff.vcf'], shell=True)
        print('snpEff was done')
    else: print('Unsupported database, snpEff needs database to execute!')
    return

# Main function
def main():
    # idba block
    if args.choose == 'idba':
        if len(FILE_NAME)==1: # One input file
            # If the file is unpaired:
            if args.file_up != None:
                call(["fq2fa "+FILE_NAME[0]+" input.fa"], shell=True)
            # If the input file is paired
            if args.file_pe != None: call(["fq2fa --paired --filter "+FILE_NAME[0]+" input.fa"], shell=True)
        if len(FILE_NAME)==2:  # Two input files
            # If the files are unpaired:
            if args.file_up != None:
                call(["fq2fa --merge "+FILE_NAME[0]+" "+FILE_NAME[1]+" input.fa"], shell=True)
            # If the input files are paired
            if args.file_pe != None: call(["fq2fa --merge --filter "+FILE_NAME[0]
                                           +" "+FILE_NAME[1]+" input.fa"], shell=True)      
        # Run idba assembly
        call(["idba --read input.fa -o "+args.out_dir], shell=True)
        CONTIG_FILE='contig.fa'

    #SPADes block
    if args.choose == 'spades':
        # Run SPAdes to assembly one input file:
        if len(FILE_NAME)==1 and args.file_up != None:
                call(["spades.py -s "+FILE_NAME[0]+" -o "+args.out_dir], shell=True)
        # Run SPAdes to assembly two input files
        if len(FILE_NAME)==2: # Two input files
            # Two single-read files
            if args.file_up != None:
                call(["spades.py --s1 "+FILE_NAME[0]+" --s2 "+FILE_NAME[1]+" -o "+args.out_dir], shell=True)
            # If the input fileS are paired
            if args.file_pe != None: call(["spades.py --pe1-1 "+FILE_NAME[0]
             +" --pe1-2 "+FILE_NAME[1]+" -o "+args.out_dir], shell=True)
        CONTIG_FILE='contigs.fasta'

    ### Sibelia block:
    # Copy referrence file to output directory
    shutil.copy(args.ref_file, args.out_dir)
    # Copy the content of snpEff foder to reference folder
    distutils.dir_util.copy_tree('snpEff', args.out_dir)
    # Go to output directory
    os.chdir(args.out_dir)
    # Run C-Sibelia to find out variants
    call(["C-Sibelia.py "+args.ref_file+" "+CONTIG_FILE], shell=True)
    # Run Sibelia to find synteny blocks
    call(["Sibelia -s loose "+CONTIG_FILE], shell=True)
    # snpEff option
    if args.snpeff == True: # Run snpEff
        snpEff(args.ref_file)
    # Circos option
    if args.circos == True:
        os.chdir('circos')
        call(['circos -conf circos.conf -debug_group _all'], shell=True)


if __name__=='__main__':
    sys.exit(main())

        
        
