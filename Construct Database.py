import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integ
import os
import glob
import pandas as pd
import re

def DownloadDataset(url):
    '''Takes orbit url and downloads RDR IMG and LBL files'''
    
    # download IMG ad LBL files in directory
    os.system('wget --no-parent -r -e robots=off -A "JIR_IMG_RDR*[^xml]" ' + url)
    
    # make specific directory and move data there
    os.system('mkdir Data')
    filepath = url.replace('/' , '\\')
    os.system('move {}'.format(filepath[8:]) + '*' + ' Data')
    # os.sys('rmdir /S atmos.nmsu.edu')
    
    
def ProcessIMG(directory):
    '''Will process IMG files in given directory'''
    
    # make data folder if it doen't already exist
    os.system("mkdir Images")
    
    folder = glob.glob(directory + "/*IMG")

    for file in folder:
        print("Working on {}".format(file))
        nrows = 432
        ncols = 128
        dtype = np.dtype('float32')
        f = open(file,'rb') #files are binary
        data_in = np.fromfile(f,dtype=dtype) #data is read in as a single 1D array
        
        #Construct a 2D array for holding the data
        data = np.zeros((ncols,nrows),dtype=dtype)
        
        counter = 0
        for i in range(ncols):
            for j in range(nrows):
                if data_in[counter] >= 0: #this is questionable!
                    data[i,j] = data_in[counter]
        
                counter += 1
                
    myimg = plt.imshow(data)
       
    cb = plt.colorbar(myimg,label='Radiance ($W/m^2/sr/\mu m$)')
    plt.savefig("Images/" + file[5:-4] + '.png')
    plt.close()
    
def ProcessData(directory):
    '''Takes directory of LBL files and will process them into csv of useful data'''
    
    # define useful parameters we want to save
    usefulparam = ["STOP_TIME", "MINIMUM_LATITUDE", "MAXIMUM_LATITUDE",
                   "WESTERNMOST_LONGITUDE", "EASTERNMOST_LONGITUDE",
                   "HORIZONTAL_PIXEL_SCALE", "VERTICAL_PIXEL_SCALE"]
    
    # make file to save data to
    outfile = open("InstrumentInfo.csv", 'w')
    
    label = 'IMG Number'
    for i in usefulparam:
        label += ',' + i
        
    print(label, file=outfile)
    
    # for each LBL file save useful data
    folder = glob.glob(directory + "/*LBL")
    
    for file in folder:
        print("Processesing File", file)
        imgparam = ['']*len(usefulparam) # list of parameters for given image
        
        # you actually need to open the file apparently
        infile = open(file, 'r')
        
        for line in infile:
            data = line.replace(' ', '').replace('\n', '').split('=')
            
            # see if matches any paramaters, place in matching spot
            for j in range(len(usefulparam)):
                if data[0] == usefulparam[j]:
                    imgparam[j] = data[1]
                    break
         
        # produce string for outfile
        outstr = str(file)[-30:-4]
        for i in imgparam:
            outstr += ',' + re.sub("[^0-9\.\-\:]", '', str(i)) # only numbers, dots, dashes, or colins
            
        print(outstr, file=outfile)
        
        infile.close()
        
    outfile.close()
    
def Search(conditions, filename="InstrumentInfo.csv"):
    # conditions go as [paramater name, minumum, maximum]
    '''Input what paramater you are limiting, returns images that
    satisfy those conditions'''
    
    data = pd.read_csv(filename)
    
    for i in conditions:
        index_names = data[(data[i[0]] < i[1]) | (data[i[0]] > i[2])].index
        data.drop(index_names, inplace = True)
        data = data.dropna(subset=[i[0]])
        
    
    print(data['IMG Number'])
    
            
        
# ProcessData("Data")
Search([['MINIMUM_LATITUDE', -40, -39], 
        ['MAXIMUM_LATITUDE', 9, 10]])

