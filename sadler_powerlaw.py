# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 08:49:23 2017

@author: Tom

Accumulation rate vs frequency

see graphic: sadler_powerlaw
"""


# load modules
import pandas as pd
import os
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
from scipy import stats

import sys
sys.path.insert(0,'D:\Tom kaltofen\Work work\custom_python_modules')
import my_plot as mp

# create figure
y_page = mp.cm2inch(8.25)
x_page = mp.cm2inch(8.25)
fig, axes = plt.subplots(nrows=1, ncols=1,figsize=(x_page, y_page))
font = {'family' : 'Times New Roman',
        'size'   : 9}
plt.rc('font', **font)
plt.gcf().subplots_adjust(left=0.15)
plt.gcf().subplots_adjust(bottom=0.15)
fig.subplots_adjust(hspace=.35)

### load whole dataset
# load stratigraphy
cols = ['strat_unit','depth_top','depth_bottom']
data = pd.read_csv('well_stratigraphy.csv',usecols = cols)
data = mp.renamer2(data)

# load time data
time = pd.read_csv('D:/Tom kaltofen/Work work/custom_python_modules/time.csv')

# merge datasets
df = pd.merge(data, time, on='strat_unit', how='inner')

# calculate accumulation rate for each lithology of each well
df['thickness'] = df['depth_bottom'] - df['depth_top']
df['m_myr']     = df['thickness'] / df['time']
print 'Single accumulation rates calculated.'

# sample accumulation rates
sample = df['m_myr']
sample = sample.sample(n=10000)
sample = pd.Series.tolist(sample)
sample = [ '%.1f' % elem for elem in sample ]
sample = [float(i) for i in sample]

# plot
binwidth = 5
axes.hist(sample, bins=np.arange(min(sample), max(sample) + binwidth, binwidth),histtype='step', color='black') 

#axes.set_xlim(10**0,10**7)
#axes.set_ylim(10**-4.1,10**)
#axes.set_ylabel('P(x)') 
#axes.set_xlabel('x')

#print df

# plot whole dataset
#axes.plot(df['time'], df['m_myr'], 'or',color='black')

plt.yscale('log', nonposy='clip')
plt.xscale('log', nonposy='clip')


axes.set_xlim(10**0,10**4)
axes.set_ylim(10**0,10**4)
axes.set_ylabel('Frequency (r)') 
axes.set_xlabel('Accumulation rate (r)')



fig.savefig('sadler_powerlaw',dpi=600)    
print 'done'




