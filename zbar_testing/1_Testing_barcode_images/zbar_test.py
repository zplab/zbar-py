# Test for zbar-py
#
# Written by Rounak Singh (rounaksingh17@gmail.com)
#

import zbar
import numpy
from scipy import misc
import os

def rgb2gray(rgb):
    return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.114])

test_filename='test_ean8.jpg'

pwd=os.path.dirname(os.path.abspath(__file__))
test_file_path=pwd+'/test_barcodes/'+test_filename

image = misc.imread(test_file_path) # get an image into a numpy array
gray = rgb2gray(image)
gray = gray.astype(numpy.uint8)
print("{}".format(type(gray)))

print("(height,width) = {}".format(gray.shape))

# Detect EAN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_EAN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN13', 'ZBAR_CFG_POSITION', 1)])

# Detect ISBN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_ISBN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_ISBN13', 'ZBAR_CFG_POSITION', 1)])

# Detect EAN8 only -- Works well
scanner = zbar.Scanner([('ZBAR_EAN8', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN8', 'ZBAR_CFG_POSITION', 1)])

# Detect all -- sometimes, it shows wrong codes
#scanner = zbar.Scanner()

results = scanner.scan(gray)
if results==[]:
    print("No Barcode found.")
else:
    for result in results:
        print(result.type, result.data, result.quality)
        #print(result.type, result.data, result.quality,result.position)
        #print("{}".format(results))
    