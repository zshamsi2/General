from msmbuilder.utils import io 
from multiprocessing import Pool
import pickle
import glob 
import mdtraj as md

msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 10000
Trjs = '../*.mdcrd'
top = 'pNRTapo-strip.pdb'

def multi_run_wrapper(args):
	return f(*args)
def f(msm,clL,frame,count):
	structure = msm.draw_samples(clL, 1)[frame]
	f = md.load(T[structure[0][0]], top=top, frame=structure[0][1])
	f.save_pdb(str(count)+'.pdb')
	print count 
	
cluster = pickle.load(open(cl,'rb'))
clL = cluster.labels_
msm = io.load(msm)

synthTrj = msm.sample_discrete(state = None, n_steps = n_samples)

T = []
for trj in sorted(glob.glob(Trjs)):
	T.append(trj)

count = 0
arg = [(msm,clL,synthTrj[count],count) for count in range(len(trj))]
p = Pool(10)
S = p.map(multi_run_wrapper, arg)









	
msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 10
Trjs = '../*.mdcrd'
top = 'pNRTapo-strip.pdb'

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
        	f = md.load(T[structure[0]], top=top, frame=structure[1])
        	f.save_pdb(filename)
        	count = count+1
        	print(str(count)+' pdb saved!')
