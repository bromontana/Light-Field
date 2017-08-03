#!/bin/bash

sshpass -p 'raspberry' scp pi@$1:~/socket_testing/temp/image0.jpg ./$2
