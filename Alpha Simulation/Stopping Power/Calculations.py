"""
This code is used to calculate the theoretical stopping distance using the ASTAR table of stopping powers with respect to various materials
"""

#Table units = MeV cm^2/g

initialE = 5.486

silverSTable = 353.5 #4.5 MeV
silverDensity = 10.5
silverS = silverSTable * silverDensity

goldSTable = 223.4 #5.5 MeV
goldDensity = 19.32
goldS = goldSTable * goldDensity

siliconSTable = 687.75 #4.25 MeV
siliconDensity = 2.33
siliconS = siliconSTable * siliconDensity

airSTable = 852.5 #4.25 MeV at sea level
airDensity = .0001205 #sea level/10
airS = airSTable * airDensity

silverS/=10 #Converting to MeV/mm
goldS/=10
siliconS/=10
airS/=10

silverLength = .000 #.001
goldLength = .001 #.002
airLength = 30

dESilver = silverS * silverLength
dEGold = goldS * goldLength
dEAir = airS * airLength

finalE = initialE - dESilver - dEGold
finalEAir = finalE - dEAir

siliconDepth = finalE / siliconS
siliconDepthAir = finalEAir / siliconS
print(f'{finalE:=4f}\n{siliconDepth:=4f}\n{finalEAir:.=4f}\n{siliconDepthAir:=.4f}')