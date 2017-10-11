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


# create figure
y_page = mp.cm2inch(16)
x_page = mp.cm2inch(16)
fig, axes = plt.subplots(nrows=4, ncols=4,figsize=(x_page, y_page))
font = {'family' : 'Times New Roman',
        'size'   : 9}
plt.rc('font', **font)

plt.gcf().subplots_adjust(left=0.02)
plt.gcf().subplots_adjust(bottom=0.1)
fig.subplots_adjust(hspace=.6)

fig.subplots_adjust(left=0.1)
                #    left=0.08, right=
                #    0.98, wspace=0.3)
axe_x = 0
axe_y = 0


# load time data
time = pd.read_csv('D:/Tom kaltofen/Work work/custom_python_modules/time.csv')

# graph, values from excel
# y = 1101.3x-1.334
x_s = []
y_s = []
for x in range(1,70,1):
    x_s.append(x)
    y_s.append(621.12 / (x**1.157) )

# load in all parts
namer = 'CREATE_WELLS_OF_SADLER_FOR_INPUT/output'
parts = os.listdir(namer)

cols = ['strat_unit','depth_top','depth_bottom']   

count_abc = 0
abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
 
for part in parts:
    
    if not part == parts[1]:
        # read in which wells    
        df = pd.read_csv(namer+'/'+part, usecols = cols)
        df = mp.renamer2(df)
        df = pd.merge(df, time, on='strat_unit', how='inner')
     
        # calculate accumulation rate for each lithology of each well
        df['thickness'] = df['depth_bottom'] - df['depth_top']
        df['m_myr']     = df['thickness'] / df['time']
        
        # get mean values for each lithology
        mean_m_myr = []
        strata = []
        t = []
    
        strat_units = df['strat_unit'].tolist()
        strat_units = list(set(strat_units))
        mean_m_myr = []
        strata = []
        times = []
        mean_thickness = []
        for strat in strat_units:
            
            thick_df = df.loc[df['strat_unit'] == strat]
            mean_thickness.append(thick_df['thickness'].mean())
            
            df_m_myr = df.loc[df['strat_unit'] == strat]
            mean_m_myr.append(df_m_myr['m_myr'].mean())
            strata.append(strat)
        d = {'strat_unit': strata,'mean_m_myr': mean_m_myr}
        df = pd.DataFrame(data=d)
        df = pd.merge(df, time, on='strat_unit', how='inner')
        df = df.sort_values(by='age_bottom',axis=0)
        
    if not part == parts[0]:
    
        df = np.log10(df.ix[:,['mean_m_myr','time']])
         
        if part == parts[1]:
            lin = stats.linregress(df['mean_m_myr'],df['time'])
            slope = lin[0]     #mx
            intercept = lin[1] #n                        
            ys = []
            xs = []
            for x in range(0,100,1):            
                ys.append(slope * x + intercept)
                xs.append(x)
            observed = ys
            r2 = lin[2]
                  
        else:
                lin2 = stats.linregress(df['mean_m_myr'],df['time'])
                slope2 = lin2[0]     #mx
                intercept2 = lin2[1] #n                        
                ys2 = []
                xs2 = []
                for x2 in range(0,100,1):            
                    ys2.append(slope2 * x2 + intercept2)
                    xs2.append(x2)
                calculated = ys2
                r2 = mp.coefficient_of_determination(np.asarray(observed), np.asarray(calculated))        
                
        axes[axe_x,axe_y].plot(xs, ys,color='grey',linewidth=1) 

    if part == parts[0]:
        axes[axe_x,axe_y].plot(x_s, y_s,color='grey',linewidth=1) 

        # plot data points
        color_counter = 0
        for index, row in df.iterrows():
        
                x= df.ix[index,'time']
                y= df.ix[index,'mean_m_myr']
                color = mp.color(color_counter)
                axes[axe_x,axe_y].plot(x, y, 'or',color=color)    
                color_counter += 1
        
        axes[axe_x,axe_y].set_xlim(0,70)
        axes[axe_x,axe_y].set_ylim(0,150)  
        
    # plot data points
    color_counter = 0

    for index, row in df.iterrows():  
                x= df.ix[index,'time']
                y= df.ix[index,'mean_m_myr']

                color = mp.color(color_counter)
                axes[axe_x,axe_y].plot(x, y, 'or',color=color)   
                color_counter += 1  
                
    if axe_x == 3:        
        if axe_y == 0:
            axes[axe_x,axe_y].set_xlabel('t and log t [Ma]')
        else: 
            axes[axe_x,axe_y].set_xlabel('log t [Ma]')
        
    if axe_y == 0:
        if axe_x == 0:
            axes[axe_x,axe_y].set_ylabel('r and log r [m/Ma]')
        else:
            axes[axe_x,axe_y].set_ylabel('log r [m/Ma]')
                        
    axes[axe_x,axe_y].set_title(part[4:-4],fontsize=9)  
    
    if not part == parts[0]:
       axes[axe_x,axe_y].set_xlim(0.2,2.0)
       axes[axe_x,axe_y].set_ylim(0,2.6)
       
    loc = plticker.MultipleLocator(base=0.4)
    if not (axe_x == 0 and axe_y == 0):
        axes[axe_x,axe_y].xaxis.set_major_locator(loc)
   
    ################################################# tick functions     
    # plotting   
 #  axes[axe_x,axe_y].xaxis.set_visible(False)
 #  axes[axe_x,axe_y].yaxis.set_visible(False)    
 #  if axe_x == 3:
 #      axes[axe_x,axe_y].xaxis.set_visible(True)
  # if axe_y == 0:
  #       axes[axe_x,axe_y].yaxis.set_visible(True)  
           
  # if axe_x == 0 and axe_y == 0:
  #    axes[axe_x,axe_y].xaxis.set_visible(True)
    
#   if axe_x == 3:
#        axes[axe_x,axe_y].tick_params(axis='x',top='off')
    
#   if axe_y == 0:
#        axes[axe_x,axe_y].tick_params(axis='y',bottom='off')
            
   # axes[axe_x,axe_y].tick_params(axis='x',which='both',top='off',bottom='off')
   # axes[axe_x,axe_y].tick_params(axis='y',top='off')
             # changes apply to the x-axis
            # both major and minor ticks are affected
          # ticks along the bottom edge are off
             # ticks along the top edge are off)

    
    if not part == parts[0]:
        r2=('R=' + str(round(r2,2)))
        axes[axe_x,axe_y].text(0.6,0.8,r2,transform=axes[axe_x,axe_y].transAxes)   
    axes[axe_x,axe_y].text(0.83,0.6,abc[count_abc],transform=axes[axe_x,axe_y].transAxes)       
    count_abc += 1
    # axe position
    axe_x += 1
    if axe_x == 4:
           axe_x = 0
           axe_y += 1
           
          
#fig.savefig('sadler.png',dpi=600)

   
print 'done'




