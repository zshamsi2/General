
import adaptiveSamplingMSM as ad
from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
	
msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 10
Trjs = '/projects/cse/shared/diwakar/gpcr/DESRES/DESRES-Trajectory_pnas2011b-A-​*-all/pnas2011b-A-*​-all/pnas2011b-A-​*-all*​.dcd'
top = 'top.top'

cluster = pickle.load(open(cl,'rb'))
clL = cluster.labels_
msm = io.load(msm)

selections = msm.draw_samples(clL, n_samples)

T = []
for trj in sorted(glob.glob(Trjs)):
	T.append(trj)


for i in range(len(selections)):
    filename = 'cluster'+ str(i) + '.pdb'
        count = 0
        selection = selections[i]
        for structure in selection:

          f = md.load(T[structure[0]], top=top, frame=structure[1])
          f.save_pdb(filename+'_'+str(count))
          count = count+1
          
