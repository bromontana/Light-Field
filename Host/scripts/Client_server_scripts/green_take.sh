#!/bin/bash

sshpass -p 'raspberry' scp pi@$1:~/home/socket_testing/temp/image0.jpg ./$2
