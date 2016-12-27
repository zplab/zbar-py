# Test for zbar-py using a webcam
# Written by Rounak Singh (rounaksingh17@gmail.com)
# Tested with linux
#
# Required: pygame, scipy, numpy
#
# Instructions:
# 1) Set the cam source '/dev/video0'
# 2) Get a pic. If pic doesnot look good, then press enter at terminal. 
#    Camera will take another pic. When done press q and enter to quit camera mode
# 3) You will get reading on the terminal
#


import zbar

import pygame
import pygame.camera
import time
from pygame.locals import *

#----------------------------------------------------------------------------------
# Get the pic -- this will become a builtin class for zbar-py in future
# To get pic from cam or video, packages like opencv or simplecv can also be used.
#----------------------------------------------------------------------------------

# This might vary depending on your PC. Try to use a good camera. 
# Laptop builtin Webcam sometimes doesnot work good.
cam_name='/dev/video1'  

pygame.init()
pygame.camera.init()
pygame.camera.list_cameras()
# Cam 
cam = pygame.camera.Camera(cam_name, (640, 480))

screen = pygame.display.set_mode(cam.get_size())
print('''
=============
Instructions:
=============
Get a good enough pic of barcode.
If pic doesnot look good, then press enter at terminal.
Camera will take another pic.
When done press q and enter to quit camera mode
''')

while True:
    cam.start()
    time.sleep(0.5)  # You might need something higher in the beginning
    img = cam.get_image()
    screen.blit(img,(0,0))
    pygame.display.flip() # update the display
    cam.stop()
    if input() == 'q':
        break

pygame.image.save(img, "barcode.jpg")
pygame.display.quit()

#-------------------------------------------------------------------------
# Read the Barcode
#-------------------------------------------------------------------------
test_filename='barcode.jpg'

# Detect all
scanner = zbar.Scanner()

results = scanner.scan_from_image(test_filename)
if results==[]:
    print("No Barcode found.")
else:
    for result in results:
        print(result.type, result.data, result.quality)
        #print(result.type, result.data, result.quality,result.position)
        #print("{}".format(results))
    