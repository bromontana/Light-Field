import os
import subprocess as subp
import socket
from time import sleep
import picamera

# server_connetion initializes the server socket and 
# makes it listen for the client. 

# host should be the host_IP and host_PORT that the 
# client is going to use to connect to and returns the
# connection object

def server_connection(host):
    server = socket.socket()

    server.bind(host)

    server.listen(1)
    connection = server.accept()[0]

    return connection



# this will make the server recieve commands from the client
# socket, and have it capture n number of images.

def waitForCommand(ConnectionObj, debugging=False):
    while True:
        evocation = ConnectionObj.recv(15)
        if debugging == True:
            print evocation
        if evocation[:4] == 'take': 
            if debugging == True: 
                print ('about to take '+evocation[4:]+' pictures')
            # This initializes the camera and gives it time to get going
            with picamera.PiCamera() as camera:
                sleep(2)
                # captures all the images in the ./temp/ directory
                for i in range(0,int(evocation[4:])):
                    camera.capture('/home/pi/img/'+str(i)+'.jpg')
                    if debugging == True: 
                        print("Captured image "+str(i))
                if debugging == True: 
                    print('Images took')
            print("Sending 'done'")
            ConnectionObj.send('done')
            if debugging == True:
                print("sent 'done'\n\n------------------------------")
            break
        else: 
            ConnectionObj.send('failed')
            break
