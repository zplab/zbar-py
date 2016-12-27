''' Example 1 for zbar-py
    Written by Rounak Singh (rounaksingh17@gmail.com)

'''
import zbar

test_filename='test.jpeg'
test_file_path='test_barcodes/'+test_filename

# Detect EAN13 only -- Works well
scanner = zbar.Scanner([('ZBAR_EAN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN13', 'ZBAR_CFG_POSITION', 1)])

# Detect ISBN13 only -- Works well
#scanner = zbar.Scanner([('ZBAR_ISBN13', 'ZBAR_CFG_ENABLE', 1),('ZBAR_ISBN13', 'ZBAR_CFG_POSITION', 1)])

# Detect EAN8 only -- Works well
#scanner = zbar.Scanner([('ZBAR_EAN8', 'ZBAR_CFG_ENABLE', 1),('ZBAR_EAN8', 'ZBAR_CFG_POSITION', 1)])

# Detect all
#scanner = zbar.Scanner()

results = scanner.scan_from_image(test_file_path)
if results==[]:
    print("No Barcode found.")
else:
    for result in results:
        print(result.type, result.data, result.quality)
        #print(result.type, result.data, result.quality,result.position)
        #print("{}".format(results))
