import numpy as np
import mdtraj as md
import glob
from msmbuilder.utils import io
import msmbuilder.cluster
import pickle

class adptvSmp:
  """
  
  """
        def __init__(self):
                return
  
        def ftz_rmsd(self):
                """
                reference structure for calculating RMSD
                """
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
                return 


        def ftr_rmsd_dist(self):
                """
                
                """
                # favorite residues to compute distance(s)
                cont=[[149, 267]]
                # reference structure for calculating RMSD
                # numbering the outputs
                ref_2hyy=md.load('2HYY.pdb')
                count=0
                for file in glob.glob('stripedTrj/MD1-strTrj/2HYY*'):
                        t = md.load(file, top='2HYY.prmtop')
                        rmsds = md.rmsd(t, ref_2hyy, frame=0)
                        dist=md.compute_contacts(t, contacts=cont)
                        ftr=[[dist[0][i][0],rmsds[i]] for i in range(len(rmsds))]
                        np.save(str(count)+'.npy', ftr)
                        count=count+1
                return
        def mkCluster(self, name_sys='2OIQ'):
                """
                """
                dataset = []
                inf = {}
                
                for i in sorted(glob.glob('featurizes_RMSD+drugDist/*.npy')):
                        dataset.append(np.load(i))
                        inf[i] = len(dataset)
                        print(i)
                        print(len(dataset))

                with open('maping_'+name_sys+'.txt', 'wb') as handle:
                        pickle.dump(inf, handle)
                states = msmbuilder.cluster.KMeans(n_clusters=500)
                states.fit(dataset)
                io.dump(states,'clustering_'+name_sys+'_db.pkl')
                return 
        

        
    
