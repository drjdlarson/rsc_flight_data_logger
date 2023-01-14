#!/usr/bin/env python
# Camera server
# Tuan Luong UA RSC
# 12/26/2021
import time
import datetime
from xmlrpc.server import SimpleXMLRPCServer

file_prefix = '/home/pi/Desktop/nav_dat/'
timestamp_filename = file_prefix + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_cam_timestamp.txt"
gimbal_angle_filename = file_prefix + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_gimbal_angle.txt"
gimbal_calib_filename = file_prefix + datetime.datetime.now().strftime("%Y%m%d_%H") + "gimbal_cal.txt"

try:
    # Begin an xmlrpc server
    with SimpleXMLRPCServer (("169.254.2.166",8000),logRequests=False) as server:
        # Define some functions that the controller calls
        
        # Get camera state (on/off)
        def getCameraState():
            with open('/home/pi/Desktop/nav_software/cam_state.txt', mode='r') as f:
                state = f.readline().rstrip()
                return state == "1"
        
        # Get current GGA string
        def getGPGGAState():
            with open('/home/pi/Desktop/nav_software/gga.txt', mode='r') as f:
                line = f.readline().rstrip()
                return line
            
        # Get current RMC string
        def getGPRMCState():
            with open('/home/pi/Desktop/nav_software/rmc.txt', mode='r') as f:
                line = f.readline().rstrip()
                return line
            
        # Record current timestamp
        def savetime():
            with open(timestamp_filename, mode='a') as f:
                    f.write(str(int(time.time())))
                    f.write('\n')
                    return True
        
        # Get current INS string
        def getVNINS():
            try:
                with open ('/home/pi/Desktop/nav_software/vnins.txt', mode='r') as f:
                    line = f.readline().rstrip()
                    return line
            except:
                return None
            
        # Record gimbal angle    
        def record_gimbal_angles(ant_pitch, ant_roll):
            with open(gimbal_angle_filename, mode='a') as f:
                f.write(str(int(time.time())))
                f.write(",")
                f.write(str(ant_roll))
                f.write(",")
                f.write(str(ant_pitch))
                f.write('\n')
        
        # Record gimbal angles and plane angle on ground to solve plane to gimbal stationary 
        def record_gimbal_base_offset (ant_pitch, ant_roll):
            with open ('/home/pi/Desktop/nav_software/vnins.txt', mode='r') as f:
                line = f.readline().rstrip()
            with open (gimbal_calib_filename, mode='w') as f:
                f.write(line)
                f.write('\n')
                f.write(str(ant_roll))
                f.write(",")
                f.write(str(ant_pitch))
        
        # Register functions above
        server.register_function(getCameraState)
        server.register_function(getGPGGAState)
        server.register_function(getGPRMCState)
        server.register_function(savetime)
        server.register_function(getVNINS)
        server.register_function(record_gimbal_angles)
        server.register_function(record_gimbal_base_offset)
        
        # Run the server forever
        server.serve_forever()
except Exception as e:
    print ('\n')