import matplotlib.pyplot as plt
import numpy as np

directory = 'c:\\Users\\chris\\OneDrive\\Desktop\\Alphasim\\Collum 0422-0426'
file_name = 'Collum 0.0mm-1.0mm Offset'

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

data.append([9063, .02243, 0])
data.append([8098, .02249, .2])
data.append([7001, .02277, .4])
data.append([5424, .02378, .6])
data.append([3859, .02611, .8])
data.append([2265, .03041, 1])

convertData()
axis[0].scatter(offset, hits, s=20)
axis[1].scatter(offset, angle, s=20)
axis[2].scatter(offset, percentage, s=20)

axis[0].set_xlabel('Offset (mm)')
axis[1].set_xlabel('Offset (mm)')
axis[2].set_xlabel('Offset (mm)')

axis[0].set_ylabel('Hits')
axis[1].set_ylabel('Mean Angle (rad)')
axis[2].set_ylabel('Percentage of 0mm')

axis[0].set_title('Hits vs Offset')
axis[1].set_title('Mean Angle vs Offset')
axis[2].set_title('Percentage vs Offset')

plt.show()