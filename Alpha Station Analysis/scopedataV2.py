#Units in ns, pC, mV

import pandas as pd
import glob
import os
import numpy  as np
from sklearn.metrics import auc
from scipy.stats import norm
import scipy
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import arange
import itertools
import scipy.optimize
import random
import matplotlib.colors as mcolors


def gaussfit(x,a,mu,s): #Gaussian fit
    gauss = a * np.exp(-((x-mu)**2/(2*s**2))) 
    return gauss

folder = 'C:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Data\\W1\\240V' #"C:/Users/tjste/OneDrive/Documents/Alpha_Station/fbkSpaceSensorz/W14/W14/300V" #Import folder
name = "FBK Space Sensor W1 240V" #Sensor name

#Extracts files from imported folder
#csv data as 
files = [x for x in os.listdir(folder)] #Grabs names from the folder
d = {}
skip=1  
#nbins = 150
print(files) 
os.chdir(folder)
def signalstuff(files):
    os.chdir(folder)
    csvs = [x for x in os.listdir(files) if x.endswith('.csv')] #Creates list of file names ending with .csv

    meow = [os.path.splitext(os.path.basename(x))[0] for x in csvs]

    data = []
    os.chdir(files)
    for i in range(len(meow)): #Extracts data from the file and puts into pandas data frame

        d[meow[i]] = pd.read_csv(csvs[i], names=('v', 't' ))
        #print(d[fns[i]])
        data.append(d[meow[i]].transpose())
        data[i]=np.array(data[i])   
    MeanVolt = pd.DataFrame()
    MeanTime = pd.DataFrame()
    
    Pmax, volt1, time1, Area1, avetime, avepuls = [[] for _ in range(6)]

    for j in range(0,len(data),skip):

        #Gathers the time and voltage from the .csv file
        time = data[j][0][:]*1e9 #Converts to ns
        volt = data[j][1][:]*1e3 #Converts to mV

        #a1 = np.max(volt)
        #if a1 > 0.10:
        #    volt2.append(volt)
        #    time2.append(time)

        #Pmax.append(a1)
        #volt5.append(volt)
        #time5.append(time)
        
        ped_bounds5=[]
        for ij in range(len(time)):
               if time[ij] > -10 and time[ij] < -1.5: #Records the baseline voltage from -10 to -1.5 ns 
                 bounds = volt[ij]
                 ped_bounds5.append(bounds)
               else:
                   continue

        Ped = np.mean(ped_bounds5) # determine baseline 
        corr= volt - Ped #Subtracts the baseline voltage from all the voltages
        a1 = np.max(corr) #Finds the maximum voltage
        #if a1>35: #Removes higher outlier voltages, trigger level removes the lower voltages
        #    continue




        #voltCorr.append(corr)
        #print(corr)
        volt1 = []
        time1 = []


 
        for jj in range (len(time)):
                if time[jj] > -1 and time[jj] < 6.5: #Finds the corrected voltage in the time range of -1 to 6.5 ns
                    v=corr[jj]#volt[jj]
                    t=time[jj]
                    volt1.append(v)#/50) afterdiscusion this factor of 50 ohms is wrong
                    time1.append(t)

                else: 
                    continue        

        
        area = auc(time1,volt1)/470 #Q = integral(I)dt = integral(V/R)dt

        #if area>.4 or area<.1: #Filters outlier charges that are too high or low
        #   continue

        avetime.append(time1)
        avepuls.append(volt1)
        Pmax.append(a1)
        Area1.append(area)

    print(len(Area1)) #Prints how many pulses analyzed post filtering
    MeanTime= pd.DataFrame(avetime)
    MeanVolt = pd.DataFrame(avepuls)
   
    mt = MeanTime.mean(axis = 0)
    
    mv = MeanVolt.mean(axis = 0)

    #print(volt1)
    #print(MeanVolt)

    return mv, mt, Area1, Pmax


colorz = ['b', 'g', 'r', 'c', 'm', 'y']
def traceploter(MeanVolt, MeanTime, Area, Pmax, j): #Plots mean time and voltage
    plt.plot(MeanTime, MeanVolt, color=colorz[j], label='Average Trace ' + files[j][files[j].rfind('_') + 1:])
    plt.subplot(311)

def histoareaplot(MeanVolt, MeanTime, Area, Pmax, j, nbins, minarea, maxarea): #Plots the charge
    y51=plt.hist(Area, density=False, bins = nbins, color=colorz[j], histtype='step', range=(minarea, maxarea))
    yhist51, xhist51 = np.histogram(Area, 150)
    xh51 = np.where(yhist51 > 0)[0]
    yh51 = yhist51[xh51]
    xt51 = xhist51[xh51]
    popt51, pcov51 = curve_fit(gaussfit, xt51, yh51)#, [.15, 0.10, 0.001])
    a51, b51, c51 = popt51
    b51f=float("{0:.5f}".format(b51))
    c51f=float("{0:.5f}".format(c51))
    equation51 = files[j][files[j].rfind('_') + 1:]+ " mean= " + str(b51f)+ ' ,rms= '+ str(c51f)
    i = np.linspace(xt51[0], xt51[-1], 200)
    yfit51=gaussfit(i, *popt51)
    plt.plot(i, yfit51, lw=1.0, color=colorz[j], label=equation51)

def histopmaxplot(MeanVolt, MeanTime, Area, Pmax, j, nbins, minvolt, maxvolt): #Plots the voltage
    y52=plt.hist(Pmax, density=False, bins=nbins, color=colorz[j], histtype='step', range=(minvolt, maxvolt))
    yhist52, xhist52 = np.histogram(Pmax, 150)
    xh52 = np.where(yhist52 > 0)[0]
    yh52 = yhist52[xh52]
    xt52 = xhist52[xh52]
    popt52, pcov52 = curve_fit(gaussfit, xt52, yh52, [30, 20, 50])
    a52, b52, c52 = popt52
    b52f=float("{0:.5f}".format(b52))
    c52f=float("{0:.5f}".format(c52))
    equation52 = files[j][files[j].rfind('_') + 1:]+ " Mean= " + str(b52f) + ' ,rms= '+ str(c52f)
    i = np.linspace(xt52[0], xt52[-1], 200)
    yfit52=gaussfit(i, *popt52)
    plt.plot(i, yfit52, lw=1.0, color=colorz[j], label=equation52)


MeanVolts, MeanTimes, Areas, Pmaxs = [[] for _ in range(4)]

MeanVoltsall, MeanTimesall, Areasall, Pmaxsall, rangevolt, rangearea = [[] for _ in range(6)]

for j in range(len(files)): #Converting the data in to list form to be plotted
    MeanVolt, MeanTime, Area, Pmax = signalstuff(files[j])
    MeanVoltsall.append(MeanVolt)
    MeanTimesall.append(MeanTime)
    Areasall.append(Area)
    Pmaxsall.append(Pmax)
    rangevolt.append(max(Pmax))
    rangearea.append(max(Area))
    rangevolt.append(min(Pmax))
    rangearea.append(min(Area))
    
minvolt=min(rangevolt)
maxvolt=max(rangevolt)
minarea=min(rangearea)
maxarea=max(rangearea)
plt.figure(figsize=[12,10])
plt.suptitle(name, fontsize=20)

plt.subplot(311)


for j in range(len(files)):
    traceploter(MeanVoltsall[j], MeanTimesall[j], Areasall[j], Pmaxsall[j], j)

plt.xticks(fontsize=15, rotation=0)
plt.yticks(fontsize=15, rotation=0)
plt.xlabel('Time [ns]', fontsize=18)
plt.ylabel('Voltage[mV]', fontsize=18)
plt.legend(loc='upper left', fontsize=14)


plt.subplot(312)

for j in range(len(files)):
    histoareaplot(MeanVoltsall[j], MeanTimesall[j], Areasall[j], Pmaxsall[j], j, 150, minarea, maxarea)


plt.xticks(fontsize=15, rotation=0)
plt.yticks(fontsize=15, rotation=0)
plt.xlabel('Area [pC]', fontsize=18)
plt.ylabel('Frequency', fontsize=18)
plt.legend(loc='upper left', fontsize=14)



plt.subplot(313)
for j in range(len(files)):
    histopmaxplot(MeanVoltsall[j], MeanTimesall[j], Areasall[j], Pmaxsall[j], j, 150, minvolt, maxvolt)



plt.xticks(fontsize=15, rotation=0)
plt.yticks(fontsize=15, rotation=0)
plt.xlabel('Voltage [mV]', fontsize=18)
plt.ylabel('Frequency', fontsize=18)

plt.legend(loc='upper left', fontsize=14)
plt.tight_layout()


plt.show()