#Installing ambertools on Ubuntu linux

## Installing dependencies

First we need to install some of the compilers and shells needed.
```bash
# Installing dependencies
sudo apt-get install csh flex patch gfortran g++ make xorg-dev libbz2-dev
```
Now we can install python dependencies.
```bash
# Installing python dependencies
sudo apt-get install python-tk python-dev python-matplotlib python-numpy python-scipy
```

## Extracting AmberTools
We extract the files and set the necessary environmental variables.
```bash
# Extract the archive
tar xvfj AmberTools14.tar.bz2 -C ~/amber14
cd ~/amber14

# AMBERHOME needs to be set in order for patching to work properly
export AMBERHOME=`pwd`

# AMBERHOME needs to be set each time a new terminal window is open
echo "export AMBERHOME=\$HOME/amber14" >> ~/.bashrc
```

Then we configure the makefiles and make the binaries.
```bash
# Configure the makefiles
./configure gnu

# We recommend you say "yes" when asked to apply updates
make install
```

And now we can add the  binaries to our PATH.
```bash
echo "export PATH=\$AMBERHOME/bin:\$PATH" >> ~/.bashrc
```

Done!