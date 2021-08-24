import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

imgL = cv.imread('C://Temp//Timelapse//Left_Calibration_selfies//orange_calib2021-08-18 22-28-05.208179.jpg', 0)
imgR = cv.imread('C://Temp//Timelapse//Right_Calibration_selfies//green_calib2021-08-18 22-28-05.205202.jpg', 0)

stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL, imgR)

plt.imshow(disparity, 'gray')
plt.show()