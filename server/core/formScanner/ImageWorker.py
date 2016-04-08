from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import numpy
import libzbar as zbar
from BaseEnums import *

#заметки:
#- исключение при отсутствии заголовка EXIF

class ImageWorker:


    #инициализация другим ImageWorker
    #self.imagePIL - PIL изображение
    #self.imageOpenCV - изображение OpenCV
    #self.binFlag = изображение бинарного формата (например, был применен Threshold)

    #image - интепретацию данного объекта определяет переменная status
    #status - сообщает, как именно интерпретировать объект image:
                #1. В объъкте скрывается PIL объект с открытым изображением
                #2. в image передается путь к изображению.
    #finedEXIF - флаг поиска заголовка EXIF в изображении
    def __init__( self, \
                  image, \
                  status = FILE_NAME, \
                  binFlag = 0 ):

        self.binFlag = binFlag      
        if ( status == FILE_NAME ):
            self.imagePIL = Image.open( image )
            self.imageFileName = image
            #загружаем изображения с диска
            self.loadPILImage( self.imageFileName )
            self.loadOpenCVImage( self.imageFileName )
            
        if ( status == PIL_IMAGE ):
            #просто копируем изображение
            #DPI в данном случае не нужно
            self.imagePIL = image.copy()
            self.copyPILImageToOpenCV( self.imagePIL )
            
        if ( status == IMAGE_WORKER ):

            self.imagePIL = image.getPILImage().copy()
            self.imageOpenCV = image.getOpenCVImage().copy()
            self.binFlag = image.getBinFlag()


    def setPILImage( self, imagePIL ):
        
        self.imagePIL = imagePIL

    def getPILImageCopy( self ):
        
        return self.imagePIL.copy()
        
    def copyOpenCVImageToPIL( self, imageOpenCV, binFlag = 0 ):

        flagConvert = "L"
        if ( binFlag != 0 ):
            #cv2_im = cv2.cvtColor(imageOpenCV,cv2.COLOR_BGR2RGB)
            self.imagePIL  = Image.fromarray(imageOpenCV)
            #height, width = imageOpenCV.shape[:2]
            #size = width, height
            #self.imagePIL = Image.fromstring( "1", size, imageOpenCV.tostring())

        else:
            
            height, width = imageOpenCV.shape[:2]
            size = width, height
            self.imagePIL = Image.fromstring( flagConvert, size, imageOpenCV.tostring())
        
    def copyPILImageToOpenCV( self, imagePIL ):
        
        self.imageOpenCV = cv2.cvtColor( numpy.array( imagePIL ), cv2.COLOR_RGB2BGR)

    def setOpenCVImage( self, imageOpenCV):

        self.imageOpenCV = imageOpenCV

    def loadPILImage( self, fileName ):
         self.imagePIL = Image.open( fileName )

    def loadOpenCVImage( self, fileName ):
        self.imageOpenCV = cv2.imread( fileName )
        
    #если необходимо загрузить иное изображение    
    def reLoadImage( self, fileName ):

        self.imagePIL = Image.open( fileName )

    def getPILImage( self ):

        return self.imagePIL

    def getOpenCVImage( self ):
        
        return self.imageOpenCV

    def saveImage( self, fileName ):
        
        self.imagePIL.save( fileName )

    def getImageWidth( self ):
        
        return self.imagePIL.width

    def getImageHeight( self ):

        return self.imagePIL.height


    def rotate( self, value ):

         self.imagePIL = self.imagePIL.rotate( value, \
                                               expand = True )
       
    def findContours( self ):
        #findContours - ИЗМЕНЯЕТ ИСХОДНОЕ ИЗОБРАЖЕНИЕ. ДЕЛАЕМ КОПИЮ
        justCopytForFindContours = self.imageOpenCV.copy()
        #!!! cv2.RETR_TREE !!
        _, contours, _ = cv2.findContours( justCopytForFindContours, \
                                           cv2.RETR_EXTERNAL, \
                                           cv2.CHAIN_APPROX_SIMPLE)
        return contours


    def getX_PixelsByMillimeters( self, value ):

        return round( value * ( self.imagePIL.width / WIDTH_FORM ) )

    def getY_PixelsByMillimeters( self, value ):

        return round(  value * ( self.imagePIL.height / HEIGHT_FORM ) )
        
    #получем DPI из заголовка EXIF JPEG изображения
    #ПРОВЕРКА НА ОТСУТСТВИЕ ЗАГОЛОВКА
    def getDPI( self ):
        
        return self.DPI


    def getBinFlag( self ):
        
        return self.binFlag

    #обрезает часть из изображения
    #ВОЗВРАЩАЕТ НОВОЕ ИЗОБРАЖЕНИЕ
    def getCropImage( self, start_x, start_y, width, height ):

        box = (start_x, start_y, (int)( start_x + width), ( int )( start_y + height ) )
        output_img = self.imagePIL.crop( box )
        #output_img.save( "test/crop" + str( counter ) + ".jpg")
        return output_img

    #если не задано имя выходного файла, threshold применяется к текущему изображению
    #изменяет imagePIL и imageOpenCV
    def doThreshold( self, \
                     threshold, \
                     thresholdReason = FORM_DETECTOR_THRESHOLD_REASON, \
                     destinationImageFileName = '' ):

        
        gray = cv2.cvtColor( self.imageOpenCV, cv2.COLOR_BGR2GRAY )
        threshMod = cv2.THRESH_BINARY_INV
        if ( thresholdReason == QR_CODE_DETECTOR_THRESHOLD_REASON ):
            threshMod = cv2.THRESH_BINARY
        retval, bin = cv2.threshold( gray, threshold, 255, threshMod )
        self.binFlag = 1
        if ( len( destinationImageFileName ) > 0 ):
            cv2.imwrite( destinationImageFileName, bin )
        else:
            self.imageOpenCV = bin                                        
            self.copyOpenCVImageToPIL( self.imageOpenCV )
            



    #TEST
    def doAdaptiveThreshold( self, \
                             thresholdReason = FORM_DETECTOR_THRESHOLD_REASON, \
                             adaptiveThresholdParam = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                             destinationImageFileName = '' ):
            gray = cv2.cvtColor( self.imageOpenCV, cv2.COLOR_BGR2GRAY )
            '''
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret3,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            '''
            img = cv2.medianBlur( gray,5 )
            threshMod = cv2.THRESH_BINARY_INV
            if ( thresholdReason == QR_CODE_DETECTOR_THRESHOLD_REASON ):
                threshMod = cv2.THRESH_BINARY
            th = cv2.adaptiveThreshold( img, \
                                        255, \
                                        adaptiveThresholdParam,\
                                        threshMod, \
                                        11, \
                                        2 )
            if ( len( destinationImageFileName ) > 0 ):
                cv2.imwrite( destinationImageFileName, th )
            else:
                self.imageOpenCV = th    
                self.copyOpenCVImageToPIL( self.imageOpenCV )
                self.binFlag = 1


    #TEST
    def removeNoisy( self ):
        
        blur = cv2.GaussianBlur( self.imageOpenCV, (5,5), 0 )
        ret3,th = cv2.threshold( blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU )
        self.imageOpenCV = th    
        self.binFlag = 1
        self.copyOpenCVImageToPIL( self.imageOpenCV )
        
    
    #возвращает изображение по заданному контуру (на основании текущего изображения в imagePIL)
    #возвращает ImagePIL - вырезанный на основании contour
    def getImagePILByContour( self, contour, imageFileName = '' ):
        if ( len ( imageFileName ) > 0 ):
            image = cv2.imread( imageFileName )
        else:
            image = numpy.array( self.imagePIL)
        x,y,w,h = cv2.boundingRect( contour )
        crop = image[y:y+h,x:x+w]
        image = Image.fromarray( crop )
        return image

