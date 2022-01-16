import cv2
import numpy as np 
import glob
import PIL.ExifTags
import PIL.Image
from matplotlib import pyplot as plt 

#=========================================================
# Stereo Calibration and rectification
#=========================================================
# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

Q = cv_file.getNode('q').mat()

imgL = cv2.imread('C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Camera timelapses\\Zweibrucken_09-01-2022\\Left\\4m\\left_2022-01-09 15-24-05.838816.png')
imgR = cv2.imread('C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Camera timelapses\\Zweibrucken_09-01-2022\\Right\\4m\\right_2022-01-09 15-24-05.839931.png')

# Show the frames
cv2.imshow("frame right", imgR) 
cv2.imshow("frame left", imgL)

cv2.waitKey(0)


# Undistort and rectify images
imgR = cv2.remap(imgR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
imgL = cv2.remap(imgL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                
# Show the frames
cv2.imshow("frame right undistorted", imgR) 
cv2.imshow("frame left undistorted", imgL)
cv2.waitKey(0)

imgLgray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgRgray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

#=========================================================
# Create Disparity map from Stereo Vision
#=========================================================

# For each pixel algorithm will find the best disparity from 0
# Larger block size implies smoother, though less accurate disparity map

# Set disparity parameters
# Note: disparity range is tuned according to specific parameters obtained through trial and error. 
block_size = 11
min_disp = 0
max_disp = 64
num_disp = max_disp - min_disp # Needs to be divisible by 16

# Create Block matching object. 
#stereo = cv2.StereoSGBM_create(minDisparity= min_disp,
#	numDisparities = num_disp,
#	blockSize = block_size,
#	uniquenessRatio = 5,
#	speckleWindowSize = 5,
#	speckleRange = 2,
#	disp12MaxDiff = 2,
#	P1 = 8 * 3 * block_size**2, #8*img_channels*block_size**2,
#	P2 = 32 * 3 * block_size**2)  #32*img_channels*block_size**2)


stereo = cv2.StereoBM_create(numDisparities = num_disp, blockSize = block_size)

# Compute disparity map
disparity_map = stereo.compute(imgLgray, imgRgray)

# Show disparity map before generating 3D cloud to verify that point cloud will be usable. 
plt.imshow(disparity_map,'gray')
plt.show()


#=========================================================
# Generate Point Cloud from Disparity Map
#=========================================================

# Get new downsampled width and height 
h,w = imgR.shape[:2]

# Convert disparity map to float32 and divide by 16 as show in the documentation
print(disparity_map.dtype)
disparity_map = np.float32(np.divide(disparity_map, 16.0))
print(disparity_map.dtype)

# Reproject points into 3D
points_3D = cv2.reprojectImageTo3D(disparity_map, Q, handleMissingValues=False)

# Get color of the reprojected points
colors = cv2.cvtColor(imgR, cv2.COLOR_BGR2RGB)

# Get rid of points with value 0 (no depth)
mask_map = disparity_map > disparity_map.min()

# Mask colors and points. 
output_points = points_3D[mask_map]
output_colors = colors[mask_map]

# Function to create point cloud file
def create_point_cloud_file(vertices, colors, filename):
	colors = colors.reshape(-1,3)
	vertices = np.hstack([vertices.reshape(-1,3),colors])

	ply_header = '''ply
		format ascii 1.0
		element vertex %(vert_num)d
		property float x
		property float y
		property float z
		property uchar red
		property uchar green
		property uchar blue
		end_header
		'''
	with open(filename, 'w') as f:
		f.write(ply_header %dict(vert_num=len(vertices)))
		np.savetxt(f,vertices,'%f %f %f %d %d %d')


output_file = 'pointCloud.ply'

# Generate point cloud file
create_point_cloud_file(output_points, output_colors, output_file)