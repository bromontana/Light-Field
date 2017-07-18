import cameracalib as camcal
import os
import cv2
from matplotlib import pyplot as plt
GREENDIR = "../../Images_from_pssh/Green/imgs/"
YELLOWDIR = "../../Images_from_pssh/Yellow/imgs/"
#calibrate the cameras and aquire all intrinsic and extrinsic variables

print("\t\t\tGreen Camera Calibration\n")
gmatrix, gdist_coeff, g_imgS, gobj, gimg, gDic = camcal.calibrateCamera(GREENDIR)
print("\n\n\t\t\tYellow Camera Calibration\n")
ymatrix, ydist_coeff, y_imgS, yobj, yimg, yDic = camcal.calibrateCamera(YELLOWDIR)

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
print("-----------------------------------------------------------------")
print("|  GREEN                            |  YELLOW                    ")
for image in image_list:
    greenimg = os.path.isfile(GREENDIR+image)
    yellowimg = os.path.isfile(YELLOWDIR+image)

    print ("|  Green: "+image+" \t=\t " + str(greenimg) + "\t|\t yellow: "+image+" \t=\t" + str(yellowimg)+"    |")


print("-----------------------------------------------------------------\n\n\n")
#"""

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


