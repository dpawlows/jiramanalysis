import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integ
import os
import glob

#def CalculateBrightAnomaly(data): 
    #f
    
def BrightMap(file):
    '''Takes IMG file as input and outputs map of brightness temperature'''
    
    #Read in data
    nrows = 432
    ncols = 128
    dtype = np.dtype('float32')
    f = open(file,'rb') #files are binary
    data_in = np.fromfile(f,dtype=dtype) #data is read in as a single 1D array
    
    #Construct a 2D array for holding the data
    data = np.zeros((ncols,nrows),dtype=dtype)
    
    #Fill 2D array and store negative values as 0.
    counter = 0
    for i in range(ncols):
        for j in range(nrows):
            if data_in[counter] > 0: #this is questionable!
                data[i,j] = data_in[counter]
            else:
                data[i,j] = data[i-1, j]
    
            counter += 1
     
        
    # define necessary constants
    bolt = 1.38e-23 # m^2 kg s^-2 K-1
    c = 3e8 # m/s
    h = 6.626e-34 # m^2 kg s^-1
    
    # wavelength assumed is M band
    lmbda = 4.78e-6 # m
    
    # convert spectral radiance from microns to meters
    data = data*1e6
    
    # calculate needed constants
    coef = (h*c)/(bolt*lmbda)
    logarg = (2*h*(c**2))/(data*(lmbda**5))
    
    # calculate brigtness temperature
    data = coef/np.log(1 + logarg)
    
    return data

def readbin(file):
    '''Read a jiram bin file and output data in a 2d matrix'''

    nrows = 336
    ncols = 256

    dtype = np.dtype('float32')
    f = open(file,'rb')
    data_in = np.fromfile(f,dtype=dtype)

    data = np.zeros((ncols,nrows),dtype=dtype)

    counter = 0
    for i in range(ncols):
        for j in range(nrows):

            data[i,j] = data_in[counter]

            counter += 1

    return data

def PlotSpectrum(specdata):
    '''Reads spectrometer data (output from readbin()) outputs 
    plot of spectrum'''
    
    # determine location of brightest pixel
    # (there is probably a better way with numpy, but it is late and I am tired)
    # index = np.unravel_index(np.argmax(specdata, axis=None), specdata.shape)
    
    maxx = 0
    index = [0, 0]
    for i in range(len(specdata)):
        for j in range(len(specdata[i])):
            if specdata[i][j] > maxx:
                maxx = specdata[i][j]
                index = [i, j]
    
    # give list of corresponding spectral radiance for slice
    # with brightest pixel
    
    spectrum = specdata[index[0]]
    # spectrum = specdata[200]
    
    return spectrum

def DownloadDataset(url):
    '''Takes orbit url and downloads RDR IMG files'''
    
    os.system('wget --no-parent -r -e robots=off -A "JIR_IMG_RDR*IMG" ' + url)
    

def ProcessIMG(directory):
    '''Will process IMG files in given directory'''
    
    # make data folder if it doen't already exist
    os.system("mkdir Data")
    
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



