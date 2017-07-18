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
    #img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cropped_faceR = imgR[y:y+h, x:x+w]
    # roi_gray = gray[y:y+h, x:x+w]
    # roi_color = img[y:y+h, x:x+w]

# CODE LEFT
faces = face_cascade.detectMultiScale(grayL)
for (x,y,w,h) in faces:
    cropped_faceL = imgL[y:y+h, x:x+w]
###########################################################
######## WORKING ##########################################
## cv2.imshow('img', img)                                ##
## cv2.waitKey(0)                                        ##
## cv2.imshow('face', cropped_face)                      ##
## cv2.waitKey(0)                                        ##
##                                                       ##
disparity  =  stereoPiD.dispair(left_file, right_file, min_disp=8, num_disp=128) ##
##                                                       ##
##cv2.imshow('img disparity',disparity)                  ##
##cv2.waitKey(0)                                         ##
##                                                       ##
plt.imshow(disparity, 'gray')                          ##
plt.show()                                             ##
###########################################################
###########################################################

# face_disparity = stereoPiD.dispair(cropped_faceL, cropped_faceR)
# cv2.imshow('face', face_disparity)
# cv2.waitKey(0)

greenDIR = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Green30Calib/'
yellowDIR = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Yellow30Calib/'

#greenMAT, greenImageD = stereoPiD.calibrateCamera(greenDIR)
#yellowMAT, yellowImageD =  stereoPiD.calibrateCamera(yellowDIR)

#stereoPiD.stereoDiffPop(yellowMAT, greenMAT, yellowImageD, greenImageD)

#Q = stereoPiD.calib3D(greenMAT, yellowMAT)


#_3Dobject= cv2.reprojectImageTo3D(disparity, Q, handleMissingValues=True)
# _3Dobject = cv2.reprojectImageTo3D(face_disparity, Q, handleMissingValues=True)



#fig = plt.figure()

#x, y, z = [], [], []
#temp = 0
#for vert in _3Dobject:
#  for horiz in vert[::40]:
#    temp += 1
#    for not filtering out max points
#
#    x.append(horiz[1])
#    y.append(horiz[0])
#    z.append(horiz[2])

    # For cutting out points that are far away
#    if horiz[2] < 6000:
#      x.append(horiz[1])
#      y.append(horiz[0])
##      z.append(horiz[2])
#      temp = 0
#    else:
#      print temp

#for item in range(len(_3Dobject[0])):
#  print _3Dobject[0][item]
#
#ax = fig.add_subplot(111, projection='3d')
#
#ax.scatter(x,y,z, c='r', marker='o')
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')
#
cv2.imshow('disparity', disparity)
#plt.show()
