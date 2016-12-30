'''
database lookup search for barcodes.
Written by Rounak Singh (rounaksingh17@gmail.com)
Tested with linux

Note: http://www.makebarcode.com -- Nice website to learn Barcodes
'''

import requests
import json
import pathlib

import zbar
import zbar.misc


def imread(image_filename):
    '''Example image-reading function that tries to use freeimage, skimage, scipy or pygame to read in an image'''

    try:
        from freeimage import read as read_image
    except ImportError:
        read_image = None

    if read_image is None:
        try:
            from skimage.io import imread as read_image
        except ImportError:
            pass

    if read_image is None:
        try:
            from scipy.misc import imread as read_image
        except ImportError:
            pass

    if read_image is None:
        try:
            import pygame.image
            import pygame.surfarray
            def read_image(image_filename):
                image_pygame_surface = pygame.image.load(image_filename)
                return pygame.surfarray.array3d(image_pygame_surface)
        except ImportError:
            raise ImportError('for this example freeimage, skimage, scipy, or pygame are required for image reading')

    image = read_image(image_filename)
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    return image

def print_book_name(isbn):
    print('Requesting openlibrary.org for book name of ISBN: '+isbn)
    url = 'http://openlibrary.org/api/books?bibkeys=ISBN:{}&format=json&jscmd=data'.format(isbn)

    r = requests.get(url)
    print('Request Status:', r.status_code)
    if r.status_code == 200:
        res=json.loads(r.text)
        if len(res)!=0:
            book_details=res['ISBN:' + isbn]
            try:
                print('Title:', book_details['title'])
            except:
                print('Title not found in data received from openlibrary.org')
        else:
            print('Not Found in database')
    else:
        print('error requesting API')

def print_product_name(product_id):
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

def lookup_barcodes(results):
    """Look up barcodes from a list of barcode results returned by zbar.Scanner.scan"""
    for result in results:
        if result.type.startswith('ISBN'):
            print_book_name(result.data.decode("ascii"))
        elif result.type == 'UPC-E':
            converted_id=zbar.misc.upce2upca(result.data.decode("ascii"))
            print_product_name(converted_id)
        else:
            print_product_name(result.data.decode("ascii"))


barcode_dir = pathlib.Path(__file__).parent / 'barcodes'
scanner = zbar.Scanner()
for image in sorted(barcode_dir.glob('*')):
    print('Scanning image ' + image.name)
    image_as_numpy_array = imread(image)
    results = scanner.scan(image_as_numpy_array)
    lookup_barcodes(results)