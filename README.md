# zbar-py

## Introduction
Author: [Zachary Pincus](http://zplab.wustl.edu) <zpincus@gmail.com>

Contributions: Rounak Singh <rounaksingh17@gmail.com> (example code and zbar.misc).

zbar-py is a module (compatible with both Python 2.7 and 3+) that provides an interface to the [zbar](http://zbar.sourceforge.net) bar-code reading library, which can read most barcode formats as well as QR codes. Input images must be 2D numpy arrays of type uint8 (i.e. 2D greyscale images).

The zbar library itself packaged along with zbar-py (it's built as a python extension), so no external dependencies are required. Building zbar requires the iconv library to be present, which you almost certainly have, except if you're on windows. Then you probably will need to download or build the iconv DLL. [Here](http://mlocati.github.io/articles/gettext-iconv-windows.html) are  pre-built 32- and 64-bit binaries for same.

The python code is under the MIT license, and zbar itself is licensed under the GNU LGPL version 2.1.

## Prerequisites:
* iconv -- c library required for building zbar-py; see above
* numpy  -- for running zbar-py
* pygame -- for examples using a webcam

## Simple examples:

More sophisticated examples can be found in 'examples' directory.

* Scan for barcodes in a 2D numpy array:

```python
import zbar
image = read_image_into_numpy_array(...) # whatever function you use to read an image file into a numpy array
scanner = zbar.Scanner()
results = scanner.scan(image)
for result in results:
    print(result.type, result.data, result.quality, result.position)
```

* Scan for UPC-A barcodes and perform checksum validity test:

```python
import zbar
import zbar.misc
image = read_image_into_numpy_array(...) # get an image into a numpy array
scanner = zbar.Scanner()
results = scanner.scan(image)
for result in results:
    if result.type == 'UPC-A':
        print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')))
```
