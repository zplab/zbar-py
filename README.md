# zbar-py

Author: [Zachary Pincus](http://zplab.wustl.edu) <zpincus@gmail.com>

A Python module (compatible with both Python 2.7 and 3+) that provides an
interface to the [zbar](http://zbar.sourceforge.net) bar-code reading library, which can read most barcode formats as well as QR codes. Input images must be 2D numpy arrays of type uint8.

Example:
    import zbar
    image = read_image_into_numpy_array(...) # get an image into a numpy array
    scanner = zbar.Scanner()
    results = image.scan()
    for result in results:
        print(result.type, result.data, result.quality, result.location)

Zbar is built as a python extension, so no external dependencies are required. Building zbar requires libiconv to be present, which probably isn't a problem except maybe on windows. The python code is under the MIT license, and zbar itself is licensed under the GNU LGPL version 2.1.