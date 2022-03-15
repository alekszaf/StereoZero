import numpy as np 
import cv2

cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

# Stereo rectification values
stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()
cv_file.release()

#Callback function
def nothing(x):
    pass

cv2.namedWindow('disp', cv2.WINDOW_NORMAL)

cv2.createTrackbar('numDisparities', 'disp', 1, 17, nothing)
cv2.createTrackbar('blockSize','disp', 5, 50, nothing)
#cv2.createTrackbar('preFilterSize', 'disp', 2, 25, nothing)
#cv2.createTrackbar('preFilterCap', 'disp', 5, 62, nothing)
#cv2.createTrackbar('textureThreshold', 'disp', 10, 100, nothing)
cv2.createTrackbar('uniquenessRatio', 'disp', 15, 100, nothing)
cv2.createTrackbar('speckleRange', 'disp', 0, 100, nothing)
cv2.createTrackbar('speckleWindowSize', 'disp', 3, 25, nothing)
cv2.createTrackbar('disp12MaxDiff', 'disp', 5, 25, nothing)
cv2.createTrackbar('minDisparity', 'disp', 5, 25, nothing)

stereo = cv2.StereoSGBM_create()
#stereo = cv2.StereoBM_create()

while True:
    
    #Load the images
    imgL = cv2.imread('C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Camera timelapses\\Zweibrucken_15-01-2022\\Left\\left_2022-01-15 15-20-32.888713.png', 1)
    imgR = cv2.imread('C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Camera timelapses\\Zweibrucken_15-01-2022\\Right\\right_2022-01-15 15-20-32.183367.png', 1)

    imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
    
    imgL_gray = cv2.remap(imgL_gray, stereoMapL_x, stereoMapL_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)
    imgR_gray = cv2.remap(imgR_gray, stereoMapR_x, stereoMapR_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)

    
    numDisparities = cv2.getTrackbarPos('numDisparities', 'disp') * 16
    blockSize = cv2.getTrackbarPos('blockSize', 'disp') * 2 + 5
    #preFilterSize = cv2.getTrackbarPos('preFilterSize', 'disp') * 2 + 5
    #preFilterCap = cv2.getTrackbarPos('preFilterCap', 'disp')
    #textureThreshold = cv2.getTrackbarPos('textureThreshold', 'disp')
    uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio', 'disp')
    speckleRange = cv2.getTrackbarPos('speckleRange', 'disp')
    speckleWindowSize = cv2.getTrackbarPos('speckleWindowSIze', 'disp') * 2
    disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff', 'min')
    minDisparity = cv2.getTrackbarPos('minDisparity', 'min')
    
    stereo.setNumDisparities(numDisparities)
    stereo.setBlockSize(blockSize)
    #stereo.setPreFilterSize(preFilterSize)
    #stereo.setPreFilterCap(preFilterCap)
    #stereo.setTextureThreshold(textureThreshold)
    stereo.setUniquenessRatio(uniquenessRatio)
    stereo.setSpeckleRange(speckleRange)
    stereo.setSpeckleWindowSize(speckleWindowSize)
    stereo.setDisp12MaxDiff(disp12MaxDiff)
    stereo.setMinDisparity(minDisparity)
    
    disparity = stereo.compute(imgL_gray, imgR_gray)
    
    disparity = disparity.astype(np.float32)
    
    disparity = (disparity/16.0 - minDisparity)/numDisparities
    
    cv2.imshow('disp', disparity)
    
    if cv2.waitKey(1) == 27:
        break