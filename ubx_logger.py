#!/usr/bin/env python
# Log data from serial port
# Tuan Luong UA RSC
# 12/26/2021

# Import libraries
import serial
import datetime
import time
import os

# Define port for F9P receiver
ubx_port = '/dev/ttyACM0'
ubx_baud = 115200

# Define location and name of output file
file_prefix = '/home/pi/Desktop/nav_dat/'
ubx_filename = file_prefix + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_ubx.txt"


with serial.Serial(ubx_port,ubx_baud,timeout = 5) as ubx_ser, open(ubx_filename, mode = 'ab') as outputfile: # Open the serial port to the F9P
    ubx_ser.reset_input_buffer() # Clear the input buffer
    try:
        while 1: 
            time.sleep (0.05)  # Just so the program does not run too fast
            # Check input buffer for new message
            if ubx_ser.inWaiting() > 0:
                bytesToRead = ubx_ser.inWaiting()   # Count number of bytes in buffer
                ubx_buf = ubx_ser.read(bytesToRead) # Read the input buffer and put it in another buffer
                outputfile = open(ubx_filename, mode = 'ab')   # Open ouput file to append bytes
                outputfile.write(ubx_buf)                      # write the buffer to file
                outputfile.flush()                             # Close file
    except KeyboardInterrupt:
        print ("Logging stopped")
        ubx_ser.close()
    except:
        ubx_ser.close()
