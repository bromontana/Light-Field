    #!/usr/bin/env python

from __future__ import print_function
import numpy as np
import cv2

# from common import splitfn

import os
import sys

import getopt

from matplotlib import pyplot as plt

from glob import glob
# import itertools as it
# from contextlib import contextmanager


def splitfn(fn):
    path, fn = os.path.split(fn)
    name, ext = os.path.splitext(fn)
    return path, name, ext

def calibrateCamera(DIR):
    args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size='])
    args = dict(args)
    args.setdefault('--debug', './output/')
    args.setdefault('--square_size', 1.0)
    if not img_mask:
        img_mask =str(DIR + 'image*.jpg')  # default
    else:
        img_mask = img_mask[0]
    #new_img_names = []
    img_names = glob(img_mask)
    #for item in imageList:
    #    new_img_names.append(item)
    debug_dir = args.get('--debug')
    if not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)
    square_size = float(args.get('--square_size'))

    pattern_size = (9, 6)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    imageD = []

    h, w = 0, 0
    img_names_undistort = []
    for fn in img_names:
        print('processing %s... ' % fn, end='')
        img = cv2.imread(fn, 0)
        if img is None:
            print("Failed to load  ", fn)
            continue

        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            imageD.append(fn.rsplit('/')[len(fn.split('/'))-1])
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if debug_dir:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        if not found:
            print('chessboard not found')
            continue

        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print('ok')

    print(len(obj_points))
    print(len(img_points))
    # calculate camera distortion
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)


    cv2.destroyAllWindows()
    return (camera_matrix, dist_coefs, (w,h), img_points, obj_points, rvecs, tvecs), imageD




def dispair(left, right, min_disp=16, num_disp=48):
    #imgR = cv2.imread('friday_delet/Yellow/image25.jpg', 0)
    imgL = cv2.imread(left,0)
    #imgR = cv2.imread('friday_delet/Green/image25.jpg', 0)
    imgR = cv2.imread(right,0)

    window_size=3
    # stereo = cv2.StereoBM_create(numDisparities=(16*3), blockSize=25)
    stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 10,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32
        )

    disparity=stereo.compute(imgL, imgR)
    # print disparity.shape
    # plt.imshow(disparity, 'gray')
    # plt.show()
    return disparity

# def commonWorkingImages(dict1, dict2):
#
#     if dict1 > dict2:
#         bigger_dic = dict1
#     else:
#         bigger_dic = dict2
#
#     equal_dics = []
#     for image in iter(bigger_dic):
#         if dict1[image] and  dict2[image] == True:
#             print(image)
#             equal_dics.append(image)
#     # print(image + "\t\t" + str(gDic[image] )+ "\t | \t" + str(yDic[image]))
#     return equal_dics

def stereoDiffPop(leftMat, rightMat, leftImageD, rightImageD):
# Compare the lists and
    if len(leftImageD) != len(rightImageD):
        for item in leftImageD:
            if item in rightImageD:
                continue
            else:
                # remove extra item from img_points and then obj_points
                del(leftMat[3][leftImageD.index(item)])
                del(leftMat[4][leftImageD.index(item)])
                leftImageD.remove(item)
        for item in rightImageD:
            if item in leftImageD:
                continue
            else:
                # remove extra item from img_points and then obj_points
                del(rightMat[3][rightImageD.index(item)])
                del(rightMat[4][rightImageD.index(item)])
                rightImageD.remove(item)
        print(len(rightImageD))
        print(len(leftImageD))

def cropDisparity(left, right, disp):
    # get matrix from left img
    found, corners = cv2.findChessboardcorners(left, (9,6))
    # find corners
    for point in corners:
      if point[0][1] > bigY: # or point[0][0] > bigY:
        bigY, bigX = int(point[0][0]), int(point[0][1])

      if point[0][1] < lilY: # or point [0][0] < lilY:
        lilY, lilX = int(point[0][0]), int(point[0][1])
    deltX, deltY = bigX - lilX, bigY - lilY
    cropped_disp = disp[lilX:lilX+deltX, lilY:lilY+deltY]
    # pick longer dist btwn corners

    return cropped_disp

def calib3D(greenCalibTuple, yellowCalibTuple):

    # Green Calibration
    gmatrix, gdist_coeff, g_imgS, gobj, gimg, grvec, gtvec = greenCalibTuple

    ymatrix, ydist_coeff, y_imgS, yobj, yimg, yrvec, ytvec = yellowCalibTuple

    RotationMatrix = np.zeros(shape=(2,2))
    TranslationMatrix = np.zeros(shape=(2,2))
    EssentialMatrix = np.zeros(shape=(3,3))
    FundMatrix = np.zeros(shape=(3,3))
    gRmat = np.zeros(shape=(3,3))
    yRmat = np.zeros(shape=(3,3))
    gPmat =np.zeros(shape=(3,4))
    yPmat = np.zeros(shape=(3,4))
    Q = np.zeros(shape=(4,4))

    #stereoCalibrate to prepare the program to use the stereovision functions
    retval, ymatrix, ydist_coeff, gmatrix, gdist_coeff, RotationMatrix, TranslationMatrix, EssentialMatrix, FundMatrix =  cv2.stereoCalibrate(gimg, yobj, gobj, ymatrix, ydist_coeff, gmatrix, gdist_coeff, g_imgS, RotationMatrix, TranslationMatrix, EssentialMatrix, FundMatrix)

    #stereoRectify for finding the physical (relative) position of cameras
    recTransformLeft, recTransformRight, projectionMatLeft, projectionMatRight, Q, ROIleft, ROIright = cv2.stereoRectify (ymatrix, ydist_coeff, gmatrix, gdist_coeff, g_imgS, RotationMatrix, TranslationMatrix, yRmat, gRmat, yPmat, gPmat, Q)

    return Q
