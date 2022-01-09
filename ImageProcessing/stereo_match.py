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

cv.imshow(imgL)
cv.imshow(imgR)

#Load sample images
#imgR = cv.imread('C://Temp//stereo_samples//Yeuna9x.png')
#imgL = cv.imread('C://Temp//stereo_samples//SuXT483.png')

grayLeft = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
grayRight = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

# Rectify the images
grayLeft = cv.remap(grayLeft, stereoMapL_x, stereoMapL_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
grayRight = cv.remap(grayRight, stereoMapR_x, stereoMapR_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
cv.imshow('Left camera - stereo rectified', grayLeft)
cv.imshow('Right camera - stereo rectified', grayRight)
cv.waitKey(0)

minDisparity = 0
numDisparities=64

stereo = cv.StereoBM_create(numDisparities=64, blockSize = 11)
disparity = stereo.compute(grayLeft, grayRight)

#Scale down disparity values and normalize
disparity = disparity.astype(np.float32)
disparity = (disparity/16.0 - minDisparity)/numDisparities

plt.imshow(disparity, 'gray')
plt.show()
