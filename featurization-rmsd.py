import numpy as np
import mdtraj as md
import glob

ref_2hyy=md.load('2HYY.pdb')
count=0
for file in glob.glob('stripedTrj/MD1-strTrj/2HYY*')
  t = md.load(file, top='2HYY.prmtop')
  rmsds = md.rmsd(t, ref_2hyy, frame=0)
  np.save(str(count)+'.npy', rmsds)
  count=count+1
