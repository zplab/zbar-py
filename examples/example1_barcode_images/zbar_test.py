''' Example 1 for zbar-py
    Written by Rounak Singh (rounaksingh17@gmail.com)
    Prequisite: zbar, pygame
'''
import zbar
import zbar.misc
import numpy
import pygame.image
import pygame.surfarray

def get_image_array_from_file(image_filename):
    '''
        It scans barcode using a image (png,jpg,tiff,etc. are supported).
        Image should be a greyscale or RGB.
        Take a filename, if file not found then throws exception FileNotFoundError.
        Returns barcode if successful, otherwise returns empty list
    '''
    image_pygame_surface=pygame.image.load(image_filename)
    image_ndarray=pygame.surfarray.array3d(image_pygame_surface)

    if(len(image_ndarray.shape)<3):
        #Image is grayscale
        pass
    elif len(image_ndarray.shape)==3:
        #Image is RGB
        image_ndarray = zbar.misc.rgb2gray(image_ndarray)
    else:
        raise ValueError('Please enter a Greyscale or RGB image.')

    image_ndarray = image_ndarray.astype(numpy.uint8)
    return image_ndarray


#
#
test_filename='test_isbn2.jpg'
test_file_path='test_images/'+test_filename

# Detect EAN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_EAN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN13', 'ZBAR_CFG_POSITION', 1)])

# Detect ISBN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_ISBN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_ISBN13', 'ZBAR_CFG_POSITION', 1)])

# Detect EAN8 only -- Works well
#scanner = zbar.Scanner([('ZBAR_EAN8', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN8', 'ZBAR_CFG_POSITION', 1)])

# Detect I25 only -- Works well
#scanner = zbar.Scanner([('ZBAR_I25', 'ZBAR_CFG_ENABLE', 1),('ZBAR_I25', 'ZBAR_CFG_POSITION', 1)])

# Detect all
scanner = zbar.Scanner()

image_as_numpy_array=get_image_array_from_file(test_file_path)

results = scanner.scan(image_as_numpy_array)
if results==[]:
    print("No Barcode found.")
else:
    for result in results:
        # By default zbar returns barcode data as byte array, so decoding byte array as utf-8
        print(result.type, result.data.decode("utf-8"), result.quality)
        #print(result.type, result.data.decode("utf-8"), result.quality,result.position)
        #print("{}".format(results))
