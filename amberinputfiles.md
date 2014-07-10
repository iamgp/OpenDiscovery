### tleaP

You can run this using `tleap -s -f tleap.in`

```
source leaprc.ff99SB
source leaprc.gaff

LIG = loadmol2 lig.ante.mol2
REC = loadpdb 1OXWA.pdb
COM = combine {LIG REC}

loadamberparams lig.frcmod

charge COM

addions COM Na+ 13

solvateoct COM TIP3PBOX 10

saveamberparm COM lig.com.solv.prmtop lig.com.solv.inpcrd
savePdb COM lig.com.solv.pdb

quit
```

### MD

#### Minimisation
```
Minimisation of complex
 &cntrl
  imin=1, maxcyc=10000, ncyc=5000,
  cut=12, ntb=1, igb=0, ntr=0
 /
END
END
```
#### First MD Run (NVT, 20ps)
```
MD heating 0 to 300K over 20 ps at CONSTANT VOLUME,  no shake
 &cntrl
  imin   = 0,
  irest  = 0,
  ntx    = 1,
  ntb    = 1,
  cut    = 12,
  ntr    = 0,
  ntc    = 1,
  ntf    = 1,
  igb    = 0
  tempi  = 0.0,
  temp0  = 300.0,
  ntt    = 3,
  gamma_ln = 1.0,
  nstlim = 20000, dt = 0.001
  ntpr = 10000, ntwx = 10000, ntwr = 10000
/
END
END
```
#### Second MD Run (NPT, 50ns)
```
MD run const pressure NO SHAKE
 &cntrl
  imin   = 0,
  irest  = 1,
  ntx    = 7,
  ntb    = 2,
  cut    = 12,
  ntr    = 0,
  ntc    = 1,
  ntf    = 1,
  igb    = 0
  ntp    = 1
  tempi  = 300.0,
  temp0  = 300.0,
  ntt    = 3,
  gamma_ln = 1.0,
  nstlim = 5000000, dt = 0.001
  ntpr = 10000, ntwx = 10000, ntwr = 10000
/
END
END
```
#### Alternative Second MD Run (NVT, 50ns)
```
MD run const VOLUME WITH SHAKE at 300K
 &cntrl
  imin   = 0,
  irest  = 1,
  ntx    = 7,
  ntb    = 1,
  cut    = 12,
  ntr    = 0,
  ntc    = 2,
  ntf    = 2,
  igb    = 0
  ntp    = 0
  tempi  = 300.0,
  temp0  = 300.0,
  ntt    = 1,
  gamma_ln = 0,
  nstlim = 25000000, dt = 0.002
  ntpr = 12500, ntwx = 12500, ntwr = 12500
/
END
END
```
### Ptraj

#### Combine MD runs
```
trajin md1.mdcrd
trajin md2.mdcrd
trajin md3.mdcrd
trajin md4.mdcrd
trajout md.combined.mdcrd
```
#### Shorten MD run
```
trajin md.combined.mdcrd 1 10002 10
trajout md.shortened.mdcrd
```
#### RMSD
```
trajin md.shortened.mdcrd
average average.pdb pdb
rms first out rms_first.dat  :1-349@N,C,CA
```
#### Distance
```
trajin md.shortened.mdcrd
distance end_to_end :350@HC1 :51@HG out oh_h2.list
```