import numpy as np
import mdtraj as md

couplingInf = np.loadtxt('ADRB2_HUMAN_ECScores.csv', delimiter = ',')

for i in range(len(couplingInf)):
