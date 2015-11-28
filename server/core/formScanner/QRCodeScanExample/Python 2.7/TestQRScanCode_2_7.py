import zbar
import Image

SIZE = 762, 1080

def resizeImage( sourceFileName, destinationFileName, size ):
    im = Image.open( sourceFileName )
    im_resized = im.resize( size, Image.ANTIALIAS)
    im_resized.save( destinationFileName )
    return im_resized

fileName = 'source_image.png'
resizedFileName = "res_" + fileName
resizeImage( fileName, resizedFileName, SIZE )
pil = Image.open(resizedFileName).convert('L')
width, height = pil.size
raw = pil.tostring()

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

image = zbar.Image(width, height, 'Y800', raw)

scanner.scan(image)

print len(image.symbols), "symbols found."
for sym in image.symbols:
    print sym.data

