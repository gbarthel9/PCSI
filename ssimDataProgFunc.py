#!/usr/bin/env python3

from ssim_map import cal_ssim
import argparse
from pcsiSimulatorFunc import pcsiSimulator
import numpy as np
from scipy.optimize import minimize
import scipy.io
import csv

def costFunc(imgOrig, cc, b, numP, ba, outfolder, saveImages): #Where imgOrig, ba, outfolder, and saveImages are parameters not variables
    # Returns array of image data 
    img2 = pcsiSimulator(imgOrig, cc, b, numP, ba, outfolder, saveImages) 
    if img2[1] is False:
        return 0
    else:
        ssimVal = (cal_ssim(imgOrig, img2[0])[0]) #Want the first thing in the list that is returned
        return ssimVal

def ssimDataProg(imagefile, chromacomprange, bitdepthrange, numpacketsrange, bitsAvailable):

    #MAKING THIS PROGRAM FUNCTINOAL TO BE CALLED FROM ANOTHER PROGRAM CYCLING THROUGH IMAGES
    #HAVE TO CHANGE FROM ARGS TO PARAMETERS PASSED TO THE FUNCTION


    #NOTE: Range operates on integers only
    bdr = np.array(range(bitdepthrange[0], bitdepthrange[1]+1, bitdepthrange[2]))
    npr = np.array(range(numpacketsrange[0], numpacketsrange[1]+1, numpacketsrange[2]))
    ccr = np.array(range(chromacomprange[0], chromacomprange[1]+1, chromacomprange[2]))
    
    ssimDataMtrx = np.zeros((len(bdr), len(npr), len(ccr))) #Pythonic len() works with 1st dimension of numpy arrays
    #print(ssimDataMtrx)
    #Might want to use map in the future so it can be more concurrent for parallelizaiton
    for i, b in enumerate(bdr):
        for j, numP in enumerate(npr):
            for k, cc in enumerate(ccr):
                ssimDataMtrx[i][j][k] = costFunc(imagefile, b, [numP],[cc], bitsAvailable, "results_NA", False)
    print(ssimDataMtrx)    
    
    #Matlab file output:
    matLabDic = {"bd": bdr,
                 "np": npr,
                 "cc": ccr,
                 "ssimData": ssimDataMtrx}
    imgName = (imagefile.split('/')[-1]).split('.')[0]#imagefile is the full path, imgName is just name, no path, no extensions#imagefile is the full path, imgName is just name, no path, no extensions
    scipy.io.savemat('ssimResults/ssimData' + imgName + '.mat', matLabDic)
    

    """OUTPUT TEXT FILE
    with open("ssimData.csv", 'w') as csvfile:
        csvfile.write(f'Bit Depth Values: {bdr}\n')
        csvfile.write(f'NumPackets Values: {npr}\n')
        csvfile.write(f'CC Values: {ccr}\n')
        csvfile.write('SSIM Data:\n')
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerows(ssimDataMtrx)
    """
if __name__ == "__main__":

    #Read the command line for
    #	The image being used
    #	The parameter ranges being testrd
    #	The iteration in those ranges (could also do this explicitly with an array)
    parser = argparse.ArgumentParser(description="Command line tool creating matrix of output data for PCSI parameter tests", 
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imagefile", type=str, default='OriginalImages/HAB2sstv.bmp',
                        help="Input image to transmit (24bit color, any filetype)")
    parser.add_argument("-b", "--bitdepthrange", type=int, default=[21,21,3], nargs='*',
                        help="Bit depth range to test and iteration step; should be mult of 3 (enter 9 24 3 for 9,12,...24)")
    parser.add_argument("-N", "--numpacketsrange", type=int, nargs='*', default=[100,100,100],
                        help="Range of packet quantity to test and iteration step ")
    parser.add_argument("-c", "--chromacomprange", type=int, default=[20, 20, 4], nargs='*',
                        help="Chroma Compression ratio range to test and iteration step")
    parser.add_argument("-a", "--bitsAvailable", type=int, default=1992,
                        help="Number of bits available in payload for image data")
    args = parser.parse_args()

    ssimDataProg(args.imagefile, args.chromacomprange, args.bitdepthrange, args.numpacketsrange, args.bitsAvailable)

    
