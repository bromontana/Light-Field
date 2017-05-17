#!/bin/bash

 
parallel-ssh -A -h host_file.txt "python close_picam.py" 
