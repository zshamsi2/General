##################
# Find the distance of the closet ion from the binding pocket in the transporter

import glob
import numpy as np
import mdtraj as md
from matplotlib import pyplot as plt
topN = A2AR-strip.prmtop
topN = 'A2AR-strip.prmtop'
name = 'A2AR-alltrjs01.mdcrd'

ionAtoms = [4738, 4739, 4740, 4741, 4742, 4743, 4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752, 4753, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773]
pocketInexAtom = 807

t = md.load(name ,top=topN)
nFrames = t.n_frames
dist = np.empty(nFrames)

for frame in range(nFrames):
        topIonAtoms = [ion for ion in ionAtoms if t.xyz[frame][ion][2]<3]
        allDist = md.compute_distances(t,[[pocketInexAtom, ion] for ion in topIonAtoms])
        frameDist = allDist[frame]
        dist[frame] = frameDist.min()

plt.show()
