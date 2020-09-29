#!/usr/bin/env python3

# This program is an optimization routine to find the optimal parameter values
# that can be used to send an image through our pcsiSimulator (compressed sensing).
# Status: Unfinished

from ssim_map import cal_ssim
import pcsiSimulatorFunc
import argparse
import numpy as np
from scipy.optimize import minimize

def costFunc(imgOrig, cc, b, np, ba, outfolder, saveImages): #Where imgOrig is a parameter and parameters are the nummbers to be optimized

   #Note bit value has to go by threes and they all have to be integers

   #Call the pcsiSimulator and get img2 based on parameters. Do I have to iterate through parameters or will the opt function. Either way would it be in here?
   
   #img2 = pcsiSimulator(imgOrig, cc, b, np, ba, outfolder, saveImages) :

   #costFunc = 1 - (cal_ssim(imgOrig, img2)[0]) #want the first thing in the list that is returned
    pass
    return 0

def main():
    #Read the command line for
    #	The image being used
    #	The parameter ranges being testrd
    #	The iteration in those ranges (could also do this explicitly with an array)
    parser = argparse.ArgumentParser(description="Command line tool for optimizing parameters of PCSI", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imagefile", type=str, default='HAB2sstv.bmp',
                        help="Input image to transmit (24bit color, any filetype)")
    parser.add_argument("-b", "--bitdepthrange", type=int, default=[12,24,3], nargs='*',
                        help="Bit depth range to test and iteration step; should be mult of 3 (enter 9 24 3 for 9,12,...24)")
    parser.add_argument("-N", "--numpacketsrange", type=int, nargs='*', default=[100,400,100],
                        help="Range of packet quantity to test and iteration step ")
    parser.add_argument("-c", "--chromacomprange", type=int, default=[16, 24, 4], nargs='*',
                        help="Chroma Compression ratio range to test and iteration step")
    parser.add_argument("-a", "--bitsAvailable", type=int, default=1992,
                        help="Number of bits available in payload for image data")
    args = parser.parse_args()
    
    #Constrained Optimization: In python you can pass functions so likely you will pass the function to minimize
    #Initial Values for Optimization:

    #b0 = np.mean(bitdepthrange[0], bitdephtrange[1])
    #cc0 = np.mean(chromacomprange[0], chromacomprange[1])
    #np0 = np.mean(numpacketsrange[0], numpacketsrange[1])
    #x0 = [cc0, b0, np0]

    #PROBLEM: could make other parameters that don't need to be optimized global or I could find a way
    #to pass them like parameters in Matlab

    #answer = minimize(costFunc,x0, method='', options={})

    #Print the result
    #print(answer)
    
    #Test:
    s10, s11 = cal_ssim("HAB2sstv.bmp", "HAB2sstv.bmp")
    s20, s21 = cal_ssim("HAB2sstv.bmp", "results_HAB2sstv/HAB2sstv150p_12b_20.bmp")
    print(f"s10 is: {s10}")
    #print(f"s11 is: {s11}")
    print(f"s20 is: {s20}")
    #print(f"s21 is: {s21}")


if __name__ == "__main__":
    main()
