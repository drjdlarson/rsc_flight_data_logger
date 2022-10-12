#
#  Camera Communications
#       C. O'Neill 2020, RSC, Univ of Alabama
#       Interfaces with D850 and FLIR Vue Pro R

import time
import serial
import gpiozero
import math
import xmlrpc.client




# NMEA checksum (Line = characters between $ and *)
def checksum(line):
    cksum = 0
    for i in line:
        cksum ^= ord(i)
    s = '{:02X}'.format(cksum)
    return s

# NMEA Returns NMEA header (1st 6 characters of line)
def getNMEAheader(line):
    return line[:6]

# Is the line a valid NMEA sentence?
def validateNMEAline(line):
    try:
        splits = line.split("*")
        checkvalue = splits[1]
        sentence = splits[0]
        line = sentence.split('$')
        sentence = line[1]
    except:
        return False
    if checksum(sentence) == checkvalue:
        return True
    else:
        return False

# NMEA GPGGA sentence with compliant length
def processGPGGA(lineraw):
    try:
        splits = lineraw.split("*")
        checkvalue = splits[1]
        sentence = splits[0]
        line = sentence.split('$')
        sentence = line[1]
        data = sentence.split(",")
        lat = float(data[2])
        lon = float(data[4])
        data[2] = "{0:.4f}".format(lat)
        data[4] = "{0:.4f}".format(lon)
        data[6] = "1"
        data[14] = ""
        corrected = ",".join(data)
        corrected = "$"+corrected+"*"+checksum(corrected)+"\r\n"
        return corrected
    except:
        return lineraw 

# NMEA GPRMC sentence with compliant length
def processGPRMC(lineraw):
    try:
        #print(lineraw)
        splits = lineraw.split("*")
        checkvalue = splits[1]
        sentence = splits[0]
        line = sentence.split('$')
        sentence = line[1]
        data = sentence.split(",")   
        lat = float(data[3])
        lon = float(data[5])
        data[3] = "{0:.4f}".format(lat)
        data[5] = "{0:.4f}".format(lon)

        corrected = ",".join(data)
        corrected = "$"+corrected+"*"+checksum(corrected)+"\r\n"
        return corrected
    except:
        return lineraw

print(" Camera Comm started.... ")

# Camera Pins
camera = gpiozero.LED(24)
shutter = gpiozero.LED(23)
flir = gpiozero.Servo(2)

# Init Pins
flir.min()
camera.on()
shutter.on()  
print("     pins init")

# Server 
HOST = '169.254.2.166'
PORT = '8000'
HostURL ='http://'+HOST+":"+PORT
backend = xmlrpc.client.ServerProxy(HostURL)
print("     backend init")

# Camera GPS
ser0 = serial.Serial(
    port = '/dev/ttyAMA0',
    baudrate = 4800,
    )
cameraGPS = ser0
print("     camera nmea init")

# Turns on the Level Converter
oe = gpiozero.LED(4)
oe.on()
print("     level converter init")

# Timer
class Cameratimer:
    def __init__(self,period):
        self.time0 = 0
        self.period = period
        self.state = 0
    
    def trigger(self):
        new = time.time()
        # Trigger period 
        if( (new - self.time0) >= self.period) and self.state == 0:
            self.time0 = new
            self.state = 1
            return True
        
        elif (new - self.time0) > 0.5 and self.state == 1:
            self.state = 2
            return True
        elif self.state ==2:
            self.state = 0
            return False
        

# Setup 
camtimer = Cameratimer(3.0)
gpstimer = Cameratimer(1.0)
print("     timers setup and running")

# Run persistant
while 1:
    try:
        #print(".")
        #time.sleep(0.05)
        #
        
        if camtimer.trigger():
            cameraON = False
            cameraON = backend.getCameraState()
            if not cameraON:
                print("Cameras off")
                camtimer.state = 0
            else:
                print("Cameras on")
            
            # Check the camera state
            if camtimer.state == 0:
                flir.min()
                camera.on()
                shutter.on()  
                #turn off everything
            elif camtimer.state == 1:
                flir.max()
                camera.off()
                shutter.off()
            elif camtimer.state == 2:
                # Release the shutter button
                camera.on()
                shutter.on()                  
        
        if gpstimer.trigger() and gpstimer.state==1:
            line = backend.getGPGGAState().rstrip()
            line = processGPGGA(line)
            cameraGPS.write(line.encode())
            print(line)
      
            line = backend.getGPRMCState()
            line = processGPRMC(line)
            cameraGPS.write(line.encode())
            print(line    )

    except Exception as e:
        print("Exception:", e)
        backend = xmlrpc.client.ServerProxy(HostURL)