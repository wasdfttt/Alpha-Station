import matplotlib.pyplot as plt
import numpy as np

directory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Collum 10 - 20 mm'
file_name = 'Collum .5 mm Radius 10 - 20 mm Length'

hits = []
length = []
angle = []
data = []

def convertData():
    for i in data:
        hits.append(i[0])
        angle.append(i[1])
        length.append(i[2])

figure, axis = plt.subplots(1, 2, figsize = (16,4))

data.append([9969, .02235, 10])
data.append([9880, .02229, 12])
data.append([9658, .02246, 14])
data.append([9308, .02252, 16])
data.append([8958, .02240, 18])
data.append([8177, .02184, 20])

convertData()
axis[0].scatter(length, hits, s=20)
axis[1].scatter(length, angle, s=20)


axis[0].set_xlabel('Collimator Length (mm)')
axis[1].set_xlabel('Collimator Length (mm)')

axis[0].set_ylabel('Hits')
axis[1].set_ylabel('Mean Angle (rad)')
axis[0].set_ylim([7500, 10500])
axis[1].set_ylim([.020, .025])

axis[0].set_title('Hits vs Length')
axis[1].set_title('Mean Angle vs Length')
plt.suptitle(file_name)

plt.show()