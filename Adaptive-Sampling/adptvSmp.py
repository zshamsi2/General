import numpy as np
import mdtraj as md
import glob
from msmbuilder.utils import io
import msmbuilder.cluster
from msmbuilder.msm import MarkovStateModel
import pickle
import adaptiveSamplingMSM as ad


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
        
        def findTop(self, trjN):
	        roundN = trjN.split('/')[1][0:3]
	        a = trjN.split('/')[-1]
	        topN = a.split('_md')[0]
	        rawtop = 'rawTrj/'+roundN+'-rwTop/'+topN+'.prmtop'
	        return rawtop
	
        def findRawtrj(self, trjN):
        	roundN = trjN.split('/')[1][0:3]
        	sysName = trjN.split('/')[-1]
        	rawTrj = 'rawTrj/'+roundN+'-rwTrj/'+sysName
        	return rawTrj
        
        def cppGen(self, cl, n_samples):
                cluster = pickle.load(open(cl,'rb'))
                clL = cluster.labels_

                msm = MarkovStateModel(lag_time=10,n_timescales=10)
                msm.fit_transform(clL)
                trjs = clL
                N = n_samples
                inits = ad.findStarting([trjs], N, method=method)
                T = []
                for trj in sorted(glob.glob(Trjs)):
	                T.append(trj)
                count = 0
                for init in inits:
                	structure = msm.draw_samples(clL, 1)[init]
                	print structure
                	top = findTop(T[structure[0][0]])
                	rawTrj = findRawtrj(T[structure[0][0]])
                	print(top)
	                frame = structure[0][1]
	                newTop = name_sys+str(count)+'_'+name_round+'.prmtop'
	                newrst = name_sys+str(count)+'_'+name_round+'-00.rst'
	                f = open('cppASample_'+str(count)+'.in', 'w')
                        f.write('parm ' + top + '\n')
                        f.write('trajin ' + rawTrj  + '\n')
                        f.write('parmbox alpha 90 beta 90 gamma 90\n')
                        f.write('trajout ' + newrst + ' restart onlyframes ' + str(frame) +'\n')
                        f.write('parmwrite out ' + newTop +'\n')
                        f.write('run \n')
                        f.write('quit')
                        f.close()
	                count = count+1	
	                print(count)
                return
                 
        
