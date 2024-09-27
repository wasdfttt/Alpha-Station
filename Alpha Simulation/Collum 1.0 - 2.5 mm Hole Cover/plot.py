import matplotlib.pyplot as plt
import numpy as np

directory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Collum 0422-0426'
file_name = 'Collum 1.0 - 2.5 mm Radius Hole in Cover'

hits = []
angle = []
percentage = []
offset = []
data = []
total = 9063

def convertData():
    for i in data:
        hits.append(i[0])
        angle.append(i[1])
        percentage.append(i[0]/total)
        offset.append(i[2])

figure, axis = plt.subplots(1, 3, figsize = (16,4))

data.append([9010, .02249, 1.0])
data.append([9038, .02246, 1.5])
data.append([8981, .02240, 2.0])
data.append([8982, .02258, 2.5])

convertData()
axis[0].scatter(offset, hits, s=20)
axis[1].scatter(offset, angle, s=20)
axis[2].scatter(offset, percentage, s=20)

axis[0].set_xlabel('Hole Radius (mm)')
axis[1].set_xlabel('Hole Radius (mm)')
axis[2].set_xlabel('Hole Radius (mm)')

axis[0].set_ylabel('Hits')
axis[1].set_ylabel('Mean Angle (rad)')
axis[2].set_ylabel('Percentage of No Cover')
axis[0].set_ylim([8000, 10000])
axis[1].set_ylim([.022, .023])
axis[2].set_ylim([.95, 1])

axis[0].set_title('Hits vs Hole Radius')
axis[1].set_title('Mean Angle vs Hole Radius')
axis[2].set_title('Percentage vs Hole Radius')
plt.suptitle(file_name)

plt.show()