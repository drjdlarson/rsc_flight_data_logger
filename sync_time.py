#!/usr/bin/env python
# Sync system time to current GPS time
# Tuan Luong UA RSC
# 12/26/2021

# Import libraries
import serial
import datetime
import time
import os

#  Define port to VN-200
ins_port = '/dev/ttyUSB0'
ins_baud = 115200

# Init some flags
time_init = False
fix_stat = False

# Calculate UNIX time given GPS time
def calc_posix_time (gps_tow,gps_week):
    cur_leap = 18
    return round(float(gps_tow),1) + int(gps_week) * 604800 + 315964800 - cur_leap

# Check if the current UNIX time is rounded whole second. Just help with accuracy
def check_rounded_time (cur_posix_time):
    return cur_posix_time % 1 == 0

# Return header of message
def get_header (msg):
    return msg[1:6]

# Calculate checksum of the line
def calc_checksum(msg):
    cksum = 0
    for i in msg:
        cksum ^= ord(i)
    s = '{:02X}'.format(cksum)
    return s

# Validate the msg using 8-bit crc checksum. Return true if valid
def validate_msg (msg):
    split_msg = msg.split('*')
    ex_cksum = split_msg[1]
    line_to_check = split_msg[0]
    line_to_check = line_to_check[1:]
    cksum = calc_checksum(line_to_check)
    return cksum.strip() == ex_cksum.strip()

# Check if the gps fix is valid so that GPS time report is accurate using RMC 
def check_valid_fix (msg):
    split_msg = msg.split(',')
    status = split_msg[2]
    return status.strip() == "A"

# Open serial port to VN-200     
ins_ser = serial.Serial(ins_port,ins_baud)
# Clear buffer
ins_ser.reset_input_buffer()

# Run until time is initialized
while not time_init:
    time.sleep (0.001) # Limit how fast the loop runs
    # Check if buffer is not empty
    if ins_ser.inWaiting() > 0:
        # Read the buffer until \n character and convert to string
        ins_buf = ins_ser.readline()
        ins_string = ins_buf.decode()
        
        # Processing of VNINS string for GPS_TOW and GPS_WEEK
        if get_header(ins_string) == "VNINS":
            # Only continue for gps time data extraction if msg is VNINS and GPS fix is valid
            if validate_msg(ins_string) and fix_stat == True:
                split_msg = ins_string.split(',')
                # Extract tow and week
                gps_tow = split_msg [1]
                gps_week = split_msg [2]
                # Calculate cur UNIX time
                cur_posix_time = calc_posix_time(gps_tow,gps_week)
                if check_rounded_time (cur_posix_time):
                    # If cur time is rounded to the second, set system time
                    time.clock_settime(time.CLOCK_REALTIME, cur_posix_time)
                    time_init = True # Flag time_init to True
                    print ("Time synced to " + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S UTC"))
        # Processing of RMC string for GPS fix and flag if fix is valid
        elif get_header(ins_string) == "GPRMC":
            if check_valid_fix(ins_string) and validate_msg(ins_string):
                fix_stat = True
ins_ser.close()
                    

    
    

