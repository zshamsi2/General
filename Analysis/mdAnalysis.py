import numpy as np
import mdtraj as md
from matplotlib import pyplot as plt
import glob
from msmbuilder.utils import io 


class mdAnalysis:

        def __init__(self):

                return
        
        def couplingMeasuring(self):
        """
        """
        
        
                return
        
        def extractClustersPDB(self, msm='MSM.pkl', cl='clustering.pkl', n_samples = 5, Trjs = 'ww_1*.xtc', top = 'ww_ext.pdb'):
        """
        """
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
                		print(T[structure[0]])
                		print(structure[1])
                        	f = md.load(T[structure[0]], top=top, frame=structure[1])
                        	f.save_pdb(filename)
                        	count = count+1
                        	print(str(count)+' pdb saved!')
                return
        
        def extractClustersPDB_Cpptraj(self):
        """
        """
        
        
                return
        
        def extractClustersPDB_multiProcessor(self):
        """
        """
        
    
                return
        
        def minIonDist(self, topN = 'A2AR-strip.prmtop',trjN = 'A2AR-alltrjs01.mdcrd' , pocketInexAtom = 807):
        """
        Find the distance of the closet ion from the binding pocket in the transporter
        """
                ionAtoms = [4738, 4739, 4740, 4741, 4742, 4743, 4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752,
                    4753, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4766, 4767,
                    4768, 4769, 4770, 4771, 4772, 4773]

                t = md.load(trjN ,top=topN)
                nFrames = t.n_frames
                dist = np.empty(nFrames)

                for frame in range(nFrames):
                topIonAtoms = [ion for ion in ionAtoms if t.xyz[frame][ion][2]<3]
                allDist = md.compute_distances(t,[[pocketInexAtom, ion] for ion in topIonAtoms])
                frameDist = allDist[frame]
                dist[frame] = frameDist.min()
                plt.show()       
                return self
        
        def mkCluster(self):
        """
        """
        
        
        return
        
        def mkSnapshots(self, msm='MSM10-500.pkl', cl='clustering.pkl',n_samples = 5000,Trjs = '../*.mdcrd',top = 'pNRTapo-strip.pdb'):
        """
        mkSnapshots
        """
                cluster = pickle.load(open(cl,'rb'))
                clL = cluster.labels_
                msm = io.load(msm)

                synthTrj = msm.sample_discrete(state = None, n_steps = n_samples)
                T = []
                for trj in sorted(glob.glob(Trjs)):
                	T.append(trj)
        
                count = 0
                for frame in synthTrj:
                	structure = msm.draw_samples(clL, 1)[msm_mapping_[frame]]
                	print(count)
                	print(structure)
                	f = md.load(T[structure[0][0]], top=top, frame=structure[0][1])
                	f.save_pdb(str(count)+'.pdb')
                	count = count+1	
                	print(count)
                return self
        
        def mkSnapshots_Cpptrj(self):
        """
        mkSnapshots_Cpptrj
        """
                return self
        
        def mkSnapshots_multiProcessor(self):
        """
        """

                return self 
        
        def msm_timescale_plt(self):
        """
        """
                return

        
        
