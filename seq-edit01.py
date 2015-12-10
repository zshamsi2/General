import numpy as np
f = open('B2AR-align-Identity.fasta')
lines = f.read().split('>')
unfrag = ['>'+line for line in lines if line.find('Fragment')==-1]
frag = ['>'+line for line in lines if line.find('Fragment')!=-1]
np.savetxt('test-frag.txt', frag, delimiter=" ", fmt="%s") 
np.savetxt('test-unfrag.txt', unfrag, delimiter=" ", fmt="%s") 

import numpy as np
f=open('str')
lines = f.read().split('\n')
frag = ['AS1'+line for line in lines]
np.savetxt('AS1_list', frag, delimiter=" ", fmt="%s") 

for i in `seq 0 500`
do
cp SampleR4_${i}.prmtop AS1_SampleR4_${i}.prmtop
done
