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
imgL = cv.imread('C://Temp//Timelapse//NGIF-9-12-21//Left//cropped//0.png', 1)
imgR = cv.imread('C://Temp//Timelapse//NGIF-9-12-21//Right//14h25min36s-26min57s//green_10m_2021-12-08 14-25-36.972421.jpg', 1)

#plt.imshow(imgL)
plt.imshow(imgR)

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

stereo = cv.StereoBM_create(numDisparities=48, blockSize = 11)
#stereo = cv.StereoBM_create(blockSize=4)
#stereo = cv.StereoBM_create(16, 15)
disparity = stereo.compute(grayLeft, grayRight)

#Scale down disparity values and normalize
disparity = disparity.astype(np.float32)
disparity = (disparity/16.0 - minDisparity)/numDisparities


plt.imshow(disparity, 'gray')
plt.show()
