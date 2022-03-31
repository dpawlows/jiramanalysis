import numpy as np
from matplotlib import pyplot as pp
from PIL import Image

### This software processes a JIRAM image file taken from either the M-band
# or the L-band. IMG file should be 432 x 128 pixels consisting of a
# binary 32 bit (4 byte) float.

#Note some of the RDR IMG files may contain both L and M bands. This
#will need modification to handle such files.

file = 'data/JIR_IMG_RDR_2017032T194927_V02.IMG'

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
        if data_in[counter] >= 0: #this is questionable!
            data[i,j] = data_in[counter]

        counter += 1

#create and image from the data and save it
myimg = pp.imshow(data)
cb = pp.colorbar(myimg,label='Radiance ($W/m^2/sr/\mu m$)')
pp.savefig('plot.png')
