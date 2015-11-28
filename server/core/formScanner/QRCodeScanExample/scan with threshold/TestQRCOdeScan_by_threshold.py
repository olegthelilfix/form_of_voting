import libzbar as zbar
from PIL import Image
import cv2

#после попыток распознавания QR кода, делаем вывод, что
#необходимость в изменения разрешения изображения пока что отсутствует
#используем только threshold

def resizeImage( sourceImage, destinationFileName, size ):
    im_resized = sourceImage.resize( size )
    im_resized.save( destinationFileName )
    return im_resized


#возвращает значение threshold примененное к изображению
def doThreshold( sourceImageFileName, destinationImageFileName, thresholdValue ):

    img = cv2.imread( sourceImageFileName )
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    retval, bin = cv2.threshold( gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite( destinationImageFileName, bin )

def scanImageForQRCode( fileName ):
    
    pil = Image.open( fileName ).convert('L')

    symbols = zbar.Image.from_im( pil ).scan()
    return symbols

if __name__ == '__main__':
    #имя исходного файла с изображением QR кода
    fileName = '61img_with_possible_qr.png'
    #имя файла с измененным разрешением изображения QR кода
    #(будет создан как новый)
    resizedFileName = "res_" + fileName

    im = Image.open( fileName  )
    #меняем разрешение
    #но пока в этом нет необходимости
    #newSize = im.width * 2, im.height * 2
    #resizeImage( im, resizedFileName, newSize )
    
    imageNameWithThreshold = "threshold_" + fileName
    for i in range( 1, 10 ):
        threshold = 200 - i * 10
        #fileName - исходное изображение, по отношению к
        #           которому и будет применен threshold
        #imageNameWithThreshold - изображение на выходе с примененным
        #                         threshold
        doThreshold( fileName, imageNameWithThreshold, threshold  )
        symbols = scanImageForQRCode( imageNameWithThreshold )
        if ( len( symbols ) > 0 ):
            print( "threshold value = ", threshold )
            print( symbols )    
            break
      
