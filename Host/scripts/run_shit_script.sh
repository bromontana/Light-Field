#1/bin/bash


parallel-ssh -A -h host_file.txt -i -t 10000 ./shit_script.sh 


scp -r pi@greenPi.local:~/imgs/ ~/Documents/StereoImages/Images_from_pssh/Green/
scp -r pi@yellowPi.local:~/imgs/ ~/Documents/StereoImages/Images_from_pssh/Yellow/


