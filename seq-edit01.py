import numpy as np
f = open('B2AR-align-Identity.fasta')
lines = f.read().split('>')
unfrag = ['>'+line for line in lines if line.find('Fragment')==-1]
frag = ['>'+line for line in lines if line.find('Fragment')!=-1]
np.savetxt('test-frag.txt', frag, delimiter=" ", fmt="%s") 
np.savetxt('test-unfrag.txt', unfrag, delimiter=" ", fmt="%s") 
