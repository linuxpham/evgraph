#!/bin/bash
"""
This script helps user automatically download and install a tool kit for genome variant research.
The tool kit comprises SPAdes, idba assembler; Sibelia; snpEff and circos. Read the readme to know 
more about the tool kit. The required programs are cmake, perl and python to execute following commands.
User can set up a path to install all the programs by:
PREFIX=path ./toolkit.sh
First stage, we install all the necessary libraries that circos needs to run. After that, all the programs
are installed.
"""


set -e
if [ "x$PREFIX" == "x" ]; then
  PREFIX=`pwd`
fi

echo Welcome to evgraph toolkit 

### Install requisite libraries
echo "Stage 1/6: install necesssary libs"
# Install perl modules which circos needs
python perl_mudules_install.py

# Make directory and copy install files 
mkdir $PREFIX
cp ver5.py $PREFIX
cp perl_modules.txt $PREFIX
cp perl_mudules_install.py $PREFIX
cd $PREFIX
mkdir bin
chmod +x ver5.py




# Install some necessary tools for circos
wget circos.ca/distribution/lib/libpng-1.6.14.tar.gz # Install libpng
tar xvfz libpng-1.6.14.tar.gz
cd libpng-1.6.14
./configure --prefix=$PREFIX/local
make
make install
cd ..
# install jpeg
wget circos.ca/distribution/lib/jpegsrc.v9.tar.gz
tar xvfz jpegsrc.v9.tar.gz
cd jpeg-9
s./configure --prefix=$PREFIX/local
make
make install
cd ..
# install freetype
wget circos.ca/distribution/lib/freetype-2.4.0.tar.gz
tar xvfz freetype-2.4.0.tar.gz
cd freetype-2.4.0
./configure --prefix=$PREFIX/local
make
make install
cd ..
# install GD library
wget www.circos.ca/distribution/lib/libgd-2.1.0.tar.gz
tar xvfz libgd-2.1.0.tar.gz
cd libgd-2.1.0
./configure --with-png=$PREFIX/local --with-freetype=$PREFIX/local --with-jpeg=/usr/local --prefix=$PREFIX/local
make
make install
cd ..

wget www.circos.ca/distribution/lib/GD-2.53.tar.gz
tar xvfz GD-2.53.tar.gz
cd GD-2.53
perl Makefile.PL
make
make install
cd ..



### Install SPAdes
echo "Stage 2/6: install SPAdes"
# Download SPAdes package
wget http://spades.bioinf.spbau.ru/release3.5.0/SPAdes-3.5.0.tar.gz

# Extract the package
tar -xzf SPAdes-3.5.0.tar.gz

cd SPAdes-3.5.0
PREFIX=$PREFIX/bin ./spades_compile.sh
export PATH=$PREFIX/SPAdes-3.5.0/bin:$PATH
source ~/.bashrc
cd ..


### Install idba
echo "Stage 3/6: install idba"
# Download idba package
wget https://hku-idba.googlecode.com/files/idba-1.1.1.tar.gz
# Unzip the package
tar -xzf idba-1.1.1.tar.gz
cd idba-1.1.1
./configure --prefix=$PREFIX/local
make
export PATH=$PREFIX/idba-1.1.1/bin:$PATH
source ~/.bashrc
cd ..

### Install Sibelia
echo "Stage 4/6: install Sibelia"
# Download Sibelia installation files
wget https://github.com/bioinf/Sibelia/archive/master.zip
# Extract the zip file
unzip master.zip
cd Sibelia-master/build
cmake ../src -DCMAKE_INSTALL_PREFIX=$PREFIX/local/bin
make
make install
cd ..
cd ..

### Install  circos
echo "Stage 5/6: install circos"
# Download circos
wget https://circos.ca/distribution/circos-0.67-4.tgz
tar xvfz circos-0.67-4.tgz
export PATH=$PREFIX/circos-0.67-4/bin:$PATH
source ~/.bashrc


### Install snpEff
echo "Stage 6/6: install snpEff"
# Download snpEff:
wget http://sourceforge.net/projects/snpeff/files/snpEff_latest_core.zip
# Install 
unzip snpEff_latest_core.zip 

export PATH=$PREFIX:$PATH
source ~/.bashrc


