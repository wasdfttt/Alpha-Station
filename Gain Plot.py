import numpy as np
import matplotlib.pyplot as plt

angles = [0, 15, 22, 30, 37, 45]
W14_200VMeans = [1.32478, 1.27760, 1.56997, 1.47850, 1.37083, 1.27879]
W14_200Vrms = [0.06364, 0.06137, 0.07542, 0.07102, 0.06585, 0.06143]
W14_300VMeans = [1.41070, 1.34717, 1.61753, 1.53607, 1.39654, 1.29349]
W14_300Vrms = [0.10556, 0.10080, 0.12103, 0.11494, 0.10450, 0.09679]

plt.errorbar(angles, W14_200VMeans, W14_200Vrms, capsize = 5, capthick = 1.5, color = 'r', label = '200V')
plt.errorbar(angles, W14_300VMeans, W14_300Vrms, capsize = 5, capthick = 1.5, color = 'g', label = '300V')
plt.axis([-5, 50, 1, 2])
plt.xlabel('Angle (deg)')
plt.ylabel('Gain')
plt.title('W14 Gain as Function of Angle')
plt.legend(loc = 'upper left', fontsize = 12)
plt.show()