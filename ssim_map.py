#!/usr/bin/env python3

import cv2
import numpy as np
from scipy import signal

def cal_ssim(img1Path, img2Mtrx): #(img1Path, img2Path):
    
    #Editor Note: Assuming single channel images are read. For RGB image, uncomment color convert lines
    
    #Attempt to pass image matrix 
    img1 = cv2.imread(img1Path,1)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)   #DOES THIS INDEX ONLY LOOK AT GRAY VALUES?
    #img2 = cv2.imread(img2Path,1)                  
    img2 = cv2.cvtColor(img2Mtrx, cv2.COLOR_BGR2GRAY)

    K = [0.01, 0.03]
    L = 255
    kernelX = cv2.getGaussianKernel(11, 1.5)
    window = kernelX * kernelX.T
     
    M,N = np.shape(img1)

    C1 = (K[0]*L)**2
    C2 = (K[1]*L)**2
    img1 = np.float64(img1)
    img2 = np.float64(img2)
 
    mu1 = signal.convolve2d(img1, window, 'valid')
    mu2 = signal.convolve2d(img2, window, 'valid')
    
    mu1_sq = mu1*mu1
    mu2_sq = mu2*mu2
    mu1_mu2 = mu1*mu2
    
    sigma1_sq = signal.convolve2d(img1*img1, window, 'valid') - mu1_sq
    sigma2_sq = signal.convolve2d(img2*img2, window, 'valid') - mu2_sq
    sigma12 = signal.convolve2d(img1*img2, window, 'valid') - mu1_mu2
   
    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))
    mssim = np.mean(ssim_map)
    return mssim,ssim_map

