import numpy as np
import cv2
from matplotlib import pyplot as plt
#import matplotlib
imgL = cv2.imread('Yellow/image00.jpg', 0) 
imgR = cv2.imread('Green/image00.jpg', 0) 


stereo = cv2.StereoBM_create(numDisparities=(16), blockSize=15)

disparity=stereo.compute(imgL, imgR) 

plt.imshow(disparity, 'gray') 
plt.show()
