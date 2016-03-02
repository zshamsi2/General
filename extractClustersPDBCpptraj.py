from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
	
msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 10
Trjs = '../*.mdcrd'
top = 'pNRTapo-strip.pdb'

cluster = pickle.load(open(cl,'rb'))
clL = cluster.labels_
msm = io.load(msm)

selections = msm.draw_samples(clL, n_samples)

T = []
for trj in sorted(glob.glob(Trjs)):
	T.append(trj)

for i in range(len(selections)):
	count = 0
	selection = selections[i]
	for structure in selection:
		filename = 'cluster'+str(i)+'_'+str(count)+'.pdb'
		      frameF=structure[1]
		      str = T[structure[0]]
        	#f = md.load(T[structure[0]], top=top, frame=structure[1])
        	#f.save_pdb(filename)
        	count = count+1
        	print(str(count)+' pdb saved!')
