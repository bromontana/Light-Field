import cameracalib as camcal
import os
import cv2
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

GREENDIR = "Green/"
YELLOWDIR = "Yellow/"
stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=15)

print("\t\t\tGreen Camera Calibration\n")
gDic =  camcal.findImageD(GREENDIR)

print("\n\n\t\t\tYellow Camera Calibration\n")
yDic = camcal.findImageD(YELLOWDIR)


print ("\n\n\n\nGreen Dictionary\n")
print (gDic)
print ("\n=======================================================\nYellow Dictionary\n")
print (yDic)
print("\n\n")



#throw out the pairs of images that couldnt both find the checkerboard (for no real reason)
image_list = camcal.commonWorkingImages(gDic, yDic)
image_list.sort()
print("=========================================================")
print("\t\t\t Image_list\n")
print(image_list)
print("\n\n\n")


# v small thing to comfirm that all the images in image_list exist
#"""
print("----------------------------------------------------------------------------------------")
print("|  GREEN                                |        YELLOW                                 |")
for image in image_list:
    greenimg = os.path.isfile(GREENDIR+image)
    yellowimg = os.path.isfile(YELLOWDIR+image)

    print ("|  Green: "+image+" \t=\t " + str(greenimg) + "\t|\t yellow: "+image+" \t=\t" + str(yellowimg)+"    |")
print("----------------------------------------------------------------------------------------\n\n\n")




gmatrix, gdist_coeff, g_imgS, gobj, gimg, grvec, gtvec = camcal.calibrateCamera(GREENDIR, image_list)
ymatrix, ydist_coeff, y_imgS, yobj, yimg, yrvec, ytvec = camcal.calibrateCamera(YELLOWDIR, image_list)


"""

print("\t\t\tDisparity Maps")

for image in image_list:
    print(YELLOWDIR+image)
    print(GREENDIR+image)
    imgR = cv2.imread(GREENDIR+image, 0)
    imgL = cv2.imread(YELLOWDIR+image, 0)

    stereo = cv2.StereoBM_create(numDisparities=(16*4), blockSize=5)

    disparity=stereo.compute(imgL, imgR)

    plt.imshow(disparity, 'gray')

    plt.show()

"""
RotationMatrix = np.zeros(shape=(2,2))
TranslationMatrix = np.zeros(shape=(2,2))
EssentialMatrix = np.zeros(shape=(3,3))
FundMatrix = np.zeros(shape=(3,3))
gRmat = np.zeros(shape=(3,3))
yRmat = np.zeros(shape=(3,3))
gPmat =np.zeros(shape=(3,4))
yPmat = np.zeros(shape=(3,4))
Q = np.zeros(shape=(4,4))

"""
print("Yellow Image Matrix")
print(yimg)
print("\n\n\nGreen Image Matrix")
print(gimg)
print("\n\n\nYellow Object Matrix")
print(yobj)
print("\n\n\nGreen Object Matrix")
print(gobj)
"""


retval, ymatrix, ydist_coeff, gmatrix, gdist_coeff, RotationMatrix, TranslationMatrix, EssentialMatrix, FundMatrix =  cv2.stereoCalibrate(gimg, yobj, gobj, ymatrix, ydist_coeff, gmatrix, gdist_coeff, g_imgS, RotationMatrix, TranslationMatrix, EssentialMatrix, FundMatrix)

recTransformLeft, recTransformRight, projectionMatLeft, projectionMatRight, Q, ROIleft, ROIright = cv2.stereoRectify (ymatrix, ydist_coeff, gmatrix, gdist_coeff, g_imgS, RotationMatrix, TranslationMatrix, yRmat, gRmat, yPmat, gPmat, Q)

disparity = stereo.compute(cv2.imread(YELLOWDIR+'image00.jpg',0), cv2.imread(GREENDIR+'image00.jpg', 0))
_3Dobject = cv2.reprojectImageTo3D(disparity, Q, handleMissingValues=True)
print len(_3Dobject)

fig = plt.figure()
print _3Dobject.shape
# _3Dobject.tofile('array.out')

# print (_3Dobject == _3Dobject.tolist())
# np.savetxt('array.out', _3Dobject.tolist(), delimiter=' ', fmt='%s')

x, y, z = [], [], []
print _3Dobject[0]
print "\n"
print _3Dobject[1]
print "\n"
print _3Dobject[2]
print "\n"
print _3Dobject[3]
print "\n"
temp = 0
for vert in _3Dobject:
  for horiz in vert[::60]: 
    temp += 1
    if horiz[2] < 10:
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
