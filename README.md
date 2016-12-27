# zbar-py

## Introduction
Authors: [Zachary Pincus](http://zplab.wustl.edu) <zpincus@gmail.com>

A Python module (compatible with both Python 2.7 and 3+) that provides an interface to the [zbar](http://zbar.sourceforge.net) bar-code reading library, which can read most barcode formats as well as QR codes. Input images must be 2D numpy arrays of type uint8, in other words 2D Greyscale.

Zbar is built as a python extension, so no external dependencies are required. Building zbar requires libiconv to be present, which probably isn't a problem except maybe on windows. The python code is under the MIT license, and zbar itself is licensed under the GNU LGPL version 2.1.

## Prerequisites:
* libiconv -- for building zbar-py
* numpy  -- for running zbar-py
* scipy, pygame -- for examples

## Installing
You will have to use setuptools, it should install. Not tested yet.

Make sure that you have libiconv on your build env.
Then Do
```bash
   $ python setup.py install
```

## Examples:

Simple examples are mentioned below. More examples can be found in examples directory.

* With 2D numpy array. Reads most types of Barcode

```python
import zbar
image = read_image_into_numpy_array(...) # get an image into a numpy array
scanner = zbar.Scanner()
results = scanner.scan(image)
for result in results:
    print(result.type, result.data, result.quality, result.position)
```

* UPC-A Barcode checksum validity test

```python
import zbar.misc

''' if UPC-A utf-8-encoded is passed as upca'''
valid = zbar.misc.upca_is_valid(upca)
if valid == True:
    print('code is valid')
elif valid == False:
    print('code is invalid')
elif valid == None:
    print('Barcode is not read properly')
```
