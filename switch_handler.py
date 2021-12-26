#!/usr/bin/env python
# Switch interrupt script
# Tuan Luong UA RSC
# 12/26/2021

# Import libraries
import os
import RPi.GPIO as GPIO
import time

led_gpio = 13
switch_gpio = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_gpio, GPIO.OUT,initial = 0)
GPIO.setup(switch_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
camera_state = False


def switch_state (channel):
    time.sleep(0.1)
    if not GPIO.input(switch_gpio):
        camera_state = True
        with open('/home/pi/Desktop/nav_software/cam_state.txt', mode = 'w') as f:
            f.write('1')
        GPIO.output(led_gpio,1)
    else:
        camera_state = False
        with open('/home/pi/Desktop/nav_software/cam_state.txt', mode = 'w') as f:
            f.write('0')
        GPIO.output(led_gpio,0)
        
    
GPIO.add_event_detect(switch_gpio, GPIO.BOTH, callback=switch_state, bouncetime = 600)
while 1:
    time.sleep(0.2)

    
   
    
    