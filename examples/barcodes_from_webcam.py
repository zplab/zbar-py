# Test for zbar-py using a webcam
# Written by Rounak Singh (rounaksingh17@gmail.com)
# Tested with linux
#
# Required: pygame
#
# Instructions:
# 1) Set the cam source '/dev/video0'
# 2) Get a pic. If pic doesnot look good, then press enter at terminal.
#    Camera will take another pic. When done press q and enter to quit camera mode
# 3) You will get reading on the terminal
#


import zbar
import zbar.misc
import numpy

import time
import pygame
import pygame.camera
import pygame.image
import pygame.surfarray

def get_image_array_from_cam(cam_name, cam_resolution):
    '''Get animage ndarray from webcam using pygame.'''
    pygame.init()
    pygame.camera.init()
    pygame.camera.list_cameras()
    cam = pygame.camera.Camera(cam_name, cam_resolution)

    screen = pygame.display.set_mode(cam.get_size())
    print('Get a pic of barcode. If pic doesnot look good, then press enter at terminal. \
           Camera will take another pic. When done press q and enter to quit camera mode')
    while True:
        cam.start()
        time.sleep(0.5)  # You might need something higher in the beginning
        pygame_screen_image = cam.get_image()
        screen.blit(pygame_screen_image, (0,0))
        pygame.display.flip() # update the display
        cam.stop()
        if input() == 'q':
            break

    pygame.display.quit()

    image_ndarray = pygame.surfarray.array3d(pygame_screen_image)

    if len(image_ndarray.shape) == 3:
        image_ndarray = zbar.misc.rgb2gray(image_ndarray)

    return image_ndarray


#----------------------------------------------------------------------------------
# Get the pic
# To get pic from cam or video, packages like opencv or simplecv can also be used.
#----------------------------------------------------------------------------------

# Cam name might vary depending on your PC.
cam_name='/dev/video1'
cam_resolution=(640,480)      # A general cam resolution

img_ndarray = get_image_array_from_cam(cam_name, cam_resolution)

#-------------------------------------------------------------------------
# Read the Barcode
#-------------------------------------------------------------------------

# Detect all
scanner = zbar.Scanner()

results = scanner.scan(img_ndarray)
if results==[]:
    print("No Barcode found.")
else:
    for result in results:
        # By default zbar returns barcode data as byte array, so decode byte array as ascii
        print(result.type, result.data.decode("ascii"), result.quality)
