import numpy as np

### This software reads a full JIRAM specturm file (JIR_SPE_RDR_...DAT)

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


file = 'data/JIR_SPE_RDR_2016238T205131_V01.DAT'
data = readbin(file)
print(data)
