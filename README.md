# Remote Stereo Imaging README

This repository is for the raspberry pi stereo imaging project. 

## Current progress 

So far there are a couple features working: 

 + Images can be taken remotely from each Pi
 + Images can be analyzed to look for the checkerboard for calibration 
 + Depth maps can be built
 + Libraries have been started to make file transfer and remote imaging 
more accessable

If anything looks aweful and out of place please leave an issue. <3

## Goals

This is starting at the time when I have aleady made progress up to 
the 4th bullet noted above. 

 + Make python libraries that enable easy image capture and transfer 
over the network using `rsync` or `socket.send()`. 
 + Make program that will update the disparity map instead of reopening 
new ones. 
 + Make program that will continually update disparity maps in real 
time when called upon. 

## Summmary

The purpose of this program is to (eventually) make better conference 
calls or something to that effect. As the quality of this prototype 
improves it will provide bandwith benchmarks. We will be able to predict 
bandwith requirements as video conferencing moves into the realm of VR 
and AR with the gigabyt bandwith future coming soon (TM). 

## Contents 

 + Host
  + Depth Mapping
   + Basically what you would need to make disparity maps from both 
camera outputs
  + Scripts
   + All of the scripts for automation. Important to check these before 
running them to make sure that the directories are correct.  
 + Raspberry Pi 
  + socket\_testing
   + This is all the stuff that will be constantly running on the server. 
These functions are going to be what lets the pi take commands and execute
them accordingly. 
  + This directory is basically the stuff that goes in the ~/ directory 
of the pi. These are all associated with taking images and sending them 
over since all of the image processing should be done on the host machine
for time reasons. 



