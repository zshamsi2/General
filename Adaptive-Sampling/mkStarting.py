from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
import adaptiveSamplingMSM as ad

msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 100
Trjs = '../*.mdcrd'
top = 'pNRTapo-strip.pdb'

cluster = pickle.load(open(cl,'rb'))
clL = cluster.labels_
msm = io.load(msm)
trjs = clL
N = n_samples
inits = ad.findStarting(trjs, N, method='leastPop')


T = []
for trj in sorted(glob.glob(Trjs)):
	T.append(trj)

count = 0
for init in inits:
	structure = msm.draw_samples(clL, 1)[init]
	print structure
	f = md.load(T[structure[0][0]], top=top, frame=structure[0][1])
	f.save_pdb(str(count)+'.pdb')
	count = count+1	

	print count 
