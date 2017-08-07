#################
# Extract a frame from each cluster using multiple processor

from msmbuilder.utils import io 
from multiprocessing import Pool
import pickle
import glob 
import mdtraj as md

msm='MSM.pkl'
cl='clustering.pkl'
n_samples = 10
Trjs = '*.xtc'
top = 'ww_ext.pdb'

def multi_run_wrapper(args):
	return f(*args)
	
def f(selection,T,top,i):
	import mdtraj as md
	count = 0
	for structure in selection:
		filename = 'cluster'+str(i)+'_'+str(count)+'.pdb'
        	f = md.load(T[structure[0]], top=top, frame=structure[1])
        	f.save_pdb(filename)
        	count = count+1
        	print(filename+' pdb saved!')
	
cluster = pickle.load(open(cl,'rb'))
clL = cluster.labels_
msm = io.load(msm)

selections = msm.draw_samples(clL, n_samples)

T = []
for trj in sorted(glob.glob(Trjs)):
	T.append(trj)

arg = [(selections[i],T,top,i) for i in range(len(selections))]
p = Pool(10)
S = p.map(multi_run_wrapper, arg)
