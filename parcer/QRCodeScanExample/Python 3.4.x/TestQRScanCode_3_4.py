import libzbar as zbar
from PIL import Image
import numpy as np

SIZE = 762, 1080

def resizeImage( sourceFileName, destinationFileName, size ):
    im = Image.open( sourceFileName )
    im_resized = im.resize( size, Image.ANTIALIAS)
    im_resized.save( destinationFileName )
    return im_resized


def scanImageForQRCode( fileName ):
    
    pil = Image.open( fileName )
    symbols = zbar.Image.from_im( pil ).scan()
    return symbols


if __name__ == '__main__':
    fileName = 'source_image.png'
    resizedFileName = "res_" + fileName
    resizeImage( fileName, resizedFileName, SIZE )
    'сканируем на QR код'
    symbols = scanImageForQRCode( resizedFileName )
    'если что-то нашли на изображении '
    print( "len=", len(symbols) )
    if len( symbols ):
        for symbol in symbols:
            print(symbol)

