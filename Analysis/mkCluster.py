# msmb AtomPairsFeaturizer --out mainnode-pair_indices_stride20-2 --pair_indices AtomIndices.txt --top A2.prmtop --trjs 'MD*/*.mdcrd' --stride 20
import numpy as np
from msmbuilder.utils import io
import msmbuilder.cluster
import glob
import pickle

name_sys =  '2OIQ'
dataset = []
inf = {}

for i in sorted(glob.glob('featurizes_RMSD+drugDist/*.npy')):
        dataset.append(np.load(i))
        inf[i] = len(dataset)
        print(i)
        print(len(dataset))

with open('maping_'+name_sys+'.txt', 'wb') as handle:
  pickle.dump(inf, handle)
 
"""
with open('file.txt', 'rb') as handle:
  b = pickle.loads(handle.read())
"""

states = msmbuilder.cluster.KMeans(n_clusters=500)
states.fit(dataset)

io.dump(states,'clustering_'+name_sys+'_db.pkl')
