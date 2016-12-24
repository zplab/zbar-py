# zbar-py

## Introduction
Author: [Zachary Pincus](http://zplab.wustl.edu) <zpincus@gmail.com>

A Python module (compatible with both Python 2.7 and 3+) that provides an interface to the [zbar](http://zbar.sourceforge.net) bar-code reading library, which can read most barcode formats as well as QR codes. Input images must be 2D numpy arrays of type uint8, in other words 2D Greyscale.

Zbar is built as a python extension, so no external dependencies are required. Building zbar requires libiconv to be present, which probably isn't a problem except maybe on windows. The python code is under the MIT license, and zbar itself is licensed under the GNU LGPL version 2.1.

## Prerequisites:
* libiconv -- for building zbar-py
* numpy -- for running zbar-py
* scipy -- for testing zbar-py

## Installing and testing
Make sure that you have libiconv on your build env
Do

```bash
$ python setup.py install

```

For testing, Install the prequisites then goto zbar_testing directory, run

```bash
$ python zbar_test.py
'''

## Example:
```python
import zbar
image = read_image_into_numpy_array(...) # get an image into a numpy array
scanner = zbar.Scanner()
results = scanner.scan(image)
for result in results:
    print(result.type, result.data, result.quality, result.location)
```