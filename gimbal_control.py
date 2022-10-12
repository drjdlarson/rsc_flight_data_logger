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
    
# Run indefinitely
while 1:
    try:
        loop_start_time_ms = time.time()
        print (".")


        time_remaining_ms = loop_time_ms - (time.time() - loop_start_time_ms)
        time.sleep(time_remaining_ms/1000)
        
    except Exception as e:
        print("Exception:",e)
        backend = xmlrpc.client.ServerProxy(HostURL) 