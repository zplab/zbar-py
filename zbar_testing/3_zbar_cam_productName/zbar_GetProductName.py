'''
Test for zbar-py using a webcam with a database lookup search for found barcodes.
Written by Rounak Singh (rounaksingh17@gmail.com)
Tested with linux

Required: pygame, Internet(Barcode lookup from databases)

Instructions:
1) Set the cam source '/dev/video0'
2) Get a pic. If pic doesnot look good, then press enter at terminal. 
   Camera will take another pic. When done press q and enter to quit camera mode
3) You will get reading on the terminal.
4) Later, program sends lookup request EAN,UPC and ISBN number to different database using Internet. 
It can print food product name and book names

Note: http://www.makebarcode.com -- Nice website to learn Barcodes
'''

import zbar
import zbar.misc
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
# This might vary depending on your PC. Try to use a good camera. 
# Laptop builtin Webcam sometimes doesnot work good.
cam_name='/dev/video1'  

pygame.init()
pygame.camera.init()
pygame.camera.list_cameras()
# Cam 
cam = pygame.camera.Camera(cam_name, (640, 480))

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
scanner = zbar.Scanner()
products=None
results =scanner.scan_from_image('barcode.jpg')
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

'''
Information on barcodes available at http://www.makebarcode.com 
and https://en.wikipedia.org/wiki/Global_Trade_Item_Number
'''

'''
Converting EAN8 to EAN13 is performed by padding zeros to 
start of EAN8. EAN8 and GTID8 are equivalent. 
See, https://en.wikipedia.org/wiki/Global_Trade_Item_Number#Format
Takes a byte array/unicode code_ean8 and returns a unicode string
'''

def get_book_name(isbn_10):
    if len(isbn_10)==10:
        print('Requesting openlibrary.org for book name of ISBN10: '+isbn_10)
        url = 'http://openlibrary.org/api/books?bibkeys=ISBN:{}&format=json&jscmd=data'.format(isbn_10)

        r = requests.get(url)
        print('Request Status:',r.status_code)
        if r.status_code ==200:
            #print(r.text)
            res=json.loads(r.text)
            #print(res)
            if len(res)!=0:
                book_details=res['ISBN:'+isbn_10]
                try:
                    print('Title:', book_details['title'])
                except:
                    print('Key not found in data received from openlibrary.org')             
            else:
                print('Not Found in database')
        else:
            print('error requesting API')

def get_product_name(product_id):
    # API address
    data_int=int(product_id)
    print('Requesting opendatasoft.com for name of product GTID {0:013d}'.format(data_int))
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
                try:
                    print('Product Name:', data_fields['gtin_nm'])
                    print('Product GTID:', data_fields['gtin_cd'])
                    print('Company Name:', data_fields['brand_nm'])
                except:
                    print('Key not found in data received from opendatasoft.com')
    else:
        print('error requesting API')

if products:
    
    for product in products:
        if product.type == 'ISBN-10':
            get_book_name(product.data)

        elif product.type == 'UPC-E':
            converted_id=zbar.misc.upce2upca(product.data)
            get_product_name(converted_id)
        else:
            get_product_name(product.data)
