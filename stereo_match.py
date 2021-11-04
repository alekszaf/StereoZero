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
#imgL = cv.imread('C://Temp//Timelapse//15-09-21//Second_depth_test-15-09-21o//orange_test_10cm2021-09-15 21-35-59.407296.jpg', 0)
#imgR = cv.imread('C://Temp//Timelapse//15-09-21//Second_depth_test-15-09-21g//green_test_10cm2021-09-15 21-35-59.403614.jpg', 0)
imgR = cv.imread('C://Temp//stereo_samples//Yeuna9x.png')
imgL = cv.imread('C://Temp//stereo_samples//SuXT483.png')

# Rectify the images
#imgL = cv.remap(imgL, stereoMapL_x, stereoMapL_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
#imgR = cv.remap(imgR, stereoMapR_x, stereoMapR_y, cv.INTER_LINEAR, cv.BORDER_CONSTANT, 0)
cv.imshow('Left camera - stereo rectified', imgL)
cv.imshow('Right camera - stereo rectified', imgR)
cv.waitKey(0)

grayLeft = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
grayRight = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

stereo = cv.StereoBM_create(numDisparities=16, blockSize = 5)
#stereo = cv.StereoBM_create(blockSize=4)
#stereo = cv.StereoBM_create(16, 15)
disparity = stereo.compute(grayLeft, grayRight)

plt.imshow(disparity, 'gray')
plt.show()