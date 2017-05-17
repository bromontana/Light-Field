import numpy
import picamera
from time import sleep

camera = picamera.PiCamera()

print("firing up the ole photon cannon, usually takes 5 seconds exactly always.")
sleep(5)

imagecap = camera.capture("image.jpg")

camera.close()
