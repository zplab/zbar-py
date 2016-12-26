# zbar-py

## Introduction
Authors: [Zachary Pincus](http://zplab.wustl.edu) <zpincus@gmail.com> , [Rounak Singh] <rounaksingh17@gmail.com> 

A Python module (compatible with both Python 2.7 and 3+) that provides an interface to the [zbar](http://zbar.sourceforge.net) bar-code reading library, which can read most barcode formats as well as QR codes. Input images must be 2D numpy arrays of type uint8, in other words 2D Greyscale.

Zbar is built as a python extension, so no external dependencies are required. Building zbar requires libiconv to be present, which probably isn't a problem except maybe on windows. The python code is under the MIT license, and zbar itself is licensed under the GNU LGPL version 2.1.

## Prerequisites:
* libiconv -- for building zbar-py
* numpy, scipy -- for running zbar-py
* pygame -- for testing zbar-py with webcam

## Installing
* For linux(tested):

```bash
$ pip install zbar-py
```

* For other plateforms (windows/mac):

First, try PyPI installation using above command. Otherwise, you will have to use setuptools, it should install. Not tested yet.

Make sure that you have libiconv on your build env.
Then Do

```bash
$ python setup.py install

```

## Testing
* Test with Images:

For testing, Install the prequisites then goto zbar_testing/1_Testing_barcodes_images directory, run

```bash
$ python zbar_test.py

```

* Test with Webcam:
For testing using cam, install the package pygame, then goto zbar_testing/2_Testing_barcodes_cam, Follow instructions in zbar_test.py

```bash
$ python zbar_test.py

```

Note: 

* Make sure that you get a clear pic with webcam. Your laptop camera may not click good enough pics.

* Other packages for using cam to take pics are opencv and simplecv. However, opencv has python3 extension -- no deb package available, so you will have to build it. Building opencv is little difficult, requires lots of dependencies. And, simplecv has no extension for python3 till date.

## Examples:

Simple examples are mentioned below. More examples can be found [here](https://github.com/rounaksingh/zbar-py/tree/master/zbar_testing)

* With image file. Reads most types of Barcode

```python
import zbar
scanner = zbar.Scanner()
results = scanner.scan_from_image('image_filename.png')
for result in results:
    print(result.type, result.data, result.quality, result.position)
```

* With image file. Reads EAN-13 only

```python
import zbar
scanner = zbar.Scanner([('ZBAR_EAN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN13', 'ZBAR_CFG_POSITION', 1)])
results = scanner.scan_from_image('image_filename.png')
for result in results:
    print(result.type, result.data, result.quality, result.position)
```

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
import zbar
import zbar.misc
scanner = zbar.Scanner()
results = scanner.scan_from_image('image_filename.png')
for result in results:
    print(result.type, result.data, result.quality, result.position)

''' if all successful, then UPC-A barcode is in result.data'''
valid = zbar.misc.upca_is_valid(result.data)
if valid == True:
    print('code is valid')
elif valid == False:
    print('code is invalid')
elif valid == None:
    print('Barcode is not read properly')
```
