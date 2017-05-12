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
mod_age_GL = mod_age_GL[::-1]
for i in range (0,len(Age_ANT)):
    num2 = (Age_ANT[i] + abs(Age_ANT[0])) *1000
    mod_age_ANT.append(num2)
## Temperature data of Antartica is given intemperature relative to the mean
## temperature in 1950, leading to a modification of average surface temperature
## today

con_fact = -45 - Temp_ANT[0]

## modify data to better suit future needs
mod_GL_temp = []
for i in range (0,len(Temp_GL)):
    num4 = Temp_GL[i]
    mod_GL_temp.append(num4)
mod_GL_temp = mod_GL_temp[::-1]
    
mod_ANT_temp =[]
for i in range (0,len(Temp_ANT)):
    num3 = Temp_ANT[i] + con_fact
    mod_ANT_temp.append(num3)
    
## make Antarctica the same time frame as Greenland 
mod_age_ANT2 =[]
for i in range(0,1609):
    mod_age_ANT2.append(mod_age_ANT[i])
mod_age_ANT2 = mod_age_ANT2[::-1]
    
mod_ANT_temp2 = []
for i in range(0,1609):
    mod_ANT_temp2.append(mod_ANT_temp[i]) 
mod_ANT_temp2 = mod_ANT_temp2[::-1]              


## plotting of figures
fig2 = plt.figure()
plot1 = fig2.add_subplot(3,1,1)
plot1.plot(mod_age_GL,mod_GL_temp)
plt.gca().invert_xaxis()
plt.xlabel('Time Before Present (years)')
plt.ylabel('Temperature (Celcius)')
plt.title('Greenland')


plot3 = fig2.add_subplot(3,1,3)
plot3.plot(mod_age_ANT2,mod_ANT_temp2)
plt.gca().invert_xaxis()
plt.xlabel('Time Before Present (years)')
plt.ylabel('Temperature (Celcius)')
plt.title('Antarctica')

plt.show()
fig2 = plt.figure()


## creating class for ice sheet to simplify calculations
class Icesheet:
    def __init__(self, thickness, surface_temp):
        self.thickness = thickness * 10
        self.temp = surface_temp

    def depth_profile(self):
        z_range = (self.thickness / 25) 
        z = 25. * np.arange(z_range)
        return z

    def temp_profile(self):
        z_range = (self.thickness / 25) 
        T = 0.5 * np.arange(z_range)
        for i in range(0,len(T)):
            T[i] = T[i] + self.temp
        return T
## Set initial temperature for profile
ANT_init = mod_ANT_temp2[0]
GL_init = mod_GL_temp[0]

## Profile data for icesheets
Greenland = Icesheet(1200, GL_init)
Antartica = Icesheet(2000, ANT_init)

GL_prof = Greenland.depth_profile()
ANT_prof = Antartica.depth_profile()

GL_t_prof = Greenland.temp_profile()
ANT_t_prof = Antartica.temp_profile()

## set up initial profile 
plt.plot(ANT_t_prof, ANT_prof)

## set up base profile for Greenland
GL_T2 = []
for i in range(0,len(GL_t_prof)):
            sum9 = GL_t_prof[i]
            GL_T2.append(sum9)

## Set temperature funciton to simplify future
def T_profile(z,temp,time,temp_time):
    
## variables   
    dt = (86400 *36.5)
    k = 2.24
    rho = 917
    Cp = 210.8
    rho_Cp = rho*Cp
    
## set up time intervals for each
    dti = -1 * np.diff(time)
    dTa = []
    for y in range(1,len(temp_time)):
        num5 = temp_time[y]
        dTa.append(num5)
        
## begin the plot
        
    for i in range(0,len(dti)):
        
        for h in range(0,int((dti[i])*10)):
            temp[0] = dTa[i]
            
            dT = np.diff(temp)
            dz = np.diff(z)

            q = -k * dT/dz
            
            z_inner = np.cumsum(dz)
            dz_inner = np.diff(z_inner)

            dT_dt = -1/(rho_Cp) * np.diff(q) / dz_inner
            
            temp[1:-1] = temp[1:-1] + (dT_dt * dt)
   
    return temp
    
## Run T_profile for the two datasets
Greenland2 = T_profile(GL_prof,GL_t_prof,mod_age_GL,mod_GL_temp)
Antartica2 = T_profile(ANT_prof,ANT_t_prof,mod_age_ANT2,mod_ANT_temp2)

    

## Plotting Antartica
plt.plot(Antartica2,ANT_prof,'r')

plt.ylim([0,2000])
plt.xlim([-60,0])
plt.gca().invert_yaxis()
plt.xlabel('Temperature(Celcius)')
plt.ylabel('Meters Below Ice Surface')
plt.title('Antarctica Profile, Past & Present')
plt.show()

##Plotting Greenland
fig3 = plt.figure()
plt.plot(Greenland2, GL_prof)
plt.plot(GL_T2, GL_prof)
plt.ylim([0,1200])
plt.xlim([-60,0])
plt.gca().invert_yaxis()
plt.xlabel('Temperature (Celcius)')
plt.ylabel('Meters Below Ice Surface')
plt.title ('Greenland Profile, Past & Present')

plt.show()
