import cv2
import numpy as np
import glob



# Calibration image parameters
chessboardSize = (9, 6)
frameSize = (720, 480)

# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

objp = pbjp * 30
print(objp)

# Store object points and image points
objpoints = []
imgpointsL = []
imgpointsR = []

# Load the images
imgLeft = glob.glob('C:/Temp/Timelapse/Left_cam_calibration/*.jpg')
imgRight = glob.glob('C:/Temp/Timelapse/Right_cam_calibration/*.jpg')