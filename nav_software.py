#!/usr/bin/env python
# Main navigation script
# Tuan Luong UA RSC
# 12/26/2021

# Import libraries
import datetime
import time
import os
import subprocess

# Run sync_time.py and wait for completion
print ("Running time_sync subroutine")
#time_sync_res = subprocess.run("sudo python3 /home/pi/Desktop/sync_time.py", shell = True, capture_output = True, text = True)
#print (time_sync_res.stdout)

# Start processes
try:
    # UBX logger for PPK
    ubx_proc = subprocess.Popen("sudo python3 /home/pi/Desktop/nav_software/ubx_logger.py", shell = True)
    # Vectornav logger
    ins_proc = subprocess.Popen("sudo python3 /home/pi/Desktop/nav_software/ins_logger.py", shell = True, text = True)
    print ("Loggers started")
    # Switch handling process
    cam_proc = subprocess.Popen("python3 /home/pi/Desktop/nav_software/switch_handler.py", shell = True, stdout = subprocess.PIPE)
    # Begin communication with camera controller and gimbal controller via server
    server = subprocess.Popen("python3 /home/pi/Desktop/nav_software/server.py", shell = True)
    print ("Server started")
    
    # Constantly print the current GGA string just for check that things are still running
    while 1:
        time.sleep(0.5)
        with open ('/home/pi/Desktop/nav_software/gga.txt', mode='r') as f:
            print (f.readline())
       
except Exception as e:
    print ("Killing all processes")
    subprocess.run("sudo pkill python", shell = True)

