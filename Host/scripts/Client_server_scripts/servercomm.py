import piservercamera as piserve
import os
from matplotlib import pyplot as plt
import cv2
import subprocess


green_dir = '/home/pinheadqt/Pictures/PiImages/Green/'
yellow_dir = '/home/pinheadqt/Pictures/PiImages/Yellow/'
plt.axis([0,1920,1080,0])
plt.ion()
plt.show()
green_client = piserve.client_connection(('greenPi.local',4000))
green_adress = green_client.getpeername()[0]
yellow_client = piserve.client_connection(('yellowPi.local',4000))
yellow_adress = yellow_client.getpeername()[0]


window_size = 3
min_disp = 16
num_disp = 32-min_disp

stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 15,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32
)

while True:
# Make the Commands
  print("about to request pictures from greenPi")
  piserve.client_camera(green_client, 1, green_dir)
# Accept Green response
  print("about to print response")
#  green_client.recv(4)
  print ("ignoring response")

# Yellow command
  print("about to request pictures from yellowPi")
  piserve.client_camera(yellow_client, 1, yellow_dir)
# Accept Yellow response
  #print(yellow_client.recv(24))


# Accept the response
# green_client.recv(10)
# yellow_client.recv(10)

#   THIS PART NEEDS TO PSSH FROM:
#   greenPi:~/home/socket_testing/temp/image*.jpg
  print(green_adress)
  print(yellow_adress)

  subprocess.call(['./green_take.sh',green_adress,green_dir])
  subprocess.call(['./yellow_take.sh',yellow_adress,yellow_dir])
#   yellowPi:~/socket_testing/temp/image*.jpg
  for filename in os.listdir(green_dir):
     imgR = cv2.cvtColor(cv2.imread(green_dir+filename), cv2.COLOR_RGB2GRAY)
     imgL = cv2.cvtColor(cv2.imread(yellow_dir+filename),cv2.COLOR_RGB2GRAY)
     
     #stereo = cv2.StereoBM_create(numDisparities=16,blockSize=15)
     disparity = stereo.compute(imgL, imgR)
     plt.imshow(disparity, 'gray')
     plt.pause(1)

