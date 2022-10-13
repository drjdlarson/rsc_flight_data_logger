#!/usr/bin/env python
# Camera server
# Tuan Luong UA RSC
# 12/26/2021

from xmlrpc.server import SimpleXMLRPCServer
try:
    # Begin an xmlrpc server
    with SimpleXMLRPCServer (("169.254.2.166",8000),logRequests=False) as server:
        # Define some functions that the controller calls
        
        # Get camera state (on/off)
        def getCameraState():
            try:
                with open('/home/pi/Desktop/nav_software/cam_state.txt', mode='r') as f:
                    state = f.readline().rstrip()
                    return state == "1"
            except:
                return False
        
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
        
        def getVNINS():
            try:
                with open('/home/pi/Desktop/nav_software/vnins.txt', mode='r') as f:
                    line = f.readline().rstrip()
                    return line
            except:
                return None
                
        # Register functions above
        server.register_function(getCameraState)
        server.register_function(getGPGGAState)
        server.register_function(getGPRMCState)
        
        # Run the server forever
        server.serve_forever()
except Exception as e:
    print (e)