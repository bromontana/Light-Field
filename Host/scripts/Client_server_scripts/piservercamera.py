import os
import subprocess as subp
import socket




# client_connection will take in the host information
# and return the initialized socket obejct.


def client_connection(host):

    # Separate the 'host' touple, if the touple doesnt work on its own
    # host_IP, host_PORT = host

    # initialize the connection and connect to the client
    client = socket.socket()
    client.connect(host)
    return client


# client_camera is the function for using socket to invoke
# image capture on the server (or raspberry pi) side, and
# it also will return the image, or series of images. It
# takes in the number of images and target directory and
# does that. And it should accept the client connection
# amirite?
#
# targetDirectory should be relative to the present working directory

def client_camera(ClientConnection, numberOfImages, targetDirectory):
    ClientConnection.send('take'+str(numberOfImages))
    if ClientConnection.recv(10) == 'done':
        pass
        # for i in range(1, numberOfImages):
            # this will run the script 'take_server_image.sh which should
            # should be in this directory
        #    subp.call(['./take_server_image.sh', ClientConnection.getpeername()[0], os.getcwd()+targetDirectory])
