"""
This code is used to take the alpha simulation stoppingPower.IN files and plot the average energy of the particles as a function of distance traveled
"""

import os
import numpy as np
import matplotlib.pyplot as plt

directory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Stopping Power'
fileName = 'Stopping Power 0.0 mm'
fileNames = ['No Materials', 'Stopping Power 0.1 mm','Stopping Power 1.0 mm', 'Stopping Power 10.0 mm', 'Stopping Power 30.0 mm']
os.chdir("c:/Users/chris/OneDrive/Desktop/Alphasim/Stopping Power")

#"""
def getP(px, py, pz): #Function to return P^2 = px^2 + py^2 + pz^2
    return px**2 + py**2 + pz**2

def getE(P, m): #Function to return energy from P = p^2 and m
    return P/(2 * m)

#figure, axis = plt.subplots(1, len(fileNames), figsize = (16,4))

subplotIndex = 0

for fileName in fileNames:
    file = open(fileName + '.txt', 'r')

    lines = file.readlines() #Reads the entire file and stores it in lines
    detorNum = 100 #Amount of detector copies
    n = len(lines) #Length of the text file

    data = [] #Empty list to store lists of data
    for i in range(detorNum): #Creating detorNum amounts of empty lists to store data detected by detorNum amounts of detectors
        data.append([])

    j = 0 #Dummy index j to indicate the detector number
    k = 1 #Dummy index k to indicate the event number
    for i in range(2 * detorNum, n): #Reads the text file from the start of the data to the end of the file
        particleData = lines[i].split(' ') #Splits the information from each line into a list based on a space in between each data value
        px = float(particleData[3]) #Records the momentum from indices 3-5 of particleData
        py = float(particleData[4])
        pz = float(particleData[5])

        m = 3727.379 #Mass of alpha particle in MeV/c^2
        p = np.sqrt(px**2 + py**2 + pz**2)
        P = getP(px, py, pz) #Momentum squared P = p^2
        E = getE(P, m) #E=p^2/2m where P = p^2

        if float(particleData[8]) == k:
            data[j].append(E)
            j+=1
        else:
            j = 0
            k+=1
            continue

    def average(dataList): #Returns the mean average of an input list
        return sum(dataList)/len(dataList)

    z = 0
    position = []
    averageE = []
    for i in data: #Creating two lists to store the average energy averageE and its associated position
        if len(i) == 0: #If there were no detected events on detector data[i], skips the detector
            continue
        averageE.append(average(i))
        z+=.5
        position.append(z)
    """
    axis[subplotIndex].plot(position, averageE)
    axis[subplotIndex].set_xlabel('Depth (μm)')
    axis[subplotIndex].set_ylabel('Average Energy (MeV)')
    axis[subplotIndex].set_title(fileName)
    for i in range(len(position)):
        print(position[i], averageE[i])
    axis[subplotIndex].text(0, 0, 'Initial Energy: ' + f"{averageE[0]:.4f} MeV")
    subplotIndex+=1
    """
    plt.plot(position, averageE)
    plt.xlabel('Depth (μm)')
    plt.ylabel('Average Energy (MeV)')
    for i in range(len(position)):
        print(position[i], averageE[i])
    plt.text(0, 0.1, 'Initial Energy: ' + f"{averageE[0]:.4f} MeV")

#plt.savefig(directory + "\\" + fileName + '.png',format='png')
plt.suptitle('Function of Energy as Depth in Silicon at 30.0 mm')
plt.ylim(0,4)
plt.show()

#x y z Px Py Pz t PDGid EventID TrackID ParentID Weight Edep VisibleEdep Ntracks
#data starts at index lines[200]