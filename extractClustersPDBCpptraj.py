from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
	
msm='MSM10-500.pkl'
cl='clustering.pkl'
n_samples = 1 # numebr of samples for each cluster
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
		filename = 'cluster'+str(i)+'_'+str(count)
		trjFrame=structure[1]
		trj = T[structure[0]]
        	#f = md.load(T[structure[0]], top=top, frame=structure[1])
        	#f.save_pdb(filename)
		f = open('cpp_'+filename+'.in', 'w')
		f.write('parm ' + top + '\n')
		f.write('trajin ' + trj  + '\n')
  		f.write('parmbox alpha 90 beta 90 gamma 90\n')
  		f.write('trajout ' + filename + '.rst restart onlyframes ' + str(trjFrame) +'\n')
  		f.write('parmwrite out ' + filename +'.prmtop\n')
  		f.write('run \n')
  		f.write('quit')
        	f.close()
        	count = count+1
        	
        	print(str(count)+' saved!')
