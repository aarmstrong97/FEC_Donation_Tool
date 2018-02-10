###
#Basic visualization tool for comparison data of top 30 FEC donors between two election cycles
#Accepts input file from bigcontrib
#
#Austin Armstong, January 2018
###

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

prompt = input ("type the directory of a comparison file generated from the end of the 'bigcontrib.py' program:\n")

donorFile = open (prompt, "r")

donorNames =[line.split('|')[0] for line in donorFile.readlines()]
donorFile.seek(0,0)
donorDem = [int(line.split('|')[1]) for line in donorFile.readlines()]
donorFile.seek(0,0)
donorRep = [int(line.split('|')[2]) for line in donorFile.readlines()]
donorFile.seek(0,0)
donorOther = [int(line.split('|')[3]) for line in donorFile.readlines()]
donorFile.seek(0,0)
donorDemC = [int(line.split('|')[5]) for line in donorFile.readlines()]
donorFile.seek(0,0)
donorRepC = [int(line.split('|')[6]) for line in donorFile.readlines()]
donorFile.seek(0,0)
donorOtherC = [int(line.split('|')[7]) for line in donorFile.readlines()]

n_groups = 31

#graph the change in donor quantities between two years,
# * means did not donate to a identified democratic party
# ** means did not donate to a identified republican party
# a combination of both might support the conclusion of a new company?
for i in range(len(donorDem)):
    if donorDemC[i] == 0:
        donorNames[i]='*-> '+donorNames[i]
    if donorRepC[i] == 0:
        donorNames[i]='**-> '+donorNames[i]
    donorDemC[i]=(donorDem[i]-donorDemC[i])/100000
    donorRepC[i]=(donorRep[i]-donorRepC[i])/100000

  
index = np.arange(n_groups)

fig, (ax, ax2) = plt.subplots(2, 1, sharex=True)

rects1 = ax.bar(index, donorDemC, 0.3, alpha=0.4, color='b', label="Democrat")
rects2 = ax.bar(index+0.3, donorRepC, 0.3, color='r', label="Republican")
rects1a = ax2.bar(index, donorDemC, 0.3, alpha=0.4, color='b', label="Democrat")
rects2a = ax2.bar(index+0.3, donorRepC, 0.3, color='r', label="Republican")

ax2.set_xlabel('Companies')

plt.ylabel('Change in Dollars Donated\n(per $100,000)', multialignment='center')

ax2.set_ylim(-1,20)
ax.set_ylim(80,400)

ax2.axhline(linewidth=0.5, color='black')

ax2.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')
ax2.xaxis.tick_bottom()

d =.01
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)      
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs) 

kwargs.update(transform=ax2.transAxes) 
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs) 
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs) 


ax2.set_xticks(index+ 0.3/2)
ax2.set_xticklabels(donorNames, rotation='90')
ax.legend()

fig.tight_layout()
plt.show()
