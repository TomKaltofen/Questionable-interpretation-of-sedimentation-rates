# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 08:49:23 2017

@author: Struktur
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
import random
import matplotlib.ticker as plticker

import sys
sys.path.insert(0,'D:\Tom kaltofen\Work work\custom_python_modules')
import my_plot as mp

# load time data
time = pd.read_csv('D:/Tom kaltofen/Work work/custom_python_modules/time.csv')
   
# load in all parts
namer = 'sadler3'
parts = os.listdir(namer)

for part in parts:

    # create figure
    y_page = mp.cm2inch(13)
    x_page = mp.cm2inch(23.00)
    fig, axes = plt.subplots(nrows=4, ncols=3,figsize=(x_page, y_page))
    font = {'family' : 'Times New Roman',
            'size'   : 9}
    plt.rc('font', **font)
    
    plt.gcf().subplots_adjust(left=0.05)
    plt.gcf().subplots_adjust(bottom=0.1)
    fig.subplots_adjust(hspace=.6)
    
    print part
    
    axe_x = 0
    axe_y = 0
    
    ### load whole dataset
    # load stratigraphy
    cols = ['strat_unit','depth_top','depth_bottom']
    data = pd.read_csv(namer+'/'+part, usecols = cols)
    data = mp.renamer2(data)
    data = pd.merge(data, time, on='strat_unit', how='inner')
    data = data.sort_values(by='age_bottom',axis=0)
        
    for lithology in data.strat_unit.unique():
               
        plt.suptitle(part[4:-4],fontsize=12)
        
        df = data[data.ix[:,'strat_unit'] == lithology]
        
        # calculate accumulation rate for each lithology of each well
        df['thickness'] = df['depth_bottom'] - df['depth_top']
        df['m_myr']     = df['thickness'] / df['time']
        
        # sample accumulation rates
        sample = (df['m_myr'])
       # sample = sample.sample(n=1000)
        sample = pd.Series.tolist(sample)
        sample = [ '%.1f' % elem for elem in sample ]
        sample = [float(i) for i in sample]
                  
        n = str(len(sample))
        
        # color
        color_counter = 0   
        color = mp.color(color_counter)   
        color_counter += 1  
                  
        # plot
        binwidth = 0.5
        axes[axe_x,axe_y].hist(sample, bottom = 0.1, bins=np.arange(min(sample), max(sample) + binwidth, binwidth),histtype='step', color='black') 
        
        
        
        #plt.yscale('log', nonposy='clip')
        axes[axe_x,axe_y].set_yscale('log', nonposy='clip')
        axes[axe_x,axe_y].set_xscale('log', nonposy='clip')
     #  axes[axe_x,axe_y].xscale('log', nonposy='clip')
         
        # title
        if lithology == 'Qua':
            lithology = 'Quaternary (Qua)'
        if lithology == 'UJu':
            lithology = 'Upper Jurassic (UJu)'
        if lithology == 'MTr':
            lithology = 'Middle Triassic (MTr)'
        if lithology == 'Ter':
            lithology = 'Tertiary (Ter)'
        if lithology == 'MJu':
            lithology = 'Middle Jurassic (MJu)'
        if lithology == 'LTr':
            lithology = 'Lower Triassic (LTr)'
        if lithology == 'UCr':
            lithology = 'Upper Cretaceous (UCr)'
        if lithology == 'LJu':
            lithology = 'Lower Jurassic (LJu)'
        if lithology == 'Ze':
            lithology = 'Zechstein (Ze)'
        if lithology == 'LCr':
            lithology = 'Lower Cretaceous (LCr)'
        if lithology == 'UTr':
            lithology = 'Upper Triassic (UTr)'
        if lithology == 'Rot':
            lithology = 'Upper Rotliegend (Rot)'            
        lithology = lithology + ' n = ' + n            
        axes[axe_x,axe_y].set_title(lithology,fontsize=9) 
        
        axes[axe_x,axe_y].set_xlim(10**0,10**3.5)
        axes[axe_x,axe_y].set_ylim(10**0,10**3.5)
        
        if axe_x == 3: 
            if axe_y == 1 :
                axes[axe_x,axe_y].set_xlabel('Accumulation rate (log r [m/Ma])')
        
        if axe_y == 0:
           # if axe_y == 1 :
                axes[axe_x,axe_y].set_ylabel('Frequency (log r)')
                        
        # axe position
        axe_x += 1
        if axe_x == 4:
               axe_x = 0
               axe_y += 1
    
                  
    fig.savefig('sadler3_res/'+str(part[4:-4])+'.png',dpi=300)


print 'done'




