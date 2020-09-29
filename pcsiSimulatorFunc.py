#!/usr/bin/env python3
# Author: Scott Howard KD9PDP
# License: GPL-3.0
# Adapted from
# http://www.pyrunner.com/weblog/2016/05/26/compressed-sensing-python/

import os
import numpy as np
import argparse
import imageio
import cv2
from pcsi.colorconv import numPixelsSent
from pcsi.pcsiolw import PCSIolw

def pcsiSimulator(imagefile, transmittedColorDepth, numberPackets, chromaCompressionList, bitsAvailable, outfolder, saveOutputFiles):  

    # Setting parameters 
    bitDepthToRemove = int((24-transmittedColorDepth)/3)  # per channel

    # read original image
    Xorig = imageio.imread(imagefile)

    # Modify imagefile for saving/writing
    imagefilePath, ext = imagefile.split('.')
    imagefileName = imagefilePath.split('/')[-1]

    # Create outfolder if desired
    if saveOutputFiles and not os.path.exists(outfolder):
        os.makedirs(outfolder)

    #Howard Changed this to cv2
    #Xorig = rgb2ycbcr(Xorig) 
    Xorig = cv2.cvtColor(Xorig, cv2.COLOR_BGR2YCrCb) #RGB = BGR
    ny,nx,nchan = Xorig.shape

    for chromaCompression in chromaCompressionList:
        # sampleSizes are the number of YCbCr and Y only pixels received in n packets
        print(numberPackets,
                                     transmittedColorDepth,
                                     chromaCompression, bitsAvailable)
        sampleSizes = [numPixelsSent(n,
                                     transmittedColorDepth,
                                     chromaCompression,
                                     bitsAvailable) for n in numberPackets]
        
        # for each sample size
        Z = [np.zeros(Xorig.shape, dtype='uint8') for s in sampleSizes]
        masks = [np.zeros(Xorig.shape, dtype='uint8') for s in sampleSizes]

        #Calling each set of parameters one a time makes this loop below not neccesary

        for i,s in enumerate(sampleSizes):

            # create random sampling index vector
            k = sum(s)
            #Requested more Pixels than in the image: NEED TO CONVERT TO PERCENTS AND DO AWAY WITH THIS
            if(k > nx * ny):    
                print("asked for more pixels than there are present")
                return (np.zeros(5), False)
                #raise ValueError(f"Request more pixels than in the image: {(nx*ny)} pixels in image: {k} requested") 
            ritotal = np.random.choice(nx * ny, k, replace=False) # random sample of indices

            # for each color channel
            for j in range(nchan):

                if(j==0):  # take more pixels for Y channel
                    ri = ritotal
                else:  # enable sampling fewer pixels for chroma
                    ri = ritotal[:s[0]]

                # extract channel
                X = Xorig[:,:,j].squeeze()

                # simulate color depth transmitted
                X = np.around(
                        np.around(X /(2**8-1) * (2**(transmittedColorDepth/3)-1))
                        / (2**(transmittedColorDepth/3)-1) * (2**8-1))
                X[X>255] = 255
                # X = (X>>bitDepthToRemove)<<bitDepthToRemove
                # X = np.around(X / ((2**8)-1) * ((2**(transmittedColorDepth/3))-1))

                # create images of mask (for visualization)
                Xm = 255 * np.ones(X.shape)
                Xm.T.flat[ri] = X.T.flat[ri]
                masks[i][:,:,j] = Xm

                # take random samples of image, store them in a vector b
                b = X.T.flat[ri].astype(float)

                # perform the L1 minimization in memory
                pcsiSolver = PCSIolw(nx, ny, b, ri)
                Z[i][:,:,j] = pcsiSolver.go().astype('uint8')

            #Z[i][:,:,:] = ycbcr2rgb(Z[i][:,:,:])  
            Z[i][:,:,:] = cv2.cvtColor(Z[i][:,:,:], cv2.COLOR_YCrCb2BGR)
            #print(Z[i][:,:,:])

            #Have to figure out what this is ^ so I can return the proper thing for my SSIM calculator
            
            #If you want to save
            if saveOutputFiles:
                imageio.imwrite(outfolder + '/' + imagefileName + str(numberPackets[i]) +'p_'
                            + str(transmittedColorDepth) + 'b_'
                            + str(chromaCompression) +'.bmp', Z[i])

            #If the program was called functionally
            if __name__!= "__main__": 
                return ((Z[i][:,:,:]), True)

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Command line tool to simulate PCSI",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imagefile", type=str, default='OriginalImages/HAB2sstv.bmp',
                        help="Input image to transmit (24bit color, any filetype)")
    parser.add_argument("-b", "--bitdepth", type=int, default=12,
                        help="Bit depth transmit (e.g., 24 for 24-bit color)")
    parser.add_argument("-N", "--numpackets", type=int, nargs='*', default=[150],
                        help="Number of packets to simulate")
    parser.add_argument("-c", "--chromacomp", type=int, default=[20], nargs='*',
                        help="Chroma Compression ratio")
    parser.add_argument("-a", "--bitsAvailable", type=int, default=1992,
                        help="Number of bits available in payload for image data")
    parser.add_argument("-o", "--outfolder", type=str, default="results",
                        help="Output folder name")
    args = parser.parse_args()

    #Main execution
    
    pcsiSimulator(args.imagefile, args.bitdepth, args.numpackets, args.chromacomp, args.bitsAvailable, args.outfolder, True)
    
    

