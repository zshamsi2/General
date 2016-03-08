import numpy as np
import msmbuilder.cluster
import glob
from msmbuilder.utils import io
import pickle

name_sys =  'ANC_S1'
dataset = []
inf = {}
for i in sorted(glob.glob('phi_psi_chi1/*.npy')):
  # making msm from raw rmsd features
  # preparing data format
  a = np.load(i)
  #b = [[j] for j in a]
  b = a
  c = np.array(b)
  #d = c[0:-1:40]
  d = c
  dataset.append(d)
  inf[i] = len(dataset)
  print(len(dataset))
  print i

with open('maping_'+name_sys+'.txt', 'wb') as handle:
  pickle.dump(inf, handle)
  
################################################################ Define tICs #####################################################

from msmbuilder.decomposition import tICA
tica = tICA(n_components=10, lag_time=1)
tica.fit(dataset)
tica_traj = tica.transform(dataset)
np.save('tica_traj', tica_traj)
################################################################ Cluster tICs #####################################################  

states = msmbuilder.cluster.KMeans(n_clusters=1000)
states.fit(tica_traj)

io.dump(states,'clustering.pkl')







################################################

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
