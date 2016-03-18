from msmbuilder.dataset import dataset
import numpy as np
from msmbuilder.cluster import KMeans
import pickle
import adptvSampling
import glob
import msmbuilder.cluster
from msmbuilder.utils import io

### Step 3: Clustering
myn_clusters = 200
n_samples = 50
dataset = []

inf = open('readme','w')
for i in sorted(glob.glob('2OIQ-ftrz/*.npy')):
  a = np.load(i)
  dataset.append(a)
  print i
states = msmbuilder.cluster.KMeans(n_clusters=myn_clusters)
states.fit(dataset)
io.dump(states,'clustering.pkl')


### Step 4: finding starting points 
# the address should be the address of trajectories corresponding to dataset
# findStarting(trjs, N, method='random')

import adaptivsamplingMSM as ad
cluster=pickle.load(open('clustering.pkl','rb'))
trjs = cluster.labels_
N = n_samples
T = []
for trj in sorted(glob.glob('rawTrj/MD1-rwTrj/*.mdcrd')):
	T.append(trj)
inits = ad.findStarting(trjs, N, method='leastcount')
msm=MarkovStateModel(lag_time=1, n_timescales=10)
msm.fit_transform(cl.labels_)
OPF = []
for i in range(n_samples):
	init = msm.draw_samples(inits[i], 1)
	traj = T[init[0][0]]
	fram = init[0][1]
	OPF.append({'traj':T[trj], 'frame':frm})
json.dump(OPF, open("ClsInf.txt",'w'))

### Step 5: making the CPPtraj inputs

import json
topFile='mytopfile.top'
inf = json.load(open("ClsInf.txt"))
n_samples = len(inf)
for i in range(n_samples):
	f = open('ccpASample_' + str(i), 'w')
	f.write('parm ' + topFile + '\n')
	trj = inf[i]['traj']
	f.write('trajin ' + trj  + '\n')
	f.write('parmbox alpha 90 beta 90 gamma 90\n')
	f.write('trajout Sample_' + str(i) + '.rst restart onlyframes ' + str(inf[i]['frame']) +'\n')
	f.write('parmwrite out Sample_' + str(i) +'.prmtop \n')
	f.write('run \n')
	f.write('quit \n')
	f.close()
	
	
# Write the output file, which have the information about population of each cluster, 
# trajectory name and frame number of corresponding frame 	
# adptvSampling.writeOPF_lessPop(l, T, myn_clusters, n_samples)
# Based on information in output file, build the cpptraj input file, as you give it the topology name, it should be 
# common for all trajectories
