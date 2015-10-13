import os

iName='aMD'
r=1 #Sampling round
a=0 #input index
b=1 #output index
Path='/Users/ZahraSh/Desktop/Testing Files'

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

os.mkdir(path)
os.mkdir(path+'/PBS')

sysList=open(sPath+'/strList','r')
for sys in sysList:
	pbsText="""
#$ -S /bin/bash  # Set shell to run job
#$ -pe orte 1     # Request one processor from the OpenMPI parallel env.
#$ -o test4.log
##$ -cwd            # Run job from my current working directory
##$ -M              # set my email address
##$ -m              # Mail at beginning and end of job
#$ -q """+ "all.q" +""" # Choose queue to run job in
module load cuda
nvidia-smi

export PATH="/home/amoffet2/amber14/bin:$PATH"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export CUDA_HOME=/usr/local/cuda
export CUDA_VISIBLE_DEVICES=1

cd """+path+"""
mkdir """+oPath+"/"+sys+"""
mpirun -np 1  pmemd.cuda.MPI -O -i """+iName+".in -o "+ oPath+"/"+sys+"/"+sys+".out -p "+pPath+"/"+sys +".top -c "+ cPath+"/"+sys+"/"+sys+"_md"+"-"+str(a) +".rst -r "+rPath+"/"+sys+"/"+sys+"_md"+str(r)+"-"+str(b)+".rst -x "+rPath+"/"+sys+"/"+sys+"_md"+str(r)+"-"+str(b)+".mdcrd "

	pbs=open(path+'/PBS/PBS_'+str(sys),'w')
	pbs.write(pbsText)
	pbs.close()
