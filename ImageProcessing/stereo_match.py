import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

cv_file = cv.FileStorage()
cv_file.open('stereoMap.xml', cv.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

#Load the images
imgL = cv.imread('C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Camera timelapses\\Zweibrucken_09-01-2022\\Left\\4m\\left_2022-01-09 15-24-05.838816.png', 1)
imgR = cv.imread('C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Camera timelapses\\Zweibrucken_09-01-2022\\Right\\4m\\right_2022-01-09 15-24-05.839931.png', 1)

cv.imshow('Left', imgL)
cv.imshow('Right', imgR)
cv.waitKey(0)

#Load sample images
#imgR = cv.imread('C://Temp//stereo_samples//Yeuna9x.png')
#imgL = cv.imread('C://Temp//stereo_samples//SuXT483.png')

grayLeft = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
grayRight = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

# Rectify the images
#grayLeft = cv.remap(grayLeft, stereoMapL_x, stereoMapL_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
#grayRight = cv.remap(grayRight, stereoMapR_x, stereoMapR_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
#cv.imshow('Left camera - stereo rectified', grayLeft)
#cv.imshow('Right camera - stereo rectified', grayRight)
#cv.waitKey(0)

#Calculate the disparity map
minDisp = 0
numDisp = 64

#StereoSGBM
stereo = cv.StereoSGBM_create(minDisparity = minDisp,
 numDisparities = numDisp,
 blockSize = 15,
 uniquenessRatio = 5,
 speckleWindowSize = 5,
 speckleRange = 5,
 disp12MaxDiff = 1)

#StereoBM
#stereo = cv.StereoBM_create(numDisparities=numDisp, blockSize = 11)

disparity = stereo.compute(imgL, imgR)

#Scale down disparity values and normalize
#disparity = disparity.astype(np.float32)
#disparity = (disparity/16.0 - minDisp)/numDisp

plt.imshow(disparity, 'gray')
plt.show()
