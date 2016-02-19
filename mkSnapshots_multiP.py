from msmbuilder.utils import io 
from multiprocessing import Pool
import pickle
import glob 
import mdtraj as md

# MSM file in pickle format
msm='MSM10-500.pkl'
# Cluster file in pickle format
cl='clustering.pkl'
# Number of snapshots
n_samples = 10000
# Address of actual MD trajectories
Trjs = '../*.mdcrd'
# Comon topology name and address
top = 'pNRTapo-strip.pdb'
# Number of processors
np = 10


# Functions required for parallelization
def multi_run_wrapper(args):
	return f(*args)
def f(msm,clL,frame,count):
	print count
	structure = msm.draw_samples(clL, 1)[frame]
	print structure
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

arg = [(msm,clL,synthTrj[count],count) for count in range(len(synthTrj))]
p = Pool(np)
S = p.map(multi_run_wrapper, arg)
