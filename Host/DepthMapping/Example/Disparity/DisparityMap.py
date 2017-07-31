# This is the very basic "how to make a disparity map" code. 
# It includes the plotting for seeing the disp maps. 


import numpy as np
import cv2
from matplotlib import pyplot as plt

# import images as numpy arrays
imgL = cv2.imread('yellow1.jpg', 0) 
imgR = cv2.imread('green1.jpg', 0) 

# create a stereoimage object 
stereo = cv2.StereoSGBM_create(numDisparities=(16*4), blockSize=5) 

# compute the disp map usng the stereo object and the images 
disparity=stereo.compute(imgL, imgR) 

# plot the disparity map 
plt.imshow(disparity, 'gray') 
plt.show()
