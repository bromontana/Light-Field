import cv2
import numpy as np
import stereoPiD
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# CASCADE

face_cascade = cv2.CascadeClassifier('/home/pinheadqt/Tools/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('/home/pinheadqt/Tools/opencv/data/haarcascades/haarcascade_eye.xml')


# IMAGE INIT
right_file = '/home/pinheadqt/Pictures/GreenImgs/image17.jpg'
left_file = '/home/pinheadqt/Pictures/YellowImgs/image17.jpg'

imgL = cv2.imread(left_file)
imgR = cv2.imread(right_file)

# IMAGE => GRAY
grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)


# CODE RIGHT
faces = face_cascade.detectMultiScale(grayR)
for (x,y,w,h) in faces:
    cropped_faceR = imgR[y:y+h, x:x+w]

faces = face_cascade.detectMultiScale(grayL)
for (x,y,w,h) in faces:
    cropped_faceL = imgL[y:y+h, x:x+w]


disparity  =  stereoPiD.dispair(left_file, right_file, min_disp=(16*4), num_disp=(128-16*4))

plt.imshow(disparity, 'gray')
plt.show()

greenDIR = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Green30Calib/'
yellowDIR = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Yellow30Calib/'

cv2.imshow('disparity', disparity)
