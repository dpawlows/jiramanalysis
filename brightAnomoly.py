# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 17:51:09 2022

@author: willi
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import Functions

#get list of files from the local "data" directory
files = os.listdir('Data')

#iterate through each file in the data directory 
for file in files: 
    #read in the brightness temperature
    bright_temp_data = Functions.BrightMap('Data/' + file) 
    
    #calculate I and I0 values for each pixel 
    I0 = np.max(bright_temp_data)
    I = bright_temp_data
    av = np.average(np.log(I0/I)) #calculate the average of the entire image
    tau = np.log(I0/I) - av #calculate the brightness anomaly of each pixel
    
    #make a plot of the brightness anomoly map and save it to the local "Images" folder
    img = plt.imshow(tau)
    cb = plt.colorbar(img,label='Tau (Brightness Anomaly)')
    plt.savefig("Images/" + file + '.png')
    plt.close()