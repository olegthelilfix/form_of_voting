from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import numpy
import libzbar as zbar
from BaseEnums import *

class ImageWorker:

    #изображение
    #image

    #открываем изображение
    def __init__( self, image, status = IT_IS_FILE_NAME ):

        if ( status == IT_IS_FILE_NAME ):
            #открываем избражение и узнаем его DPI
            self.imagePIL = Image.open( image )
            self.imageFileName = image
            #считаем DPI
            info = self.imagePIL._getexif()
            exifObj = {}
            if info != None:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exifObj[decoded] = value
            self.DPI = exifObj['XResolution'][0]/exifObj['XResolution'][1]
        else:
            #просто копируем изображение
            #DPI в данном случае не нужно
            self.imagePIL = image.copy()
            self.DPI = UNDEFINED_DPI_VALUE
            
    #если необходимо загрузить иное изображение    
    def reLoadImage( self, fileName ):

        self.imagePIL = Image.open( fileName )

    def getImage( self ):

        return self.imagePIL

    def saveImage( self, fileName ):
        self.imagePIL.save( fileName )

    def getImageWidth( self ):
        
        return self.imagePIL.width

    def getImageHeight( self ):

        return self.imagePIL.height
        
    #получем DPI из заголовка EXIF JPEG изображения
    #ПРОВЕРКА НА ОТСУТСТВИЕ ЗАГОЛОВКА
    def getDPI( self ):
        
        return self.DPI

    #обрезает часть из изображения
    #ПРИМЕНИТЕЛЬНО К ТЕКУЩЕМУ ИЗОБРАЖЕНИЮ В ОБЪЕКТЕ (self.imagePIL)
    def cropImage( self, start_x, start_y, width, height ):

        box = (start_x, start_y, (int)( start_x + width), (int)(start_y + height))
        output_img = self.imagePIL.crop( box )
        #output_img.save( "test/crop" + str( counter ) + ".jpg")
        return output_img

    #если не задано имя выходного файла, threshold применяется к текущему изображению
    def doThreshold( self, threshold, destinationImageFileName = '' ):
        imageOpenCV = cv2.cvtColor( numpy.array(self.imagePIL ), cv2.COLOR_RGB2BGR)
        #gray = cv2.cvtColor( imageOpenCV, cv2.COLOR_BGR2GRAY )
        retval, bin = cv2.threshold( imageOpenCV, threshold, 255, cv2.THRESH_BINARY)
        if ( len( destinationImageFileName ) > 0 ):
            cv2.imwrite( destinationImageFileName, bin )
        else:
            self.imagePIL = Image.fromarray(bin)

    def getImageByContour( contour, imageWithCells, outputImageFileName ):

        x,y,w,h = cv2.boundingRect( contour )
        crop = imageWithCells[y:y+h,x:x+w]
        cv2.imwrite( outputImageFileName, crop)

