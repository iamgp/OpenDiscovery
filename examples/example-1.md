<p align="center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/logo.png" width="300px" /></p>

[www.opendiscovery.org.uk](http://www.opendiscovery.org.uk)

Version: 1.0.1

Contacts: gareth.price@warwick.ac.uk; a.marsh@warwick.ac.uk

## Example 1: TIR1 Ubiquitin Ligase + IAC
You can follow along with this example by downloading the initial PDB from [here](http://www.rcsb.org/pdb/explore/explore.do?structureId=2p1q). Before starting, watch the video tutorial provided by the authors of AutoDock Vina, [here](http://vina.scripps.edu/tutorial.html).

### Preparing the files
We first need to split the crystal structure of the complex into separate receptor and ligand files.
The first section of a PDB is normally the HEADER, with notes about the structure and how it was acquired. We can easily grab just the ATOM lines by using `grep` in terminal:

`grep "^ATOM\|^TER" 2P1Q.pdb > ubq_lig.pdb`

Here the `^` symbol is saying "find all the lines which start with ATOM or (\\|) TER", and then the filename, then we "pipe" all the output into a new file, `receptor.pdb`.

We can now do the same thing, but with the ligands, which start with HETATM:

`grep "^HETATM" 2P1Q.pdb > IAC.pdb`

But if you look int the `IAC.pdb` file, it also includes IHP, an allosteric ligand that binds to another active site (which we are not interested in). To select only IAC, we can do this:

`grep "^HETATM" 2P1Q.pdb | grep "IAC" > IAC.pdb`

We first select all the lines starting with HETATM, then select those which contain IAC, and the make the IAC.pdb file.

Now, put `ubq_lig.pdb` into a **receptor** folder and `IAC.pdb` into a **pdb** folder. Next, we need to prepare the receptor protein (`ubq_lig.pdb`).

Open up AutoDockTools, and follow the steps in the image below. Make sure to remember the coordinates and dimensions. Make sure Spacing (Angstrom) is set to 1.000.

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/3-prepare_receptor_aux.jpg"></p>

Open a new file and enter the box coordinates and dimensions such as:

```
center_x = 6.967
center_y = -133.155
center_z = -29.129

size_x = 10
size_y = 10
size_z = 10
```

Save it as `ubq_lig.conf`.

You should have a folder that looks like:

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/tree-1-2.png"></p>


### Task 1: Compare Docked IAC to Crystal Structure
In this task we run ODScreen to dock just the IAC molecule into the active site of the Ubiquitin Ligase protein. Using both the resulting docked *and* crystal ligand-protein complex we can calculate an RMSD (Root Mean Squared Deviation) value, giving an indication of how well Vina performs.

First, let's check that everything is installed properly. In terminal, `cd` to the Protocol Folder (i.e. the folder with `odscreen.py` etc.) and run `python odcheck.py`. Check that there are no failures, and follow the installation guides if there are. You can ignore the warnings. Now, we can run the screening protocol. Navigate to the folder where ubq_lig.conf is located (from before). Now we can run `python odscreen.py`. Make sure you use the correct path to the `odscreen.py` file.

`python /protocolfolder/odscreen.py -d . -r ubq_lig -i pdb -c ubq_lig.conf`

This is the result:

```
 # ----------------------------------------- #
 #              OPEN DISCOVERY               #
 #             Screening Module              #
 # ----------------------------------------- #
 # Version:  1.0.1                             #
 # URL:      www.opendiscovery.org.uk        #
 # Contacts: gareth.price@warwick.ac.uk      #
 #           a.marsh@warwick.ac.uk           #
 # ----------------------------------------- #
 #  LigDir: /Users/garethprice/Desktop/rmsd  #
 #           Receptor Name: ubq_lig          #
 #              Input Type: pdb              #
 #             Conf: ubq_lig.conf            #
 #             Exhaustivness: 50             #
 # ----------------------------------------- #
 #  Time Started: Thu, 12 Sep 2013 23:25:55  #
 # ----------------------------------------- #


                      SMI
              Writing smi/IAC.smi


                      MOL
              Writing mol/IAC.mol


                      MOL2
             Writing mol2/IAC.mol2


                     IMAGES


                  MINIMISATION
                 Minimising IAC


                PDBQT PREPARATION
               Writing IAC.pdbqt


                    SCREENING
                 Processing IAC


                   EXTRACTING
            Processing results/IAC/


                   PDB -> MOL2
         Writing results-mol2/IAC.mol2


                   SUMMARISING
                Summarising IAC


                MAKING COMPLEXES
                  Writing IAC


 # ----------------------------------------- #
 #                  FINSHED                  #
 #         Time Taken: 54.57 seconds         #
 # ----------------------------------------- #
```

The resulting files are:

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/tree-2.png"></p>

Once the protocol is complete, start Chimera (USCF), then open both `pdb/IAC.pdb` and `results/IAC/IAC_mode_1.pdb`:

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/chimera-1.png"></p>

Visual inspection tells us that the docking has worked well. We can get a numerical value for RMSD by opening the command line (by Tools->Command Line->Raise). First, select the "Select" toolbar item, then "Chemistry", then "element" then "H". Now go "Actions"->"Atoms/Bonds"->"Delete".

In the command line bar, type `rmsd #0 #1`:

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/chimera-2.png"></p>

An RMSD of 2.224 Angstroms is perfectly reasonable.

### Task 2: Generate a library of similar ligands and dock them to the protein
There are plenty of methods of  generating libraries of similar compounds, and you may already have a library of ligands that you are interested in. An easy way is to use [Chemicalize](http://chemicalize.org). Search for `indolylacetic acid`, then click "View all similar structures".

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/chemicalize-1.png"></p>

Choose Download on the top right and choose Smiles as the method of download:

<p style="text-align: center"><img src="http://www2.warwick.ac.uk/fac/sci/moac/people/students/2012/gareth_price/opendiscovery/walkthrough/chemicalize-2.png"></p>

Move this into the folder where your `ubq_lig.conf` file is located. Rename the file to `smiles.smi`, then we can run `odscreen` to automatically go through the whole list and perform the procedure we did in Task 1, to every single ligand. The file downloaded will contain thousands of chemical ligands– it might be wise to split them into chunks if computer time is limited. Odscreen has a limit of 999 ligands at anyone time, too.


 You can run `odscreen` on the smiles.smi file with:

`python /protocolfolder/odscreen -d . -r ubq_lig -i smilestext -c ubq_lig.conf`

This produces:

```
 # ----------------------------------------- #
 #              OPEN DISCOVERY               #
 #             Screening Module              #
 # ----------------------------------------- #
 # Version:  1.0.1                             #
 # URL:      www.opendiscovery.org.uk        #
 # Contacts: gareth.price@warwick.ac.uk      #
 #           a.marsh@warwick.ac.uk           #
 # ----------------------------------------- #
 #  LigDir: /Users/garethprice/Desktop/rmsd  #
 #           Receptor Name: ubq_lig          #
 #           Input Type: smilestext          #
 #             Conf: ubq_lig.conf            #
 #             Exhaustivness: 20             #
 # ----------------------------------------- #
 #  Time Started: Thu, 12 Sep 2013 23:46:58  #
 # ----------------------------------------- #
  996 molecules converted
  996 files output. The first is smi/compound1.smi
  0
             Splitting smiles file


                      MOL
           Writing mol/compound1.mol
           Writing mol/compound10.mol
          Writing mol/compound100.mol

 . . . . . .
```

Once docked, you can perform analysis (visual or otherwise) on the docked complexes. A list (`summary-sorted.csv`) is produced which ranks the ligands based on their calculated free binding energy. This can be opened in Excel or a normal text editor.








