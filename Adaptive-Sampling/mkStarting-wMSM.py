from msmbuilder.utils import io 
import pickle
import glob 
import mdtraj as md
import adaptiveSamplingMSM as ad
from msmbuilder.msm import MarkovStateModel
import shutil 


cl = 'clustering_2OIQ_db.pkl'
n_samples = 50
Trjs = 'stripedTrj/MD*-strTrj/*.mdcrd' # unstriped trajs!
name_round = 'md3'
name_sys = '2OIQ_db_'
method = 'leastPop'
"""
cl = 'clustering_2OIQ_bi.pkl'
n_samples = 50
Trjs = 'stripedTrj/MD*-strTrj/*.mdcrd' # unstriped trajs!
#top = '2OIQ_db.prmtop'
name_round = 'md3'
name_sys = '2OIQ_bi_'
method = 'leastPop'
"""


def findTop(trjN):
	roundN = trjN.split('/')[1][0:3]
	a = trjN.split('/')[-1]
	topN = a.split('_md')[0]
	rawtop = 'rawTrj/'+roundN+'-rwTop/'+topN+'.prmtop'
	return rawtop
	
def findRawtrj(trjN):
	roundN = trjN.split('/')[1][0:3]
	sysName = trjN.split('/')[-1]
	rawTrj = 'rawTrj/'+roundN+'-rwTrj/'+sysName
	return rawTrj
	
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
	print top
	#f = md.load(rawTrj, top=top, frame=structure[0][1])
	#f.save_pdb(name_sys+str(count)+'_'+name_round+'.pdb')
	#shutil.copy(top, name_sys+str(count)+'_'+name_round+'.prmtop')
	#f.save_mdcrd(name_sys+str(count)+'_'+name_round+'.mdcrd')
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
	print count 
