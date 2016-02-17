from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
	
msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 5000
Trjs = '../*.mdcrd'
top = 'pNRTapo-strip.pdb'

cluster = pickle.load(open(cl,'rb'))
clL = cluster.labels_
msm = io.load(msm)

trj = msm.sample_discrete(state = None, n_steps = n_samples)
#selections = msm.draw_samples(clL, n_samples)

T = []
for trj in sorted(glob.glob(Trjs)):
	T.append(trj)

count = 0
for frame in trj:
	selections = msm.draw_samples(clL, 1)[frame]
	
	f = md.load(T[structure[0]], top=top, frame=structure[1])
	f.save_pdb(str(count)+'.pdb')
	count = count+1	

	print count 
