#Find the gain of each sensor
#Pin sensor is without the gain layer
#Combine the pin sensors data all into one
#Find the mean and rms of the combined pin sensors data
#Subtract the mean and rms from the normal sensor at each angle
#Focusing on just the charge

#RMS on RMS

#W8 300V corrupted
#W14 corrupted

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
from sklearn.metrics import auc

sensorDirectory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Data\\W8\\200V'
sensorFolder = []
pinSensorDirectory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Data\\W8_pin\\150V'
pinSensorFolder = []
sensorName = 'FBK Space Sensor W8 200V vs W8 Pin 150V'
skip = 4 #How many files to skip to make data processing faster, Ex: skip = 1 increments by 1, meaning all data will be processed
resistance = 470

os.chdir(sensorDirectory)
for x in os.listdir(): #Creates a list of the folder names in the sensor directory
    sensorFolder.append(x)

print(sensorFolder)

os.chdir(pinSensorDirectory)
for x in os.listdir(): #Creates a list of the folder names in the pin sensor directory
    pinSensorFolder.append(x)

print(pinSensorFolder)

def getData(folder, directory, skip = skip): #Gets the data from an inputted folder
    files = []
    os.chdir(directory)

    print('Getting data from: ' + folder)

    for x in os.listdir(folder): #Creates a list of the file names within the inputted folder that end with .csv
        if x.endswith('.csv'):
            files.append(x)
    
    os.chdir(folder)

    data = []
    if skip == 0:
        for i in range(0, len(files)): #Creates a list data of pandas dataframes containing the csv data for each file in the specified folder
            data.append(pd.read_csv(files[i], names = ('Time', 'Voltage')))
    else:
        for i in range(0, len(files), skip): #Creates a list data of pandas dataframes containing the csv data for each file in the specified folder with incremental skips
            data.append(pd.read_csv(files[i], names = ('Time', 'Voltage')))
    
    #print(data)
    #print(data[0]['Voltage'])

    #maxVoltages = []
    
    charges = []
    for i in range(0, len(data)):
        time = data[i]['Time'] * 1e9 #Accessing time and voltage from the list data and converting to ns and mV respectively
        voltage = data[i]['Voltage'] * 1e3
        #print(data[i]['Time'])
        #print(time)
        
        baselineVoltage = []
        for j in range(0, len(time), 10):
            if(time[j] > -10 and time[j] < -1.5):
                baselineVoltage.append(voltage[j]) #Appends the voltages for times > 10 and < -1.5 ns to baselineVoltage
        
        meanBaselineVoltage = np.mean(baselineVoltage) #Calculates the average baseline voltage for each data frame in data
        correctedVoltage = voltage - meanBaselineVoltage #Corrects the voltage based off the average baseline voltage
        #maxVoltage = np.max(correctedVoltage) #Finds the maximum corrected voltage
        #maxVoltages.append(maxVoltage)

        charge = auc(time, correctedVoltage)/resistance #Integrates the current I = V/R with respect to time
        charges.append(charge) #Appends the charge for each file to list charges
    
    return charges #Returns a list of charges for the files read

def gaussianFit(x, amplitude, mu, sigma):
    y = amplitude * np.exp(-(x - mu)**2 / (2 * sigma**2)) #Defines the gaussian function to be used in the curve fitting
    return y

colours = ['r', 'g', 'b', 'c', 'm', 'y'] #Colours to be used when plotting
def histogramPlot(folder, directory, numBins = 200, skip = skip, meanDiff = 0, rmsDiff = 0): #Used for iterating over entire directory and the folders inside of it
    for i in range(len(folder)): #Iterates over every folder in the directory
        charges = getData(folder[i], directory, skip) #Gathers the charges from each folder in the directory
        charges = [charge - meanDiff for charge in charges] #Subtracts meanDiff from each charge in charges
        plt.hist(x = charges, density = False, bins = numBins, color = colours[i], histtype= 'step') #Creates a histogram for the charges

        print('Plotting data from: ' + folder[i])

        frequencies, bins = np.histogram(charges, numBins) #Creates a numerical list of frequencies and their corresponding bins for the charges
        nonZeroIndices = np.where(frequencies>0)[0] #Creates a list of the indices where there are non zero frequencies for a bin
        nonZeroFrequencies = frequencies[nonZeroIndices] #Creates list of non zero frequencies in the histogram and their corresponding bins
        nonZeroBins = bins[nonZeroIndices]

        gaussianFitParameters, gaussianFitUncertainties = sp.optimize.curve_fit(gaussianFit, nonZeroBins, nonZeroFrequencies) #Gathers the parameters and their uncertainties for a gaussian fit given the input bins and frequencies
        meanCharge = f'{gaussianFitParameters[1]:.5f}' #Truncates the mean charge and RMS
        meanChargeRMS = f'{np.sqrt(gaussianFitParameters[2]**2 + rmsDiff**2):.5f}'
        fileLabel = folder[i][folder[i].rfind('_') + 1:] + ', mean = ' + meanCharge + ' pC, rms = ' + meanChargeRMS + ', ' + str(len(charges)) + ' pulses' #Creates the label for the legend
        xFit = np.linspace(nonZeroBins[0], nonZeroBins[-1], 200) #Creates a linear space from the lowest to highest non zero frequency bin
        yFit = gaussianFit(xFit, *gaussianFitParameters) #Creates the gaussian fit for the parameters estimated by curve_fit
        plt.plot(xFit, yFit, lw = 1, color = colours[i], label=fileLabel) #Plots the gaussian fit
        #print(gaussianFitParameters, gaussianFitUncertainties)

def pinHistogramPlot(folder, directory, numBins = 200, skip = skip, combineFolders = True): #Used for combining folders and returning the mean and RMS
    if(combineFolders == True):
        pinSensorCharges = []
        combinedPinSensorCharges = []
        print('Starting combined sensors')
        for i in range(len(folder)):
            pinSensorCharges.append(getData(folder[i], directory, skip))
        for i in pinSensorCharges:
            combinedPinSensorCharges += i
        
        print('Plotting combined sensors')
        
        plt.hist(x = combinedPinSensorCharges, density = False, bins = numBins, color = colours[-1], histtype= 'step') #Creates a histogram for the charges

        frequencies, bins = np.histogram(combinedPinSensorCharges, numBins) #Creates a numerical list of frequencies and their corresponding bins for the charges
        nonZeroIndices = np.where(frequencies>0)[0] #Creates a list of the indices where there are non zero frequencies for a bin
        nonZeroFrequencies = frequencies[nonZeroIndices] #Creates list of non zero frequencies in the histogram and their corresponding bins
        nonZeroBins = bins[nonZeroIndices]

        gaussianFitParameters, gaussianFitUncertainties = sp.optimize.curve_fit(gaussianFit, nonZeroBins, nonZeroFrequencies) #Gathers the parameters and their uncertainties for a gaussian fit given the input bins and frequencies
        meanCharge = f'{gaussianFitParameters[1]:.5f}' #Truncates the mean charge and RMS
        meanChargeRMS = f'{gaussianFitParameters[2]:.5f}'
        fileLabel = 'Combined, mean = ' + meanCharge + ' pC, rms = ' + meanChargeRMS + ', ' + str(len(combinedPinSensorCharges)) + ' pulses' #Creates the label for the legend
        xFit = np.linspace(nonZeroBins[0], nonZeroBins[-1], 200) #Creates a linear space from the lowest to highest non zero frequency bin
        yFit = gaussianFit(xFit, *gaussianFitParameters) #Creates the gaussian fit for the parameters estimated by curve_fit
        plt.plot(xFit, yFit, lw = 1, color = colours[-1], label=fileLabel) #Plots the gaussian fit
        return gaussianFitParameters[1], gaussianFitParameters[2]
    else:
        histogramPlot(folder, directory, numBins, skip)

#print(getData(pinSensorFolder[0], pinSensorDirectory))

pinHistogramPlot(pinSensorFolder, pinSensorDirectory, 200, 1, False)
meanDiff, rmsDiff = pinHistogramPlot(pinSensorFolder, pinSensorDirectory, 200, 1, True)
print(f'{meanDiff=}, {rmsDiff=}')
histogramPlot(sensorFolder, sensorDirectory, 200, 1)#, meanDiff, rmsDiff)
plt.title(sensorName)
plt.xlabel('Charge (pC)')
plt.ylabel('Frequency')
plt.legend(loc = 'upper left', fontsize =  14)
#plt.savefig(sensorDirectory + '\\' + sensorName)
plt.show()