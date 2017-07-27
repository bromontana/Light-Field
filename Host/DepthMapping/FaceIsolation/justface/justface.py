import cv2
import numpy as np
import stereoPiD
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

# CASCADE

face_cascade = cv2.CascadeClassifier('/home/pinheadqt/Tools/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('/home/pinheadqt/Tools/opencv/data/haarcascades/haarcascade_eye.xml')


# IMAGE INIT
right_file = '../../../../../../Pictures/GreenImgs/image17.jpg'
left_file = '../../../../../../Pictures/YellowImgs/image17.jpg'

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

plt.imshow(cropped_faceR)
plt.show()
plt.imshow(cropped_faceL)
plt.show()
# For the whole image
disparity  =  stereoPiD.dispair(left_file, right_file, min_disp=(8), num_disp=(64)) ##

print(cropped_faceR.shape)
### TEST ###
faces = face_cascade.detectMultiScale(grayR)
for (x,y,w,h) in faces:
    disparity_crop = disparity[y:y+h, x:x+w]


disparity2 = stereoPiD.dispair(cropped_faceL, cropped_faceR, num_disp=32)
plt.imshow(disparity_crop, 'gray')
plt.show()

plt.imshow(disparity2, 'gray')
plt.show()

# takes camera calibration values from CameraCalibration/Arrays/ which should only need to be found once per camera and stored
# greenMAT = pickle.load(open('/home/pinheadqt/Documents/RemoteStereoImaging/Host/DepthMapping/CameraCalibration/Arrays/greenMat.p','rb'))
# yellowMAT = pickle.load(open('/home/pinheadqt/Documents/RemoteStereoImaging/Host/DepthMapping/CameraCalibration/Arrays/yellowMat.p','rb'))
Q = pickle.load(open('/home/pinheadqt/Documents/RemoteStereoImaging/Host/DepthMapping/CameraCalibration/Arrays/Q.p','rb'))

_3Dobject= cv2.reprojectImageTo3D(disparity, Q, handleMissingValues=True)
# _3Dobject = cv2.reprojectImageTo3D(face_disparity, Q, handleMissingValues=True)



fig = plt.figure()

x, y, z = [], [], []
temp = 0
for vert in _3Dobject:
  for horiz in vert[::15]:
    temp += 1
#    for not filtering out max points
#
#    x.append(horiz[1])
#    y.append(horiz[0])
#    z.append(horiz[2])

    # For cutting out points that are far away
    if horiz[2] < 6000:
      x.append(horiz[1])
      y.append(horiz[0])
      z.append(horiz[2])
      temp = 0
    else:
      print temp

for item in range(len(_3Dobject[0])):
  print _3Dobject[0][item]

ax = fig.add_subplot(111, projection='3d')

ax.scatter(x,y,z, c='r', marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

cv2.imshow('disparity', disparity)
plt.show()
