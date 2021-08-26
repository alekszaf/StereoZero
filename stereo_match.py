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
imgL = cv.imread('C://Temp//Timelapse//Left_Tests_25-08-2021//orange_calib_23cm2021-08-25 23-31-16.563063.jpg', 0)
imgR = cv.imread('C://Temp//Timelapse//Right_Tests_25-08-2021//green_calib_23cm2021-08-25 23-31-16.665927.jpg', 0)

# Rectify the images
imgL = cv.remap(imgL, stereoMapL_x, stereoMapL_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
imgR = cv.remap(imgR, stereoMapR_x, stereoMapR_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
cv.imshow('Left camera - stereo rectified', imgL)
cv.imshow('Right camera - stereo rectified', imgR)
cv.waitKey(0)

stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL, imgR)

plt.imshow(disparity, 'gray')
plt.show()