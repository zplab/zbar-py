''' Example for zbar-py
    Written by Rounak Singh (rounaksingh17@gmail.com)
    Prequisite: zbar, , one of {freeimage, pygame, skimage, scipy}
'''
import zbar
import zbar.misc
import pathlib

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

barcode_dir = pathlib.Path(__file__).parent / 'barcodes'
scanner = zbar.Scanner()
for image in sorted(barcode_dir.glob('*')):
    print('scanning image ' + image.name)
    image_as_numpy_array = imread(image)
    results = scanner.scan(image_as_numpy_array)
    if not results:
        print('  No barcode found.')
    for result in results:
        # zbar returns barcode data as byte array, so decode byte array as ascii
        print('  type: {}, data: {} quality: {}'.format(result.type, result.data.decode('ascii'), result.quality))
