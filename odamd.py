import os, sys
from lib.odcore import *
import argparse

parser = argparse.ArgumentParser(description='Open Discovery aMD Generator');
parser.add_argument('-a', '--natoms', help='Number of Atoms');
parser.add_argument('-r', '--nres', help='Number of protein residues');
parser.add_argument('-d', '--avedi', help='Average dihedral energy');
parser.add_argument('-p', '--avep', help='Average EPTot');
parser.add_argument('-t', '--time', help='Time in ns');
parser.add_argument('-b', '--base', help='The file you wish to append info to (leave for default)', default='default')
args = vars(parser.parse_args());

nATOMS   = int(args['natoms']);
nRES     = int(args['nres']);
aveDi    = int(args['avedi']);
aveEPTot = int(args['avep']);
timeToRun= int(args['time']);
baseFile = args['base'];

# Boosted dihedral energy EthreshD alphaD
EDi = aveDi + (4 * nRES);
alphaDi = 0.2 * (4 * nRES);

print '\n!-----------------------\n!INPUT VALUES\n!-----------------------'
print '!Number of atoms: {0}'.format(nATOMS);
print '!Number of residues: {0}'.format(nRES);
print '!Average dihedral energy: {0} kcal/mol'.format(aveDi);
print '!Average ETot energy: {0} kcal/mol'.format(aveEPTot);

print '\n!-----------------------\n!DIHEDRALS\n!-----------------------'
print '!EthreshD: {0} kcal/mol'.format(EDi);
print '!AlphaD: {0} kcal/mol'.format(alphaDi);


# Total boost parameters
ETot = aveEPTot + (0.16 * nATOMS);
alphaTot = (0.16 * nATOMS);

print '\n!-----------------------\n!TOTAL ENERGY\n!-----------------------'
print '!EthreshP: {0} kcal/mol'.format(ETot);
print '!AlphaP: {0} kcal/mol\n'.format(alphaTot);


defaultBaseFile = '''aMD run const VOLUME WITH SHAKE at 300K {0}ns
 &cntrl
  imin   = 0,
  irest  = 1,
  ntx    = 7,
  ntb    = 1,
  cut    = 8,
  ntr    = 0,
  ntc    = 2,
  ntf    = 2,
  igb    = 0
  ntp    = 0
  tempi  = 300.0,
  temp0  = 300.0,
  ntt    = 1,
  gamma_ln = 0,
  ntpr = 12500, ntwx = 12500, ntwr = 12500,'''.format(timeToRun);

print defaultBaseFile;

steps = (timeToRun * 1000)/0.002;

print '  dt=0.002, nstlim={0}'.format(int(steps))
print '  iamd=3, !aMD OPTIONS\n  EthreshD={0}, alphaD={1},\n  EthreshP={2}, alphaP={3},\n /\nEND\nEND\n'.format(EDi, alphaDi, ETot, alphaTot);

sys.exit()