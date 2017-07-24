import numpy as np
import cv2
import stereoPiD
import pickle
greenDIR = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Green30Calib/'
yellowDIR = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Yellow30Calib/'

# find intrinsic variables for both cameras 
greenMAT, greenImageD = stereoPiD.calibrateCamera(greenDIR)

yellowMAT, yellowImageD = stereoPiD.calibrateCamera(yellowDIR)

#  camcal returns: (camera_matrix, dist_coefs, (w,h), img_points, obj_points, rvecs, tvecs), imageD

# removes images that do nothing
stereoPiD.stereoDiffPop(yellowMAT, greenMAT, yellowImageD, greenImageD)


OutFile = '/home/pinheadqt/Documents/StereoImages/CameraCalibration/Arrays/'

pickle.dump(greenMAT, open('greenMat.p','wb'))
pickle.dump(yellowMAT, open('yellowMat.p', 'wb'))
