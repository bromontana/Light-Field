#!/bin/bash

sshpass -p 'raspberry' scp pi@$1:~/home/pi/imgs/image0.jpg ./$2
