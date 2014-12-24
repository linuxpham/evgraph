import os, sys, getopt, subprocess

def main(argv):
   inputfile = ''
   outdir = ''
   program=''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","odir="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   #Take input file and output directory
   for opt, arg in opts:
      if opt == '-h':
         print 'If you want to use idba: ver2.py -i <inputfile> -o <outputdir>'
	 print('If you want to use SPAdes to assembler: ver2.py -s <inputfile> -o <outputdir>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
	 program="idba"
      elif opt in ("-s", "--ifile"):
         inputfile = arg
         program="spades"
      elif opt in ("-o", "--odir"):
         outdir = arg
         print(outdir)
   # Run idba if idba is chosen
   if program == "idba":
      subprocess.call(["idba_hybrid -r "+inputfile+ " -o " + outdir], shell=True)
   # Run SPAdes if it is chosen
   if program == "spades":
      subprocess.call(["python spades.py -s "+inputfile+" -o "+ outdir], shell=True)
   os.chdir(outdir) # Go to outdir to run Sibelia
   subprocess.call(["Sibelia -s loose contig.fa"], shell= True)
if __name__ == "__main__":
   main(sys.argv[1:])
