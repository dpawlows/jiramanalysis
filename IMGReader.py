import numpy as np
import matplotlib.pyplot as plt

# files to import
files = ['JIR_IMG_RDR_2017033T114006_V02.IMG',
         'JIR_IMG_RDR_2017033T114036_V02.IMG',
         'JIR_IMG_RDR_2017033T114107_V02.IMG',
         'JIR_IMG_RDR_2017033T114137_V02.IMG',
         'JIR_IMG_RDR_2017033T114208_V02.IMG',
         'JIR_IMG_RDR_2017033T114238_V02.IMG',
         'JIR_IMG_RDR_2017033T114309_V02.IMG',
         'JIR_IMG_RDR_2017033T114339_V02.IMG',
         'JIR_IMG_RDR_2017033T114410_V02.IMG',
         'JIR_IMG_RDR_2017033T114440_V02.IMG',
         'JIR_IMG_RDR_2017033T114511_V02.IMG',
         'JIR_IMG_RDR_2017033T114541_V02.IMG']


# shape of images
shape = (128,432)

for i in files:
    
    # determine dtype based on if EDR or RDR
    if i[-26] == 'R':
        dtype = np.dtype(np.int32)
    else:
        dtype = np.dtype(np.int16)
    
    # produce image array
    fid = open(i, 'rb')
    data = np.fromfile(fid, dtype)
    image = data.reshape(shape)
    
    # ugly code to determine bounds (vmin=.9e9, vmax=1.04e9 works fine)
    mx = 0
    mn = 1e9
    
    for j in range(len(image)):
        for k in range(len(image[j])):
            if image[j][k] > mx:
                mx = image[j][k]
            if 0 < image[j][k] < mn:
                mn = image[j][k]
                
    # plot image
    plt.figure()
    plt.imshow(image, cmap='gray', vmin=mn, vmax=mx)
    plt.show()
    