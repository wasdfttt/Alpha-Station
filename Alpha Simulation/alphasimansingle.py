import os
import numpy as np
import matplotlib.pyplot as plt

"""
This code is used to anaylyze the simulation results to obtain the distribution of energy, angles, and plot the final 2-D position of the particles
"""


#these are the only variables you should need to change while analysing the data everything else should be automated i think
directory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Collum 10 - 20 mm'
detector_name = "Collum .5mmx50mm 10mm 0 deg hit or miss"
file_name = detector_name
os.chdir(directory)
file_placeholder = open(file_name + ".txt", 'r')
detector_angle = 0 #(3.14/4) #use radians
meanx = .08
meany = 115

'''
this is to remove particles that graze the collimator if you are runing a simulation with degraded particles 
set this to zero then just look at it and guess what it should be if you dont really know just ask me
'''
min_energy = 0 #MeV

line_list = file_placeholder.readlines()
n = len(line_list)
print(n)
#defining all the lists used
som = 0
sumer = 0
angax, Pax, zed, Eax, justx, justy, misangax, misPax, miszed, misEax, missjustx, missjusty, angax, xhit, yhit, angmiss = [[] for _ in range(16)]
#defining detector length
detlength = 1.3 #mm

def findmiss(xposition, yposition, ang):
    """
    this is the test for whether or not the particle hits the detector or board, this is only relevent 
    if you are testing for this otherwise it is redundent and you should comment it out below    
    """
    test = 1
    if xposition>(detlength/2) or xposition<(-(detlength/2)) or yposition<(-(detlength/2)) or yposition>(detlength/2):
        misangax.append(ang)
        missjustx.append(xposition)
        missjusty.append(yposition)
        test = 0
        return test

    else:
        return test

for i in range(2,n):
    #exstracting data from file outputted
    particle_hit = line_list[i].split(' ')
    #position
    xposition =float(particle_hit[0])
    yposition = float(particle_hit[1])
    #momentum vectors
    Px = float(particle_hit[3])
    Py = float(particle_hit[4])
    Pz = float(particle_hit[5])

    #calculating magnitude of momentum, angle, and energy
    P = np.sqrt((Px**2)+(Py**2)+(Pz**2))
    ang = np.arccos(Pz/P)
    E = (P*.0542)/2

    # if simulating detector and board use the next two lines for position

    test = findmiss(xposition, yposition, ang)
    if test == 0: continue
    
    if E<min_energy:
        continue
    #adding detected particles information to their respective lists for all particles

    Pax.append(P)
    angax.append(ang)
    Eax.append(E)
    justx.append(xposition)
    justy.append(yposition)
    som += ang
mean = som/len(angax)
for i in range(len(Pax)):
    sumer += Pax[i]
iner = 0
for i in range(len(Pax)):
    iner += (Pax[i]-mean)**2

SD = np.sqrt(iner/len(Pax))
print(f'{mean=:.5f}')
print(SD)
#generating plot
figure, axis = plt.subplots(1, 3,figsize=(16, 4), gridspec_kw = {'width_ratios':[3, 3, 4]}) 

axis[0].scatter(angax, Eax, c= 'b') 
axis[1].hist(angax, bins = 15, color= "blue")

axis[0].set_ylabel("Energy (MeV)")
axis[0].set_xlabel("Angle (Rad)")
axis[0].set_title("Energy vs Angle\n" + detector_name)


axis[1].set_xlabel("Angle (Rad)")
axis[1].set_title("Angular Distribution\n" + detector_name)
axis[1].text(meanx, meany, "Mean =" + f"{mean:.4f}")


scater = axis[2].scatter(justx, justy, c = 'b')
scater = axis[2].scatter(missjustx,missjusty, c = 'r')
#scater = axis[2].scatter(justx, justy, c = angax)
#colorbar = plt.(scater, ax = axis[2], orientation='vertical', label='Particle angle')
axis[2].set_aspect('equal', adjustable='box')
axis[2].set_ylabel("Position Y(mm)")
axis[2].set_xlabel("Position X(mm)")
axis[2].set_title("Position on Detector and Board\n"+ detector_name)

print(file_name, "\nHits:", len(justx),"\nMisses:", len(missjustx),"\nTotal", len(justx) + len(missjustx))

plt.savefig(directory + "\\" + file_name + '.png',format='png')
#plt.show()