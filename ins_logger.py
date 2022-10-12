#!/usr/bin/env python
# Log data from serial port
# Tuan Luong UA RSC
# 12/26/2021

# Import libraries
import serial
import datetime
import time
import os

# Define port for VN-200
ins_port = '/dev/ttyUSB0'
ins_baud = 115200

# Function to get header of the VN-200 output string
def get_header(msg):
    return msg[1:6]

# Define output file location and name
file_prefix = '/home/pi/Desktop/nav_dat/'
ins_filename = file_prefix + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_vnins.txt"

# open serial connection to VN-200
with serial.Serial(ins_port,ins_baud, timeout = 5) as ins_ser, open(ins_filename, mode ='a') as outputfile:
    # Clear the input buffer
    ins_ser.reset_input_buffer()
    try:
        while 1:
            time.sleep (0.001) # Set limit on how fast the loop can run
            
            # Check if buffer is not empty
            if ins_ser.inWaiting() > 0:
                ins_buf = ins_ser.readline()     # Read the input buffer until \n character
                ins_string = ins_buf.decode()    # Convert the byte to string (VNINS, GPRMC, GPGGA)
                # Only set to log VNINS messages 
                if get_header(ins_string) == "VNINS":
                    outputfile.write(ins_string)
                    with open('/home/pi/Desktop/nav_software/vnins.txt',mode='w') as f:
                        f.write(ins_string)
                elif get_header(ins_string) == "GPRMC":
                    with open('/home/pi/Desktop/nav_software/rmc.txt',mode='w') as f:
                        f.write(ins_string)
                elif get_header(ins_string) == "GPGGA":
                    with open('/home/pi/Desktop/nav_software/gga.txt',mode='w') as f:
                        f.write(ins_string)
    except:
        ins_ser.close()
