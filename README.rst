OpenDiscovery
===================

Version: 2.2

Contacts: gareth.price@warwick.ac.uk; a.marsh@warwick.ac.uk

Introduction
------------

Open Discovery is a suite of programs that use Open Source or freely
available tools to dock a library of chemical compounds against a
receptor protein. In a paper in the Journal of
Chemical Education, we outline the usefulness of having an
uncomplicated, free-to-use protocol to accomplish a task that has been
the subject of academic and commercial interest for decades [1]. We also
highlight the gaps in open source tools around preparing protein -
ligand complexes for molecular simulation, an area we expect to develop
in the future.

Dependencies
------------

-  Python (you probably have this, install from
   http://www.python.org/getit/ - version developed with: 2.7)
-  Open Babel (install from http://openbabel.org/ - version developed
   with: 2.3.1)
-  AutoDock Vina binary (provided in lib folder, but downloaded from
   http://vina.scripps.edu - version developed with: 1.1.2)
-  OpenDiscovery is most easily obtained using `pip`, the python package manager. Pip installs all the python dependencies that are required.

Pip installation
------------
You can find all the methods of installing pip by looking at the documentation for it [here](http://opendiscovery.co.uk/pip.readthedocs.org/en/latest/installing.html).

However, the simplest way is to download [get_pip.py](https://raw.github.com/pypa/pip/master/contrib/get-pip.py), and using terminal, run it through the python interpreter. After, check it is installed properly by retrieving its version:

```bash
mkdir ~/pip && cd ~/pip
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get_pip.py
rm -r ~/pip
pip -V
```
Please note: by typing 'sudo' you will be required to type your password. This allows the command root access to install files where they need to go.

Using pip to install OpenDiscovery
---------------------------------
Assuming pip has installed correctly, OpenDiscovery can be installed by the following command:

```bash
# Installing OpenDiscovery globally
sudo pip install OpenDiscovery
```

If you do not have root (such as on a cluster of workstations), pip can be used to install modules into a user directory:

```bash
# Installing OpenDiscovery locally in user folder
pip install --user OpenDiscovery
```

There are other options [here](https://www.pik-potsdam.de/members/linstead/guides/python-on-the-cluster/installing-your-own-python-modules-on-the-cluster).

Terminology
-----------

* **Receptor**: The protein to which the chemical compound is docked to. Note: use AutoDockTools to prepare the receptor as described by its creators. The video tutorial includes a good introduction to docking.
* **Exhaustiveness**: Somewhat ambigious, but can be thought of as being proportional to the amount of effort the docking uses to search all orientations, positions and rotations of the ligand.
* **Ligand Folder**: The folder in which the conf files, ligands and receptor proteins are located.
* **PDBQT**: A PDBQT file is a normal PDB file (i.e. atoms, chains, xyz coordinates etc.) with partial charges (Q) and atom types (T).
* **Conf File**: Docking programs require a box in which they can look at different orientations, positions and rotations of the ligand. This should be created using AutoDockTools.

Walkthrough
-----------

A simple walkthrough for this new version will be created shortly.
The original version can be found [here](http://opendiscovery.co.uk/start.html)

References
----------
[1]: [Price, G. W., Gould, P. S. & Marsh, A. Use of Freely Available and Open Source Tools for In Silico Screening in Chemical Biology. J. Chem. Educ. (2014). doi:10.1021/ed400302u](http://pubs.acs.org/doi/full/10.1021/ed400302u)

Running OpenDiscovery
===================

Setting up the ligand folder
------
The receptor protein must be located within a folder named receptor. A PDB version must be present, and a PDBQT version, generated using [AutoDockTools](http://autodock.scripps.edu/resources/adt), must also be present with the same name as the PDB version. Finally, a conf file must be present, again with the same name, ending with a .txt extension.

Note: the ligand folder can be placed anywhere on your computer. Just remember the path to it.

Next, we need to set up the ligand folder. Here, we can place ligands in any format that open babel allows. For example, we could have X.pdb, Y.mol, Z.mol2 and so on.

<!--![](http://opendiscovery.co.uk/assets/images/ligand-folder.png)
-->
To be continued...

# Contact
IF you wish to get in contact, please email [Gareth Price](gareth.price@warwick.ac.uk).