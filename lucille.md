# Setting up OpenDiscovery on Ubuntu Servers
#### Email gareth.price@warwick.ac.uk for help.

## Installing python
We need to first install our own python.

```bash
curl -O https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz
```

Extract the contents and change the directory into it:

```bash
tar xvf Python-2.7.8 &&
cd Python-2.7.8
```

Configure to make the make file:

```bash
./configure
```

Make the necessary folders:

```bash
mkdir -p ~/usr/local
```

Then run make:

```bash
make altinstall prefix=$HOME/usr/local exec-prefix=$HOME/usr/local
```

Let's add the folder into our PATH and re-source the file:

```bash
echo "export PATH=\$HOME/usr/local/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
```

Check your new python2.7 is working:

```bash
which python2.7
```

…should return `~/usr/local/bin/python2.7`

## Installing Easy_Install
Let's install our own easy_install:

```bash
curl -O http://python-distribute.org/distribute_setup.py
~/usr/local/bin/python2.7 distribute_setup.py
```
*Note, I am explicitely stating the full path of the python2.7 install, although if we have our PATH set up correctly this is only for completeness' sake.*

Let's check it is installed correctly:

```bash
which easy_install-2.7
```

… should return `~/usr/local/bin/easy_install-2.7`

Easy_install installs stuff into ~/.local/bin, so let's add that to our .bashrc and re-source the file:

```bash
echo "export PATH=\$HOME/.local/bin/:\$PATH" >> ~/.bashrc
source ~/.bashrc
```

## Installing PIP
Now we can use easy_install to install pip:

```bash
~/usr/local/bin/easy_install-2.7 --user pip
```
*Note, I am explicitely stating the full path of the easy_install-2.7 install, although if we have our PATH set up correctly this is only for completeness' sake.*

Like always, let's make sure pip is installed properly:

```bash
which pip2.7
```

…should return `~/.local/bin/pip2.7`

## Installing python modules, including OpenDiscovery
And we can now use pip to install matplotlib, numpy and pandas:

```bash
~/.local/bin/pip2.7 install --user pandas
~/.local/bin/pip2.7 install --user numpy
~/.local/bin/pip2.7 install --user matplotlib
```

Important: if you want to use plot() using matplotlib on lucille, you _must_ run the following commands after you've installed matplotlib:
```bash
echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
```

And then OpenDiscovery:
```bash
~/.local/bin/pip2.7 install --user OpenDiscovery
```

*Note, I am explicitely stating the full path of the pip2.7 install, although if we have our PATH set up correctly this is only for completeness' sake.*


## Installing OpenBabel
Okay, nearly there. Let's compile OpenBabel.

Download the sourcecode, untar it and upload the folder into your user directory (~).

Create a new directory for obabel and cd into it:

```bash
mkdir -p ~/usr/local/obabel
cd ~/usr/local/obabel
```

Using cmake, let's make the makefiles:

```bash
cmake ~/openbabel-2.3.2 -DCMAKE_INSTALL_PREFIX=~/usr/local/obabel
```

Now let's `cd` into the openbabel install directory, and make this thing!:

```bash
cd ~/openbabel-2.3.2/
make && make install
```

It should finish after a while. Once it is done, all we need to do is add the binaries to our PATH:
```bash
echo "export PATH=\$HOME/usr/local/obabel/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
```


## Running OpenDiscovery
Now you have everything installed, all you need to do is submit a slurm script to the queue. Something like the following would do:

```bash
#!/bin/bash
#
#
#SBATCH --gres=gpu:4
#SBATCH --ntasks=4
#SBATCH --exclusive
#SBATCH --mem-per-cpu=3000
#SBATCH --time=0-1:0:0
# This has walltime of 1 hour, after that it gets killed.
# --time=days-hours:minutes:seconds

# if you are using something like odscreen.py (look after):
~/usr/local/bin/python2.7 odscreen.py

# if you want to use the binary
odscreen -d ~/OD_Experiment -e 10
```

An example of odscreen.py is:
```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from OpenDiscovery.screen import run

# ---------------------------------------------------------------------------- #
# Set up options 															   #
# ---------------------------------------------------------------------------- #
# Options available:														   #
# 	- parse      		allows entry via the command line (all 				   #
# 						other options are defunct) 							   #
# 	- directory			tell OpenDiscovery where the files are 				   #
# 						this is required! 									   #
# 	- exhaustiveness	how much effort do you want to use? must be an integer #
# 	- verbose			If True, all commands will show their output (useful   #
# 						for debugging)										   #
# ---------------------------------------------------------------------------- #

options                   = {}
options['directory']      = '~/Desktop/OD_Experiment/'
options['exhaustiveness'] = 1
options['verbose'] = True

# ---------------------------------------------------------------------------- #
# Run the screening								 			   				   #
# ---------------------------------------------------------------------------- #

od = run(options).plot(save=True)
```