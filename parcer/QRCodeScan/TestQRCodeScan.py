#Кусок кода для поиска QR на изображении
#
#Рядом в папке расположены файлы:
# source_image  - исходное изображение
# mini_qr_code - QR код, который не удается распознать

import libzbar as zbar
from PIL import Image

def scanImageForQRCode( fileName ):
    pil = Image.open( fileName )
    symbols = zbar.Image.from_im( pil ).scan()
    return symbols

if __name__ == '__main__':
    fileName = '12345.png'
    'сканируем QR код'
    symbols = scanImageForQRCode( fileName )
    'если что-то нашли на изображении '
    print( "len=", len(symbols) )
    if len( symbols ):
        for symbol in symbols:
            print(symbol)

