import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

angles = [0, 15, 22, 30, 37, 45]
#W14_200VMeans = [1.32478, 1.27760, 1.56997, 1.47850, 1.37083, 1.27879]
W14_200VMeans = [1.32915, 1.28001, 1.57317, 1.48135, 1.37367, 1.28147]
#W14_200Vrms = [0.12283, 0.11951, 0.12738, 0.13011, 0.11983, 0.10608]
W14_200Vrms = [0.12282, 0.11956, 0.12733, 0.13005, 0.11985, 0.10619]
#W14_300VMeans = [1.41070, 1.34717, 1.61753, 1.53607, 1.39654, 1.29349]
W14_300VMeans = [1.41308, 1.34939, 1.62005, 1.53858, 1.39966, 1.29691]
#W14_300Vrms = [0.16115, 0.15262, 0.16351, 0.16957, 0.15270, 0.13640]
W14_300Vrms = [0.16125, 0.15279, 0.16367, 0.16979, 0.15284, 0.13649]
W11_300VMeans = [2.60389, 2.65042, 2.65671, 2.62634, 2.52939, 2.53668]
W11_300Vrms = [0.24491, 0.22940, 0.23451, 0.23097, 0.24796, 0.25437]
W11_300VMeans2 = [2.15327, 2.19175, 2.19695, 2.17193, 2.09167, 2.09769] #W14 Pin 250V
W11_300Vrms2 = [0.23723, 0.22759, 0.23128, 0.22804, 0.23758, 0.24235]
W11_400VMeans = [2.15124, 2.20668, 2.21193, 2.18730, 2.11023, 2.14238]
W11_400Vrms = [0.23970, 0.23038, 0.23699, 0.23424, 0.25038, 0.26612]

colours = cm.rainbow(np.linspace(0,1,4))
plt.errorbar(angles, W11_300VMeans, W11_300Vrms, capsize = 5, capthick = 1.5, color = colours[0], label = '300V (Pin 150V)', marker = 'o')
plt.errorbar(angles, W11_300VMeans2, W11_300Vrms2, capsize = 5, capthick = 1.5, color = colours[1], label = '300V (Pin 250V)', marker = 'o')
plt.errorbar(angles, W11_400VMeans, W11_400Vrms, capsize = 5, capthick = 1.5, color = colours[2], label = '400V (Pin 250V)', marker = 'o')
plt.axis([-5, 50, 1.5, 3])
plt.xlabel('Angle (deg)')
plt.ylabel('Gain')
plt.title('W11 Gain as Function of Angle')
plt.legend(loc = 'lower left', fontsize = 12)
plt.show()