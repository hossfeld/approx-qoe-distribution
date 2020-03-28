# -*- coding: utf-8 -*-
"""
An example is provided which uses the scripts to approximates a QoE distribution with a 
Beta distribution for given MOS and SOS parameter. More details on the 
background and a detailed description is provided in the paper [QoEMAN2020].

This tool is published under the license CC BY-SA 4.0 at
https://github.com/hossfeld/approx-qoe-distribution 

The following paper is to be cited in the bibliography whenever the tool is used.
[QoEMAN2020]
    Tobias Hossfeld, Poul E. Heegaard, Martin Varela, Lea Skorin-Kapov, Markus Fiedler. 
    "From QoS Distributions to QoE Distributions: a System's Perspective". 
    4th International Workshop on Quality of Experience Management (QoE Management 2020), 
    featured by IEEE Conference on Network Softwarization (IEEE NetSoft 2020), Ghent, Belgium.

Created on Thu Mar 26 21:51:00 2020
@author: Tobias Hossfeld
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import approxQoEdist as app

#%% read data from a file as Panda DataFrame to compute the SOS parameter a
# the ratings are given on a 5-point scale
df = pd.read_csv('exampleDataFrame.csv')
a = app.calcSOSParameter(df)
print(a)

#%% read data from a array provided in a csv file on a 5-point scale
# y = np.genfromtxt('exampleArray.csv', delimiter=',')
# print(app.calcSOSParameter(y))    

#%% Compare continuous distribution with measurement data for particular test condition
plt.figure(1)
plt.clf()
cond = 25 
ratings = df[df['condition']==cond]["rating"]
numberRatings = np.bincount(ratings,minlength=6)[1:] # number of ratings with score i
prob = numberRatings/np.sum(numberRatings)
mos = ratings.mean()

w=0.49
i = np.arange(1,6)
plt.bar(i-w/2, prob.cumsum(), label=f'measurement (cond={cond})', width=w, zorder=2)

rv_discrete = app.getDiscreteDistribution(mos=mos, sos_parameter=a)
plt.bar(i+w/2, rv_discrete.cdf(i), width=w, label='disc. Beta approx.', zorder=2)

x = np.linspace(1,5,100)

rv = app.getBetaDistribution(mos=mos, sos_parameter=a)
plt.plot(x, rv.cdf(x), 'k-', label='cont. Beta approx.')

plt.xlabel('rating')
plt.ylabel('CDF')
plt.legend()
plt.grid(which='major')

#%% Plot CDF of approximated continuous user rating distributions
plt.figure(2)
plt.clf()
x = np.linspace(1,5,100)
for mos in np.arange(1.5, 5, step=0.5):
    rv = app.getBetaDistribution(mos=mos, sos_parameter=a)
    plt.plot(x, rv.cdf(x), label=mos)
    
plt.xlabel('user rating')    
plt.ylabel('CDF')    
plt.legend(title='MOS')
plt.title(f'SOS parameter a={a:.2f}')
plt.grid(which='major')

#%% Plot discrete user rating distribution
plt.figure(3)
plt.clf()
i = np.arange(1,6)
sosa = 0.1
mosValues = np.arange(1.5, 5, step=0.5)
w = 0.9/len(mosValues) # width of the bar plots
for k, mos in enumerate(mosValues):
    rv = app.getDiscreteDistribution(mos=mos, sos_parameter=sosa)
    #plt.plot(i, rv.pmf(i), 'o:', label=mos)
    plt.bar(i+k*w, rv.pmf(i), width=w, label=mos, zorder=2)
    
plt.xlabel('user rating')    
plt.ylabel('probability')    
plt.legend(title='MOS',  bbox_to_anchor=(1, 1))
plt.title(f'SOS parameter a={sosa:.2f}')
plt.grid(which='major')
plt.xticks(i)
plt.tight_layout()
