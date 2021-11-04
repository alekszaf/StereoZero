import cv2
import numpy as np
import glob

############## DETECT CHESSBOARD PATTERN ##############

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
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY) # Convert to grayscale
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

############## SINGLE-CAMERA CALIBRATION ##############

# Left camera
retL, cameraMatrixL, distL, rotationL, translationL = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

print("Camera matrix L: \n")
print(cameraMatrixL)
print("Distortion L: \n")
print(distL)
print("Rotation vector L: \n")
print(rotationL)
print("Translation vector L: \n")
print(translationL)

# Right camera
retR, cameraMatrixR, distR, rotationR, translationR = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

print("Camera matrix R: \n0")
print(cameraMatrixL)
print("Distortion R: \n")
print(distR)
print("Rotation vector R: \n")
print(rotationR)
print("Translation vector R: \n")
print(translationR)


## Undistortion (single camera)
for imgLeft, imgRight in zip(imagesLeft, imagesRight):
    imgL = cv2.imread(imgLeft)
    imgR = cv2.imread(imgRight)
    dstL = cv2.undistort(imgL, cameraMatrixL, distL, None, newCameraMatrixL)
    dstR = cv2.undistort(imgR, cameraMatrixR, distR, None, newCameraMatrixR)
    xL, yL, wL, hL = roi_L    
    xR, yR, wR, hR = roi_R
    dstL = dstL[yL:yL+hL, xL:xL+wL]
    dstR = dstR[yR:yR+hR, xR:xR+wR]
    cv2.imshow('undistorted left', dstL)
    cv2.imshow('distorted left', imgL)
    cv2.imshow('undistorted right', dstR)
    cv2.imshow('distorted right', imgR)
    cv2.waitKey(0)

# Reprojection error

mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rotationL[i], translationL[i], cameraMatrixL, distL)
    error = cv2.norm(imgpointsL[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print('total error: {}'.format(mean_error/len(objpoints)))

############## STEREO CALIBRATION ##############
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC # keep the intrinsic parameters fixed

criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# essentialMatrix, fundamentalMatrix - how do we relate one camera to the other
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)

############## STEREO RECTIFICATION ################
"""Compute the rotation matrices for each camera
to make both camera image planes the same plane (virtually).
This makes all the epipolar lines parallel and thus simplifies
the dense stereo corespondence problem"""

rectifyScale = 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv2.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale, (0,0))

stereoMapL = cv2.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv2.CV_16SC2)
stereoMapR = cv2.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv2.CV_16SC2)

# Save the parameters

cv_file = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_WRITE)

cv_file.write('stereoMapL_x', stereoMapL[0])
cv_file.write('stereoMapL_y', stereoMapL[1])
cv_file.write('stereoMapR_x', stereoMapR[0])
cv_file.write('stereoMapR_y', stereoMapR[1])

cv_file.release()