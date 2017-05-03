import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

## collecting data

data_GL = pd.read_excel('Greenland_temp.xlsx', header = 14)
data_ANT = pd.read_excel('Antartic_temp.xlsx', header = 10)

data_GL.columns = ['Age','Temp']
data_ANT.columns = ['Age','Temp']
Age_GL = data_GL['Age']
Age_ANT = data_ANT['Age']

Temp_GL = data_GL['Temp']
Temp_ANT = data_ANT['Temp']


## modifying data
mod_age_GL = []
mod_age_ANT = []
for i in range(0,len(Age_GL)):
    num = (Age_GL[i] +  abs(Age_GL[0]))*1000
    mod_age_GL.append(num)
for i in range (0,len(Age_ANT)):
    num2 = (Age_ANT[i] + abs(Age_ANT[0])) *1000
    mod_age_ANT.append(num2)
## Temperature data of Antartica is given intemperature relative to the mean
## temperature in 1950, leading to a modification of average surface temperature
## today

con_fact = -45 - Temp_ANT[0]


mod_ANT_temp =[]
for i in range (0,len(Temp_ANT)):
    num3 = Temp_ANT[i] + con_fact
    mod_ANT_temp.append(num3)

    
mod_age_ANT2 =[]
for i in range(0,1609):
    mod_age_ANT2.append(mod_age_ANT[i])
mod_ANT_temp2 = []
for i in range(0,1609):
    mod_ANT_temp2.append(mod_ANT_temp[i]) 
              

fig1 = plt.figure()
plot1 = fig1.add_subplot(5,1,1)
plot1.plot(mod_age_GL,Temp_GL)
plt.gca().invert_xaxis()

plot2 = fig1.add_subplot(5,1,3)
plot2.plot(mod_age_ANT,mod_ANT_temp)
plt.gca().invert_xaxis()

plot3 = fig1.add_subplot(5,1,5)
plot3.plot(mod_age_ANT2,mod_ANT_temp2)
plt.gca().invert_xaxis()

plt.show()

