try:
    import setuptools
    from setuptools import setup, Extension
    setuptools_opts = dict(install_requires='numpy')
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    setuptools_opts = {}

import os
import ctypes
import ctypes.util

SRCS = '''Source/zbar/decoder.c
Source/zbar/decoder/code128.c
Source/zbar/decoder/code39.c
Source/zbar/decoder/ean.c
Source/zbar/decoder/i25.c
Source/zbar/decoder/pdf417.c
Source/zbar/decoder/qr_finder.c
Source/zbar/error.c
Source/zbar/img_scanner.c
Source/zbar/qrcode/bch15_5.c
Source/zbar/qrcode/binarize.c
Source/zbar/qrcode/isaac.c
Source/zbar/qrcode/qrdec.c
Source/zbar/qrcode/qrdectxt.c
Source/zbar/qrcode/rs.c
Source/zbar/qrcode/util.c
Source/zbar/refcnt.c
Source/zbar/scanner.c
Source/zbar/symbol.c'''.split('\n')

INCLUDE = 'Source', 'Source/zbar'

def has_libc_iconv():
    if os.name != 'posix':
        return False
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    return hasattr(libc, 'iconv')

# don't try to link to standalone iconv library if it's already in libc
# (iconv is in glibc, but on OS X one needs a stanalone libiconv)
LIBS = [] if has_libc_iconv() else ['iconv']

zbar = Extension('zbar._zbar',
    sources=['zbar/_zbar.c'] + SRCS,
    include_dirs=INCLUDE,
    define_macros=[
        ('ENABLE_QRCODE', None),
        ('ENABLE_EAN', None),
        ('ENABLE_I25', None),
        ('ENABLE_CODE39', None),
        ('ENABLE_CODE128', None),
        ('ENABLE_PDF417', None),
        ('HAVE_INTTYPES_H', None),
        ('ZBAR_VERSION_MAJOR', 0),
        ('ZBAR_VERSION_MINOR', 10),
        ('NO_STATS', None)],
    libraries=LIBS
)

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(name='zbar-py',
      version='1.0.4',
      description='zbar package',
      url='https://github.com/zplab/zbar-py',
      author='Zachary Pincus',
      author_email='zpincus@gmail.com',
      ext_modules=[zbar],
      packages=['zbar'],
      license='MIT',
      long_description=long_description,
      **setuptools_opts)

