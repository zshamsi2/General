import numpy as np
import mdtraj as md

#coupling Information
ci = np.loadtxt('ADRB2_HUMAN_ECScores.csv', delimiter = ',')

maxP = ci[0][2]
eps = []
for i in range(len(ci)):
  if ci[i][2] > maxP*0.1:
    #evolutionary pairs
    ep = [ci[i][0], ci[i][1]]
    eps.append(ep)

# removing coupling with uncrystalized residues which are not exist in pdb
for i in range(len(eps)):
  while 175<eps[i][0]<179 or 175<eps[i][1]<179 or 230<eps[i][0]<265 or 230<eps[i][1]<265 or eps[i][0]<30 or eps[i][1]<30 or 341<eps[i][0] or 341<eps[i][1]:
    eps.pop(i)

for i in range(len(eps)):
  a = eps[i][0]
  b = eps[i][1]
  if 29<a<176:
    eps[i][0] = a-30
    elif 178<a<231:
      eps[i][0] = a-33
      elif 264<a<342:
        eps[i][0] = a-67
        
  if 29<b<176:
    eps[i][1] = b-30
    elif 178<b<231:
      eps[i][1] = b-33
      elif 264<b<342:
        eps[i][1] = b-67

t=md.load('3SN6-R.pdb')
t2=md.load('2RH1.pdb')
dist=md.compute_contacts(t, contacts=eps, scheme='closest')
dist2=md.compute_contacts(t2, contacts=eps, scheme='closest')


