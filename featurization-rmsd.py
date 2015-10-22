import numpy as np
import mdtraj as md

ref_2hyy=md.load('2HYY.pdb')
t = md.load('stripedTrj/MD1-strTrj/2HYY_2_md1-01.mdcrd', top='2HYY.prmtop')
rmsds = md.rmsd(t, ref_2hyy, frame=0)
np.save('tst.npy', rmsds)
