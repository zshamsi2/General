######################
# Plot the distance between evolutionary couple residues in available crystal structures

import numpy as np
import mdtraj as md
from matplotlib import pyplot as plt

# coupling Information
ci = np.loadtxt('ADRB2_HUMAN_ECScores.csv', delimiter = ',')

maxP = ci[0][2]
eps = []
for i in range(len(ci)):
    if ci[i][2] > (maxP*0.1):
    #evolutionary pairs
        ep = [ci[i][0], ci[i][1], ci[i][2]]
        eps.append(ep)

# removing coupling with uncrystalized residues which are not exist in pdb
for i in range(len(eps)):
    if i<len(eps):
        print i
        print len(eps)
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

t1=md.load('3SN6-R.pdb')
t2=md.load('2RH1.pdb')

eps1 = [[eps[i][0], eps[i][1]] for i in range(len(eps))]
dist1=md.compute_contacts(t1, contacts=eps1, scheme='closest')
dist2=md.compute_contacts(t2, contacts=eps1, scheme='closest')

deltaDist = [dist1[0][0][i]-dist2[0][0][i] for i in range(len(dist1[0][0]))]
x = [eps[i][2] for i in range(len(eps))]
plt.scatter(x , np.absolute(deltaDist))
plt.savefig('fig1.png')
plt.show()

####################################################################################################################
# Calculating dihedral angles
####################################################################################################################

top1 = md.load('3SN6-R.pdb').topology
top2 = md.load('2RH1.pdb').topology

dhdrls101 = []
dhdrls102 = []
dhdrls201 = []
dhdrls202 = []

for i in range(len(eps)):
    atoms101 = top1.select("type == C and resid " + str(eps[i][0]))
    atoms102 = top1.select("type == C and resid " + str(eps[i][1]))
    atoms201 = top2.select("type == C and resid " + str(eps[i][0]))
    atoms202 = top2.select("type == C and resid " + str(eps[i][1]))
    
    dhdrl101 = md.compute_dihedrals(t1, atoms101)
    dhdrl102 = md.compute_dihedrals(t1, atoms102)
    dhdrl201 = md.compute_dihedrals(t2, atoms201)
    dhdrl202 = md.compute_dihedrals(t2, atoms202)
    
    dhdrls101.append(dhdrl101)
    dhdrls102.append(dhdrl102)
    dhdrls201.append(dhdrl201)
    dhdrls202.append(dhdrl202)
