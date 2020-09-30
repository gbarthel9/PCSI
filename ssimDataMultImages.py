#!/usr/bin/env python3

from ssim_map import cal_ssim
import argparse
from pcsiSimulatorFunc import pcsiSimulator
from ssimDataProgFunc import ssimDataProg
import numpy as np
from scipy.optimize import minimize
import scipy.io
import csv
import os


def main():
    parser = argparse.ArgumentParser(description="Command line tool creating matrix of output data for PCSI parameter tests", 
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imageDir", type=str, default='OriginalImages',
                        help="Input image directory to run ssim tests on (24bit color, any filetype)")
    parser.add_argument("-b", "--bitdepthrange", type=int, default=[21,21,3], nargs='*',
                        help="Bit depth range to test and iteration step; should be mult of 3 (enter 9 24 3 for 9,12,...24)")
    parser.add_argument("-N", "--numpacketsrange", type=int, nargs='*', default=[100,100,100],
                        help="Range of packet quantity to test and iteration step ")
    parser.add_argument("-c", "--chromacomprange", type=int, default=[20, 20, 4], nargs='*',
                        help="Chroma Compression ratio range to test and iteration step")
    parser.add_argument("-a", "--bitsAvailable", type=int, default=1992,
                        help="Number of bits available in payload for image data")
    parser.add_argument("-s", "--saveOutputImages", type=int, default=0,
                        help="1 to save output images, 0 to not save")
    args = parser.parse_args()
    
    for filename in os.listdir(args.imageDir):
        imgPath = os.path.join(args.imageDir, filename) #automatically adds a '/' because it is an os function (expects that)
        #print(imgPath)
        ssimDataProg(imgPath, args.chromacomprange, args.bitdepthrange, args.numpacketsrange, args.bitsAvailable, args.saveOutputImages)


if __name__ == "__main__":
    main()

