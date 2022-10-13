#!/usr/bin/env python
# Switch interrupt script
# Tuan Luong UA RSC
# 12/26/2021

# Import libraries
import os
import RPi.GPIO as GPIO
import time
import xmlrpc.client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_gpio, GPIO.OUT,initial = 0)
GPIO.setup(switch_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

loop_time_ms = 10 #100 Hz
    
HOST = '169.254.2.166'
PORT = '8000'
HostURL ='http://'+HOST+":"+PORT
backend = xmlrpc.client.ServerProxy(HostURL)   

pitch_deg = 0
roll_deg = 0
    
def checksum (sentence, chk_val):
    try:
        cksum = 0
        for i in sentence:
            cksum ^= ord(i)
            s = '{:02X}'.format(cksum)
        if s == chk_val:
            return True
        else:
            return False
    except:
        return False


def processVNINS(lineraw):
    try:
        splits = lineraw.split("*")
        chksum_val = splits[1]
        senstence = splits[0]
        header_splits = senstence.split("$")
        line = header_splits[1]
        data = line.split(",")
        if not checksum (line, chksum_val):
            return False
        global pitch_deg 
        pitch_deg = data[6]
        global roll_deg 
        roll_deg = data[7]
        return True
    except:
        return False


# Run indefinitely
while 1:
    try:
        loop_start_time_ms = time.time()
        print (".")
        line = backend.getVNINS()
        if line is None:
            continue
        if processVNINS(line):
            print (pitch_deg," | ", roll_deg)
        time_remaining_ms = loop_time_ms - (time.time() - loop_start_time_ms)
        time.sleep(time_remaining_ms/1000)
        
    except Exception as e:
        print("Exception:",e)
        pitch_deg = 0
        roll_deg = 0
        backend = xmlrpc.client.ServerProxy(HostURL) 