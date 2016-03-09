import pickle
import numpy as np
from msmbuilder.msm import MarkovStateModel
from msmbuilder.msm import implied_timescales
import pylab as plt
import matplotlib as mpl
from msmbuilder.utils import io

font = {'family':'Times New Roman', 'size': 12}
plt.rc('font', **font)
cl = pickle.load(open('clustering.pkl','rb'))
n_timescales=10
stepS = 1.2
lag_times=[1, 2, 3,4, 5,6, 7,8, 9,10,11,12,13,14,15,16,17]
l = len(lag_times)

ts=np.zeros([10,l])

ns_lt=np.ndarray.tolist(stepS*np.array(lag_times))
index = 0

for i in lag_times:
    msm=MarkovStateModel(lag_time=i, n_timescales=n_timescales)
    msm.fit_transform(cl.labels_)
    ts[:,index]=msm.timescales_
    index=index+1
    io.dump(msm,'MSM'+str(i)+'.pkl')

"""
for i in lag_times:
    msm = io.load('MSM'+str(i)+'.pkl')
    ts[:,index]=msm.timescales_
    index=index+1
"""

fig, ax = plt.subplots(1,1)

for i in range(10):
  j=i+1
  if j==1:
    k='st'
  elif j==2:
    k='nd'
  elif j==3:
    k='rd'
  elif j>3:
    k='th'
  l=str(j)+k
  ax.plot(ns_lt[0:-1],stepS*ts[i,0:-1],label="%s timescale" %l)
  #ax.plot(ns_lt[0:-1],stepS*ts[i,0:-1],'o',label="%s timescale" %l)

fig.set_figheight(4)
fig.set_figwidth(5.5)

#fig.set_size_inches(3.5, 2.333)
#fig.set_size_inches(3.5, 2.333)

ax.set(xlabel='Lag time (ns)',ylabel='Implied timescales (ns)')
ax.semilogy()

fig.savefig('test1.png',dpi=300,bbox_inches='tight')
fig.show()
