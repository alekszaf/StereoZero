import cv2
import numpy as np
import glob



# Calibration image parameters
chessboardSize = (9, 6)
frameSize = (720, 480)

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

objp = objp * 30
print(objp)

# Store object points and image points
objpoints = []
imgpointsL = []
imgpointsR = []

# Load the images
imagesLeft = glob.glob('C:/Temp/Timelapse/Left_cam_calibration/*.jpg')
imagesRight = glob.glob('C:/Temp/Timelapse/Right_cam_calibration/*.jpg')

for imgLeft, imgRight in zip(imagesLeft, imagesRight):
    imgL = cv2.imread(imgLeft)
    imgR = cv2.imread(imgRight)
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersL = cv2.findChessboardCorners(grayL, chessboardSize, None)
    retR, cornersR = cv2.findChessboardCorners(grayR, chessboardSize, None)

    if retL and retR == True:
        objpoints.append(objp)

        cornersL = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        imgpointsL.append(cornersL)

        cornersR = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        imgpointsR.append(cornersR)

        #Draw and display corners
        cv2.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv2.imshow('img left', imgL)
        cv2.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv2.imshow('img right', imgR)
        cv2.waitKey(1000)

cv2.destroyAllWindows()  

### CALIBRATION ###

# Left camera
retL, cameraMatrixL, distL, rotationL, translationL = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

# Right camera
retR, cameraMatrixR, distR, rotationR, translationR = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))
