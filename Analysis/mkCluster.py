import numpy as np
import msmbuilder.cluster
import glob
from msmbuilder.utils import io
import pickle

# Concatinate features before analysis with mapping
# Works GREAT!!! :) 

import glob
import numpy as np
import pickle
name_sys =  'ANC_A2'
mapping = {}
for i in range(0,100):
  flagFirstTime = True
  name = 'A1_Sampler4_'+str(i)+'_Md4-ftrz.npy'

  ftrFrame = 0
  for file in sorted(glob.glob('phi_psi_chi1/A1_Sampler4_'+str(i)+'_Md4*')):
    print file
    if flagFirstTime:
      z = np.load(file)

      insideMap = {}
      for trjFrame in range(len(z)):
        insideMap[ftrFrame]=[file,trjFrame]
        ftrFrame = ftrFrame+1

      flagFirstTime = False
    else:
      trjFtr = np.load(file)
      z = np.append(trjFtr,z, axis=0)

      for trjFrame in range(len(trjFtr)):
        insideMap[ftrFrame]=[file,trjFrame]
        ftrFrame = ftrFrame+1

  print z.shape
  np.save(name,z)
  mapping[name]= insideMap
  
with open('maping_'+name_sys+'.txt', 'wb') as handle:
  pickle.dump(mapping, handle)  
"""
with open('file.txt', 'rb') as handle:
  b = pickle.loads(handle.read())
"""
  
  
# Concatinate features before analysis
import glob
import numpy as np

for i in range(0,100):
  flagFirstTime = True
  name = 'A1_Sampler4_'+str(i)+'_Md4'
  for file in sorted(glob.glob('phi_psi_chi1/A1_Sampler4_'+str(i)+'_Md4*')):
    print file
    if flagFirstTime:
      z = np.load(file)
      flagFirstTime = False
    else:
      z = np.append(np.load(file),z, axis=0)
  print z.shape
  np.save(name,z)
  
  
name_sys =  'ANC_S1'
dataset = []
inf = {}
for i in sorted(glob.glob('phi_psi_chi1/*.npy')):
  # making msm from raw rmsd features
  # preparing data format
  a = np.load(i)
  b = np.array(a)
  dataset.append(b)
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
