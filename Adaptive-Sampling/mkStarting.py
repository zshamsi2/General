from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
import adaptiveSamplingMSM as ad
from msmbuilder.msm import MarkovStateModel

cl = 'clustering_2OIQ_db.pkl'
n_samples = 50
Trjs = 'MD*-strTrj/*.mdcrd' # unstriped trajs!
top = '2OIQ_db.prmtop'
name_round = 'md3'
name_sys = '2OIQ_db_'
method = 'leastPop'

def findTop(trjN):
	a = trjN.split('/')[-1]
	b = a.split('_md')[0]
	top = b + '.prmtop'
	#top = a.split('.')[0] + '.prmtop'
	return top
	
	
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
	print top
	f = md.load(T[structure[0][0]], top=top, frame=structure[0][1])
	f.save_pdb(name_sys+str(count)+'_'+name_round+'.pdb')
	f.save_pdb(name_sys+str(count)+'_'+name_round+'.prmtop')
	f.save_pdb(name_sys+str(count)+'_'+name_round+'.mdcrd')
	count = count+1	

	print count 
