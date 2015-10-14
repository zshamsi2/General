##########################################################################################
def chFormat(nodesInf):
	count=0
	for q in nodesInf:
		for d in nodesInf[q]:
			if count==0:
				newNodesInf={0:[q, d]}
			newNodesInf[count]=[q, d]
			count=count+1
	return newNodesInf
##########################################################################################
import os
iName='aMD'
r=1 #Sampling round
a=0 #input index
b=1 #output index
Path='/Users/ZahraSh/Desktop/Testing Files'

nodesInf={'all.q@compute-0-0.local' : [0,1,2,3], 'all.q@compute-0-1.local' : [0,1,2,3], 
'all.q@compute-0-2.local' : [0,1,2,3], 'all.q@compute-0-3.local' : [0,1,2,3], 'all.q@compute-0-4.local'
 : [0,1,2,3], 'all.q@compute-0-5.local' : [0,1,2,3], 'all.q@compute-0-6.local' : [0,1,2,3]}

# .in file address
iPath=Path
# .top file address
pPath=Path+'/MD'+str(r)+'/top'
# .crd or .rst file address for input
cPath=Path+'/MD'+str(r)+'/MD'+str(r)+'-'+str(a)
# .rst (restart) file address output
rPath=Path+'/MD'+str(r)+'/MD'+str(r)+'-'+str(b)
# .out file address
oPath=Path+'/MD'+str(r)+'/MD'+str(r)+'-'+str(b)
# General path
path=Path+'/MD'+str(r)+'/MD'+str(r)+'-'+str(b)
# Structure list path
sPath=Path
sysList=open(sPath+'/strList','r')

try:
	os.mkdir(path)
	os.mkdir(path+'/PBS')
except OSError as exception:
	print "The directory exists"
	
nodesInf2=chFormat(nodesInf)
count=0

for sys in sysList:
	P = sys.split()
	sys=P[0]
	pbsText="""
#$ -S /bin/bash  # Set shell to run job
#$ -pe orte 1     # Request one processor from the OpenMPI parallel env.
#$ -o test4.log
##$ -cwd            # Run job from my current working directory
##$ -M              # set my email address
##$ -m              # Mail at beginning and end of job
#$ -q """+ nodesInf2[count][0] +""" # Choose queue to run job in
module load cuda
nvidia-smi

export PATH="/home/amoffet2/amber14/bin:$PATH"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export CUDA_HOME=/usr/local/cuda
export CUDA_VISIBLE_DEVICES="""+str(nodesInf2[count][1])+"""

cd """+path+"""
mkdir """+oPath+"/"+sys+"""
mpirun -np 1  pmemd.cuda.MPI -O -i """+iName+".in -o "+ oPath+"/"+sys+"/"+sys+".out -p "+pPath+"/"+sys +".top -c "+ cPath+"/"+sys+"/"+sys+"_md"+"-"+str(a) +".rst -r "+rPath+"/"+sys+"/"+sys+"_md"+str(r)+"-"+str(b)+".rst -x "+rPath+"/"+sys+"/"+sys+"_md"+str(r)+"-"+str(b)+".mdcrd "

	pbs=open(path+'/PBS/PBS_'+str(sys),'w')
	pbs.write(pbsText)
	pbs.close()
	count=count+1
