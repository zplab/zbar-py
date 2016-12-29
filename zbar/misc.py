'''
This file contains some useful barcode converter, and checksum calculation.

UPC-A checksum calculation
conversions:
    EAN-8 to EAN13
    UPC-E to UPC-A.

Written by Rounak Singh
'''

import numpy

def rgb2gray(rgb):
    '''
        converts rgb to grayscale image
        rgb is of type numpy.ndarray
    '''
    return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def upca_to_ean13(upca):
    '''
    Takes unicode UPC-A. 
    Returns unicode EAN-13
    '''
    # Check length and type of ean8
    if len(upca)!=12:
        raise ValueError("full UPC-A should be of length 12")
    else:
        try:
            upca=int(upca)
        except ValueError as e:
            raise ValueError('UPC-A should be numerical digits') from e
    return '{0:013d}'.format(upca)

def ean8_to_ean13(ean8):
    '''
    Takes unicode EAN-8. 
    Returns unicode EAN-13
    '''
    # Check length and type of ean8
    if len(ean8)!=8:
        raise ValueError("EAN-8 should be of length 8")
    else:
        try:
            ean8=int(ean8)
        except ValueError as e:
            raise ValueError('EAN-8 should be numerical digits') from e
    return '{0:013d}'.format(ean8)


def upca_get_check_digit(upca):
    ''' 
    calculates the checksum of upca
    UPC-A code must be passed as str. 
    Check Digit is returned as str
    Error: returns None
    '''
    
    # return a list of digits from a number
    if len(upca)==11:
        try:
            digits = [int(d) for d in upca]
        except ValueError as e:
            raise ValueError("UPC-A should be  numerical digits") from e
    elif len(upca)==12:
        try:
            digits = [int(d) for d in upca[0:-1]]
        except ValueError as e:
            raise ValueError("UPC-A should be  numerical digits") from e
    else:
        raise ValueError("UPC-A should be of length 11 (without check digit)")

    odd_digits = digits[0::2]
    even_digits = digits[1::2]
    checksum = 0
    checksum += sum(odd_digits)*3
    checksum += sum(even_digits)

    checksum = checksum % 10
    if checksum==0:
        check_digit=0        
    else:
        check_digit=10-checksum
    return str(check_digit)

def upca_is_valid(upca):
    '''
    calculates the checksum of full upca(12 digits).
    UPC-A must be passed as str
    return type is Boolean
    '''
    
    if len(upca) == 12:
        # return a list of digits from a number
        try:
            digits = [int(d) for d in upca]
        except ValueError as e:
            raise ValueError("UPC-A should be  numerical digits") from e
        odd_digits = digits[0::2]
        even_digits = digits[1::2]
        checksum = 0
        checksum += sum(odd_digits)*3
        checksum += sum(even_digits)
        return (checksum % 10) == 0
    else:
        raise ValueError("UPC-A should be of length 12 (with check digit)")

def upce_2_upca(upc_e):
    '''
    This function converts a UPC-E code into UPC-A
    UPC-E must be passed as str.
    UPC-A is returned as str
    if any error then None is returned.
    Ref:
    http://www.taltech.com/barcodesoftware/symbologies/upc
    http://stackoverflow.com/questions/31539005/how-to-convert-a-upc-e-barcode-to-a-upc-a-barcode

    '''
    
    # converting to strings
    upc_e=str(upc_e)

    # Checking if the barcodes have numbers only
    try:
        int(upc_e)
    except ValueError as e:
        raise ValueError("UPC-E should be  numerical digits") from e
    # If the first digit of UPC-E is not 0
    if upc_e[0] != '0':
        raise ValueError("First digit of UPC-E should be zero(0)")

    upc_a='0'+upc_e[1]+upc_e[2]
    zeros='0000'

    if upc_e[6] == '0' or upc_e[6] == '1' or upc_e[6] == '2':
        upc_a+=upc_e[6]+zeros+upc_e[3:-2]
    elif upc_e[6]== '3':
        upc_a+=upc_e[3]+zeros+'0'+upc_e[4:-2]
    elif upc_e[6]== '4':
        upc_a+=upc_e[3:5]+zeros+'0'+upc_e[5]
    else:
        upc_a+=upc_e[3:6]+zeros+upc_e[6]

    # Add checksum digit
    upc_a+=upc_e[-1]

    # verify UPC-E code if valid using Checksum
    if upca_is_valid(upc_a):
        return upc_a
    else:
        msg='UPC-E is invalid. Please verify the checksum digit. \nValid checksum digit = '+upca_get_check_digit(upc_a) + \
            '\nSo, valid UPC-A is '+ upc_a[:-1] + upca_get_check_digit(upc_a)
        raise ValueError(msg)

