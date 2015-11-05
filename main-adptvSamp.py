from msmbuilder.dataset import dataset
import numpy as np
from msmbuilder.cluster import KMeans
import pickle
import adptvSampling
import glob
import msmbuilder.cluster
from msmbuilder.utils import io

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

cluster=pickle.load(open('clustering.pkl','rb'))
l = cluster.labels_

T = []
# the address should be the address of trajectories corresponding to dataset
for trj in glob.glob('rawTrj/MD1-rwTrj/*.mdcrd'):
	T.append(trj)
T.sort()
# Write the output file, which have the information about population of each cluster, 
# trajectory name and frame number of corresponding frame 	
adptvSampling.writeOPF_lessPop(l, T, myn_clusters, n_samples)

# Based on information in output file, build the cpptraj input file, as you give it the topology name, it should be 
# common for all trajectories
topFile='mytopfile.top'
adptvSampling.CpptrajInGen()
