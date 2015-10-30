import numpy as np
import mdtraj as md
import glob

# reference structure for calculating RMSD
ref=md.load('2HYY.pdb')
count=0
for file in glob.glob('stripedTrj/MD1-strTrj/*.dcd'):
  a = file.split('/')[-1]
  name = a.split('.')[0]
  t = md.load(file, top='2HYY.prmtop')
  rmsds = md.rmsd(t, ref, frame=0)
  rmsds1 = [[j] for j in rmsds]
  rmsds2 = np.array(rmsds1)
  np.save(name+'.npy', rmsds2)
