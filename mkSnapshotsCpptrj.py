from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md

msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 5000
Trjs = '../*.mdcrd'
top = 'pNRTapo-strip.pdb'

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
	print count
	print structure
	trjFrame = structure[0][1]
	trj = T[structure[0][0]]
	#f = md.load(T[structure[0][0]], top=top, frame=structure[0][1])
	#f.save_pdb(str(count)+'.pdb')
	f = open('cpp_'+str(count)+'.in', 'w')
	f.write('parm ' + top + '\n')
	f.write('trajin ' + trj  + '\n')
  f.write('parmbox alpha 90 beta 90 gamma 90\n')
  f.write('trajout ' + str(count) + '.pdb restart onlyframes ' + str(trjFrame) +'\n')
  f.write('parmwrite out ' + newTop +'\n')
  f.write('run \n')
  f.write('quit')
  
	count = count+1	

	print count 
