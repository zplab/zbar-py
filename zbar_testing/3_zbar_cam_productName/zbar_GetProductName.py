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
# Note: http://www.makebarcode.com -- Nice website to learn Barcodes


import zbar
import numpy
from scipy.misc import *
import os

import pygame
import pygame.camera
import time
from pygame.locals import *

import requests
import json
#-------------------------------------------------------------------------
# Get the pic
#-------------------------------------------------------------------------
pygame.init()
print()
pygame.camera.init()
pygame.camera.list_cameras()
# Cam 
cam = pygame.camera.Camera("/dev/video0 ", (640, 480))

screen = pygame.display.set_mode(cam.get_size())
print('Get a pic of barcode. If pic doesnot look good, then press enter at terminal. \
       Camera will take another pic. When done press q and enter to quit camera mode')
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
def rgb2gray(rgb):
    return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.114])

test_filename='barcode.jpg'

image = imread(test_filename) # get an image into a numpy array
gray = rgb2gray(image)
gray = gray.astype(numpy.uint8)
imsave('barcode_gray.png', gray)

print("{}".format(type(gray)))

print("(height,width) = {}".format(gray.shape))

# Detect EAN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_EAN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN13', 'ZBAR_CFG_POSITION', 1)])

# Detect ISBN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_ISBN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_ISBN13', 'ZBAR_CFG_POSITION', 1)])

# Detect EAN8 only -- Works well
#scanner = zbar.Scanner([('ZBAR_EAN8', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN8', 'ZBAR_CFG_POSITION', 1)])

# Detect all -- sometimes, it shows wrong codes
scanner = zbar.Scanner()

products=None

results = scanner.scan(gray)
if results==[]:
    print("No Barcode found.")
else:
    for result in results:
        print(result.type, result.data, result.quality)
        #print(result.type, result.data, result.quality,result.position)
        #print("{}".format(results))
    products=results

#-------------------------------------------------------------------------
# Get product Name, Product manufacturer
#-------------------------------------------------------------------------


if products:
    
    for product in products:
        # API address
        data_int=int(product.data)
        print('Requesting name for product GTID {0:013d}'.format(data_int))
        url = 'http://pod.opendatasoft.com/api/records/1.0/search/?dataset=pod_gtin&q={0:013d}&facet=gpc_s_nm&facet=brand_nm&facet=owner_nm&facet=gln_nm&facet=prefix_nm'.format(data_int)

        r = requests.get(url)
        print('Request Status:',r.status_code)
        if r.status_code ==200:
            #print(r.text)
            res=json.loads(r.text)
            #print(res)
            records=res['records']
            if res['nhits'] == 0:
                print('Product Not found')
            else:
                print('NumHits:', res['nhits'] )
                for record in records:
                    #print(record)
                    data_fields=record['fields']
                    print('Product Name:', data_fields['gtin_nm'])
                    print('Product GTID:', data_fields['gtin_cd'])
                    print('Company Name:', data_fields['brand_nm'])
        else:
            print('error requesting API')
        