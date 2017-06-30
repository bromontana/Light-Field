import os
import numpy
import picamera
from time import sleep

camera = picamera.PiCamera()


sleep(2)


for i in range (0,31):
	
	# temp = '"About to cap ' + str(i) + '"'
	# echo = "'echo "+ temp + "'"
	# os.system(echo)
	os.system('echo "3"')
	sleep (1)
	os.system('echo "2"')
	sleep (1)
        os.system('echo "1"' )
	sleep (1)
        os.system('echo "0"')
	
	if i < 10:
	    imagecap = camera.capture("~/imgs/image0"+str(i)+".jpg")
	else:
	    imagecap = camera.capture("~/imgs/image"+str(i)+".jpg")

	os.system('echo "**Click**"')



camera.close()

