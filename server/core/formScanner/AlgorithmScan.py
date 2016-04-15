#---------------------------------------------------
# Имя файла с изображением бланка.
#---------------------------------------------------
SOURCE_IMAGE = "003.jpg"
#---------------------------------------------------

import cv2
import PIL
from TokenFileWorker import *
from FormRotation import *
from BaseEnums import *
from PIL import Image
from PIL.ExifTags import TAGS
import libzbar as zbar
from numpy import arccos
from ImageWorker import *
import math
import sys
from BigQRCodeData import *
from CellsDetector import *
from SmallQRCodeData import *
from ScanResult import *
from ScanResultEnums import *

counter = 0

COUNT_OF_QR_CODES_ON_PAGE = 3

FAST_ALGORITHM_IS_WORKED = 0


TRESHOLD_ON_MARKED_STATUS = 0.086

y = 1
x = 0

height_big_qr_code = 0
width_big_qr_code = 0


#вырезаем изображение - координаты в ПИКСЕЛЯХ
def crop_image( input_image, isItFileName, start_x, start_y, width, height ):
        
        if ( isItFileName == 1):
                input_img = Image.open(input_image)
        else:
                input_img = input_image

        box = (start_x, start_y, (int)( start_x + width), (int)(start_y + height))
        #print( box )
        output_img = input_img.crop( box )
        #output_img.save( "test/crop" + str( counter ) + ".jpg")
        return output_img

def scanImageForQRCode( sourceImage, isItFileName = 1 ):
        if ( isItFileName == 1 ):
                pil = Image.open( sourceImage ).convert('L')
        else:
                pil = sourceImage
        symbols = zbar.Image.from_im( pil ).scan()
        return symbols

#рассчитываем координаты кода относительно координат изображения
def correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y ):
    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
    #y = bottomLeftCorners[y] - topLeftCorners[y]
    topLeftCorners = topLeftCorners[ x ] + start_x, topLeftCorners[ y ] + start_y
    #topLeftCorners[y] = topLeftCorners[ y ] + start_y
    bottomLeftCorners = bottomLeftCorners[x ] + start_x, start_y + bottomLeftCorners[ y ]
    #bottomLeftCorners[ y ] = bottomLeftCorners[ y ] + topLeftCornest[ y ]
    topRightCorners = topRightCorners[ x ] + start_x, topRightCorners[ y ] + start_y
    #topRightCorners[ y ] = topRightCorners[ y ] + start_y
    bottomRightCorners = bottomRightCorners[ x ] + start_x, bottomRightCorners[ y ] + start_y
    #bottomRightCorners[ y ] = bottomRightCorners[ y ] + topRightCorners[ y ]
    coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
    return coordinateOfQRCode


def findFirstQRCode( sourceImageFileName ):
        symbols = scanImageForQRCode( sourceImageFileName, 0 )
        coordinateOfQRCode = []
        if ( len( symbols) > 0 ):
                sym = symbols[ 0 ]
                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in sym.locator]
                coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
                print( sym.data )

        return coordinateOfQRCode


def findAllQRCodeOnColumn( imageWorker, start_x, start_y ):
#ОЖИДАЕМ ЧТО ИЗОБРАЖЕНИЕ УЖЕ ПЕРЕВЕНУТО
#БЕРЕМ В КАЧЕСТЕ ЭТАЛОНА РАЗМЕР БОЛЬШОГО КОДА
#УЧИТЫВАЕМ ЧТО ЛИСТ ПОД НАКЛОНОМ
    height = int( height_big_qr_code )
    width = width_big_qr_code
    source_image = imageWorker.getPILImageCopy()
    
    step_y = int ( height / 10 )
    heghtOfImage = source_image.height

    qrCodeCount = 0

    topLeftCorners = -1
    bottomLeftCorners = -1
    bottomRightCorners = -1
    topRightCorners = -1
    data = ""
    listOfQRCodes = []
    dataList = []
    c = 0
    while( 1 ):
        img_with_possible_qr = crop_image( source_image, 0, start_x, start_y, width, height )
        
        
        imageWorker.copyPILImageToOpenCV(img_with_possible_qr)
        symbols = []
        for i in range( 1, 10 ):
            threshold = 200 - i * 10
            threshImg = doThreshold( imageWorker.getOpenCVImage(),\
                                     threshold )
            imageWorker.copyOpenCVImageToPIL( threshImg )
            symbols = scanImageForQRCode( imageWorker.getPILImage(), 0 )
            if ( len( symbols ) > 0 ):
                    break
        if len( symbols ) > 0:
            #получаем значение y кода на исходном изображении
            for sym in symbols: 
                coordinateOfQRCode = [item for item in sym.locator]
                dataList.append( sym.data )
                coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                #img_with_crop = crop_image( source_image, 0, bottomLeftCorners[x], topLeftCorners[y], bottomRightCorners[x] - bottomLeftCorners[x], bottomLeftCorners[y] - topLeftCorners[y] )
                #img_with_crop.save( FOLDER_QR_CODES +
                #                    PREFIX_FOR_SMALL_QR_CODE_IMAGE_FILENAME +
                #                    str( c ) +
                #                    ".png")
                start_y = bottomLeftCorners[ y ]
                listOfQRCodes.append( sym )
                listOfQRCodes.append( coordinateOfQRCode )
            #print('i find small qr')
            #print( str( c ) + fileNameImgWithPossibleQr )
            continue
        
        start_y = start_y + step_y
        #print( "start_x", start_x, "start_y", start_y)
        #count_y = count_y + 1

        if ( ( start_y + height ) >= heghtOfImage ):
            #print("finished find qr codes"
            break

    return listOfQRCodes, dataList

#ДЛЯ ИСХОДНОГО ИЗОБРАЖЕНИЯ
def getX_PixelsFromSourceImageByQRCode( widthOfQRCode, value ):

        HEIGHT_OF_BIG_QR_CODE
        return round( ( value ) * ( widthOfQRCode / WIDTH_OF_BIG_QR_CODE ) ) + RESERVE_PIXELS_VALUE

def getY_PixelsFromSourceImageByQRCode( heightOfQRCode, value ):

        return round( ( value  ) * ( heightOfQRCode / HEIGHT_OF_BIG_QR_CODE ) ) + RESERVE_PIXELS_VALUE


def detectFormByBigQRCode( image, coordinatesOfCode ):

        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinatesOfCode
        heightOfQRCode = bottomLeftCorners[ Y ] - topLeftCorners[ Y ]
        widthOfQRCode = topRightCorners[ X ] - topLeftCorners[ X ]

        #ПИКСЕЛИ
        PIXELS_DISTANCE_TO_FORM_LEFT_SIDE = getX_PixelsFromSourceImageByQRCode( widthOfQRCode, DISTANCE_TO_FORM_LEFT_SIDE )
        PIXELS_DISTANCE_TO_FORM_TOP_SIDE = getY_PixelsFromSourceImageByQRCode( heightOfQRCode, DISTANCE_TO_FORM_TOP_SIDE )
        #print( PIXELS_DISTANCE_TO_FORM_TOP_SIDE, PIXELS_DISTANCE_TO_FORM_LEFT_SIDE )
        posX = topLeftCorners[ X ] - PIXELS_DISTANCE_TO_FORM_LEFT_SIDE
        posY = topLeftCorners[ Y ] - PIXELS_DISTANCE_TO_FORM_TOP_SIDE

        # поправляем координаты для кода
        topLeftCorners = topLeftCorners[X] - posX, topLeftCorners[Y] - posY
        topRightCorners = topRightCorners[ X ] - posX, topRightCorners[ Y ]  - posY
        bottomLeftCorners = bottomLeftCorners[ X ] - posX, bottomLeftCorners[ Y ] - posY
        bottomRightCorners = bottomRightCorners[ X ] - posX, bottomRightCorners[ Y ] - posY
        
        PIXELS_DISTANCE_TO_FORM_BOTTOM_SIDE = getY_PixelsFromSourceImageByQRCode( heightOfQRCode, DISTANCE_TO_FORM_BOTTOM_SIDE )
        height = heightOfQRCode + PIXELS_DISTANCE_TO_FORM_TOP_SIDE + PIXELS_DISTANCE_TO_FORM_BOTTOM_SIDE 

        PIXELS_DISTANCE_TO_FORM_RIGHT_SIDE = getX_PixelsFromSourceImageByQRCode( widthOfQRCode, DISTANCE_TO_FORM_RIGHT_SIDE )
        width = widthOfQRCode + PIXELS_DISTANCE_TO_FORM_RIGHT_SIDE + PIXELS_DISTANCE_TO_FORM_LEFT_SIDE

        #image.save("crop_test1.jpg")
        print( posX,posY,width,height)
        img = crop_image( image, 0, posX, posY, width, height )
        #img.save("crop_test.jpg")

        newCoordinatesOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
        return img, newCoordinatesOfQRCode


def getOpenCVImageFromPIL( imagePIL ):
        self.imageOpenCV = cv2.cvtColor( numpy.array( self.imagePIL ), cv2.COLOR_RGB2BGR)

def getPILImageFromOpenCV( imageOpenCV ):
        height, width = imageOpenCV.shape[:2]
        size = width, height
        imagePIL = Image.fromstring( flagConvert, size, imageOpenCV.tostring())
        return imagePIL


def bigQRCodeIsNotOnTheFirstPage( coordinateOfQRCode,\
                                  image):

    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
   
    widthOfQRCode = topRightCorners[ X ] - topLeftCorners[ X ]
    PIXELS_DISTANCE_TO_LEFT_SIDE = getX_PixelsFromSourceImageByQRCode( widthOfQRCode, DISTANCE_FROM_CENTER_BIG_QR_CODE_TO_RIGHT_SIDE_BIG_QR_CODE )
   
    topLeftCorners = topLeftCorners[ x ] + PIXELS_DISTANCE_TO_LEFT_SIDE,\
                     topLeftCorners[ y ]
    bottomLeftCorners = bottomLeftCorners[x ] + PIXELS_DISTANCE_TO_LEFT_SIDE, \
                        bottomLeftCorners[ y ]
    topRightCorners = topRightCorners[ x ] + PIXELS_DISTANCE_TO_LEFT_SIDE, \
                      topRightCorners[ y ]
    bottomRightCorners = bottomRightCorners[ x ] + PIXELS_DISTANCE_TO_LEFT_SIDE, \
                         bottomRightCorners[ y ]
    coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
    return coordinateOfQRCode

# Проверка - является ли код БОЛЬШИМ.
# У Большого кода сперва следует прописной символ b (код по ASCII 98)
def isItBigQRCode( symData ):

        
        return symData[0] == BIG_QR_CODE_SYMBOL_PREFIX

# Пробуем отыскать большой QR код на листе СРАЗУ.
# Это в разы ускорит процесс
def tryToFindBigQRCodeInFullForm( imageWorker ):


        res = 0
        coordinateOfQRCode = []
        symData = ""
        for i in range( 1, 10 ):
                        #print( "HI!")

                        threshold = 200 - i * 10
                        #cv2.imwrite( "JUST_FOR_TEST_OPENCV.jpg", imageWorker.getOpenCVImage())
                        threshImg = doThreshold( imageWorker.getOpenCVImage(),\
                                                 threshold )
                        imageWorker.copyOpenCVImageToPIL( threshImg )
                        i#mageWorker.getPILImage().save("JUST_FOR_TEST_1.jpg")
                        symbols = scanImageForQRCode( imageWorker.getPILImage(), 0 )
                        if ( len( symbols ) > 0 ):
                                #print(len(symbols))
                                k = 0
                                for sym in symbols:
                                        sym = symbols[ k ]
                                        k = k + 1
                                        symData = sym.data
                                        # ЭТО БОЛЬШОЙ КОД
                                        #print( 'YES!')
                                        #print(symData)
                                        if ( isItBigQRCode( symData ) ):
                                                #print('QR CODE ALREASDY!')
                                                FAST_ALGORITHM_IS_WORKED = 1
                                                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in sym.locator]
                                                coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
                                                res = 1
                                                return res, coordinateOfQRCode, symData
                                        
                        
        return res, coordinateOfQRCode, symData

        
#ВОЗВРАЩАЕТ ЛИСТ
# rotatedStatus - был ли повернут лист
def thirdVariantOfAlgorithm( imageWorker, \
                             rotatedStatus = IS_NOT_ROTATED ):

        global height_big_qr_code 
        global width_big_qr_code

        sourceImage = imageWorker.getPILImageCopy()
        height_big_qr_code = getX_PixelsByMillimeters( sourceImage, \
                                                       HEIGHT_OF_BIG_QR_CODE )
        width_big_qr_code = getY_PixelsByMillimeters( sourceImage, \
                                                      WIDTH_OF_BIG_QR_CODE )
        #ДИАГОНАЛЬ
        diagonal = math.sqrt( height_big_qr_code ** 2 + width_big_qr_code ** 2 )
        height_big_qr_code = diagonal
        width_big_qr_code = diagonal

        #im = Image.open( sourceImageFileName ).convert('L')
        width_source_image = sourceImage.width
        height_source_mage = sourceImage.height
        start_x = int( width_source_image - width_big_qr_code)
        start_y = 0
        symData = ""
        coordinateOfQRCode = []

        imageWorker.copyPILImageToOpenCV(sourceImage)

        # Пытаемся сперва СРАЗУ обнаружить коды
        res, coordinateOfQRCode, symData = tryToFindBigQRCodeInFullForm( imageWorker )
        
        while( 1 ):
                if ( res == 0 ):
                        crop_img = crop_image( sourceImage,\
                                               0,\
                                               start_x,\
                                               start_y,\
                                               width_big_qr_code,\
                                               height_big_qr_code )
                        imageWorker.copyPILImageToOpenCV(crop_img)
                        for i in range( 1, 10 ):
                                #print( "HI!")

                                threshold = 200 - i * 10
                                #cv2.imwrite( "JUST_FOR_TEST_OPENCV.jpg", imageWorker.getOpenCVImage())
                                threshImg = doThreshold( imageWorker.getOpenCVImage(),\
                                                         threshold )
                                imageWorker.copyOpenCVImageToPIL( threshImg )
                                #imageWorker.getPILImage().save("JUST_FOR_TEST_1.jpg")
                                symbols = scanImageForQRCode( imageWorker.getPILImage(), 0 )
                                if ( len( symbols ) > 0 ):
                                        sym = symbols[ 0 ]
                                        symData = sym.data
                                        if ( isItBigQRCode( symData ) ):
                                                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in sym.locator]
                                                coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
                                                break
                #coordinateOfQRCode = findFirstQRCode( crop_img )
                if ( len( coordinateOfQRCode ) != 0 ):
                            #print("start_x, y", start_x, start_y)

                            bigQRCodeData = BigQRCodeData()
                            #print( symData )
                            bigQRCodeData.parseDataFromStr( str(symData) )

                                
                            if ( res == 0 ):
                                    coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )

                            topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                            img_with_crop = crop_image( sourceImage, \
                                                        0, \
                                                        bottomLeftCorners[x], \
                                                        topLeftCorners[y], \
                                                        bottomRightCorners[x] - bottomLeftCorners[x], \
                                                        bottomLeftCorners[y] - topLeftCorners[y] )
                            #img_with_crop.save( FOLDER_QR_CODES +
                            #                    IMAGE_FILENAME_BIG_QR_CODE )
                            formRotation = FormRotation( sourceImage, \
                                                         coordinateOfQRCode )
                            result, imageRotated, rotationValue = formRotation.start()

                            #сохранение попытки поворота
                            #imageRotated.save("tryToRotate.png")
                            #print( result )
                            #Если был поворот
                            if ( result == 1 and rotatedStatus == IS_NOT_ROTATED ):

                                    #image = imageRotated
                                    #coordinateOfQRCode, sourceImage, symData = thirdVariantOfAlgorithm( image)
                                    #widthOfQRCode = bottomRightCorners[x] - bottomLeftCorners[x]
                                    #heightOfQRCode = bottomLeftCorners[y] - topLeftCorners[y]
                                    
                                    xCenterPoint = int ( width_source_image / 2 );
                                    
                                    yCenterPoint = int ( height_source_mage / 2 )
                                    #print( "Before getNewPointByCoordinates", coordinateOfQRCode )

                                    # если сработал быстрый алгоритм можно быстро отыскать НОВЫЕ координаты.
                                    #print(FAST_ALGORITHM_IS_WORKED)
                                    if ( FAST_ALGORITHM_IS_WORKED == 0 ):
                                            #print("FAST")
                                            imageWorker.copyPILImageToOpenCV(imageRotated)
                                            res, coordinateOfQRCode, symData = tryToFindBigQRCodeInFullForm( imageWorker )
                                            
                                    else:
                                            #print("NOT FAST")
                                            coordinateOfQRCode = getNewPointByCoordinatesOfCode( coordinateOfQRCode,\
                                                                                                 xCenterPoint,\
                                                                                                 yCenterPoint,\
                                                                                                 rotationValue )
                                    #print( "After getNewPointByCoordinates", coordinateOfQRCode )
                                                                    

                            #print ( coordinateOfQRCode )
                            # Это код НЕ первой страницы?
                            if ( bigQRCodeData.getPageBit() == str(0) ):
                                # корректируем его координаты.
                                #print("CORRECT BIG CODE")
                                coordinateOfQRCode = bigQRCodeIsNotOnTheFirstPage( coordinateOfQRCode,\
                                                                                   imageRotated )
                            #print ( "NEW",coordinateOfQRCode )
                            
                            sourceImage, coordinateOfQRCode = detectFormByBigQRCode( imageRotated,\
                                                                                     coordinateOfQRCode )

                            #print( coordinateOfQRCode )
                            #crop_img.save("big_qr_code.jpg")
                            break

                start_x = start_x - int( width_big_qr_code / 10 )
                #Как только дошли до левого края страницы
                if ( start_x < 0 ):
                        start_x =  int( width_source_image - width_big_qr_code )
                        start_y = start_y + int( height_big_qr_code / 10 )
                if ( ( start_y + int( height_big_qr_code ) )  >= height_source_mage ):
                        break

        imageWorker.setPILImage( sourceImage )
        return coordinateOfQRCode, imageWorker, symData


def getNewPoint( xStartPoint,\
                 yStartPoint,\
                 xCenterPoint,\
                 yCenterPoint,\
                 currentAngle ):

        original = abs(currentAngle)
        #print( currentAngle )
        currentAngle = abs(currentAngle)
        if ( currentAngle > 0 ):
                currentAngle = math.radians( currentAngle )                     
                xEndPoint = int ( xStartPoint * math.cos( currentAngle ) -\
                            yStartPoint * math.sin( currentAngle ) )
                yEndPoint = int( xStartPoint * math.sin( currentAngle ) +\
                            yStartPoint * math.cos( currentAngle ) )
        else:
                currentAngle = math.radians( currentAngle )                     
                xEndPoint = int ( xStartPoint * math.cos( currentAngle ) +\
                            yStartPoint * math.sin( currentAngle ) )
                yEndPoint = int( -xStartPoint * math.sin( currentAngle ) +\
                            yStartPoint * math.cos( currentAngle ) )
                

        #print ( xCenterPoint )
        #print( xEndPoint )

        #45.5 = ПЕЧАЛЬ БЕДА
        xEndPoint = int( xEndPoint + int ( original ) * 45.5  )
        #yEndPoint = int( yEndPoint + yCenterPoint )

        return xEndPoint, yEndPoint

def getNewPointByCoordinatesOfCode( coordinateOfQRCode,\
                                    xCenterPoint,\
                                    yCenterPoint,\
                                    currentAngle ):

        #if ( currentAngle < 0 ):
        #        currentAngle = 360 - abs(currentAngle)
                
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                                    
        topLeftCorners = getNewPoint( topLeftCorners[ X ],\
                                      topLeftCorners[ Y ],\
                                      xCenterPoint,\
                                      yCenterPoint,\
                                      currentAngle )
        topRightCorners = getNewPoint( topRightCorners[ X ],\
                                       topRightCorners[ Y ],\
                                       xCenterPoint,\
                                       yCenterPoint,\
                                       currentAngle )
        bottomLeftCorners = getNewPoint( bottomLeftCorners[ X ],\
                                         bottomLeftCorners[ Y ],\
                                         xCenterPoint,\
                                         yCenterPoint,\
                                         currentAngle )
        bottomRightCorners= getNewPoint( bottomRightCorners[ X ],\
                                         bottomRightCorners[ Y ],\
                                         xCenterPoint,\
                                         yCenterPoint,\
                                         currentAngle )
        
        coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
  
        return coordinateOfQRCode

#НА ОСНОВАНИИ ЛИСТА (в изображении только лист)
def getX_PixelsByMillimeters( imagePIL, value,  ):

        return round( ( value ) * ( imagePIL.width / WIDTH_FORM ) ) + RESERVE_PIXELS_VALUE

#НА ОСНОВАНИИ ЛИСТА (в изображении только лист)
def getY_PixelsByMillimeters( imagePIL, value ):

        return round( ( value  ) * ( imagePIL.height / HEIGHT_FORM ) ) + RESERVE_PIXELS_VALUE


def getCellImage( imageWithCells, sourceImage, startPos ):
                
        start_x = getX_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX )
        start_y = getY_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX )
        width = getX_PixelsByMillimeters( sourceImage, WIDTH_OF_CELL ) - start_x
        height = getY_PixelsByMillimeters( sourceImage, HEIGHT_OF_CELL ) - start_y
        cell = crop_image( imageWithCells, 0, startPos + start_x, start_y, width, height )
        return cell

def getImageWithCells( imagePIL, QRCode ):

        #БЕРУ НЕМНОГО БОЛЬШЕ ПО X
        #считаем расстояние до первой ячейки
        distance_to_first_cell = getX_PixelsByMillimeters( imagePIL, DISTANCE_FROM_CODE_TO_CELL ) + \
                                 getX_PixelsByMillimeters( imagePIL, DISTANCE_BETWEEN_CELLS ) * 2 + \
                                 getX_PixelsByMillimeters( imagePIL, WIDTH_OF_CELL) * 3
        #print( "distance to first cell = ", distance_to_first_cell )
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = QRCode
        #print( topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners )
        
        start_x =  0
        
        start_y = topLeftCorners[y]
        width = bottomLeftCorners[ x ]
        height = bottomLeftCorners[y] - topLeftCorners[y] + \
                 (int) ( ( bottomLeftCorners[y] - topLeftCorners[y] ) / 2 )#ЗАПАС
        #print( start_x, start_y, width, getPixelValueBySizeInInch(HEIGHT_OF_CELL_INCH) )
        img_with_crop = crop_image( imagePIL, 0, start_x, start_y, width, height )
        return img_with_crop
        #doThreshold( imageWithCells, imageWithCells )


def doThreshold( sourceImage, threshold = 200):
    
    gray = cv2.cvtColor( sourceImage, cv2.COLOR_BGR2GRAY )
    retval, bin = cv2.threshold( gray, threshold, 255, cv2.THRESH_BINARY)
    return bin


def doAdaptiveThreshold( sourceImage, \
                         adaptiveThresholdParam = cv2.ADAPTIVE_THRESH_GAUSSIAN_C ):
        img =  sourceImage
        gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        img = cv2.medianBlur( gray,5 )
        th = cv2.adaptiveThreshold( img, \
                                255, \
                                adaptiveThresholdParam,\
                                cv2.THRESH_BINARY_INV, \
                                11, \
                                2 )
        return th


def getIndexOfMax( value, squares ):
        for i in range(0, len( squares ) ):
                if ( squares[i][0][0][0] == value ):
                        return i
        return -1

def sortSquares( squares ):

        squaresRes = []
        #print( squares[0][0][0][0], squares[1][0][0][0], squares[2][0][0][0] )
        listSquares = [ squares[0][0][0][0], squares[1][0][0][0], squares[2][0][0][0] ]
        value = min(listSquares)
        squaresRes.append( squares[ getIndexOfMax( value, squares ) ] )
        listSquares.remove( value )

        value = min(listSquares)
        squaresRes.append( squares[ getIndexOfMax( value, squares ) ] )
        listSquares.remove( value )
        
        squaresRes.append( squares[ getIndexOfMax( listSquares[0] , squares ) ] )
        
        return squaresRes

def find_squares( imgWithCells, \
                  imageWorker,\
                  thresholdValue, \
                  thresholdMod = ADAPTIVE_MOD):
#возвращает контуры найденных МЕТОК

    #gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    imageWorker.copyPILImageToOpenCV(imgWithCells)
    res = doAdaptiveThreshold( imageWorker.getOpenCVImage() )
    imageWorker.setOpenCVImage( res )
    #cv2.imwrite("ADAPTIVE_THRESH.jpg", res)
    #image = cv2.imread( threshImg, cv2.CV_8UC1 )
    #cv2.imshow('squares', image )
    #cv2.waitKey(0)
    #removeNoisy( imageWithCellsFileName,imageWithCellsFileName )
    image = imageWorker.getOpenCVImage()
    #cv2.imwrite("ADAPTIVE_THRESH.jpg", image)

    #СОХРАНЯЕМ. т.к. findContours ПОРТИТ исходное перпедаваемое изображение (image в нашем случае).
    originalAdaptiveImage = image.copy()
    #cv2.imshow('squares', image )
    #cv2.waitKey(0)
    bin, contours, hierarchy = cv2.findContours( image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imwrite("ADAPTIVE_THRESH.jpg", originalAdaptiveImage)
    squares = []
    count = 0
    for cnt in contours:
        rect = cv2.boundingRect( cnt )
        #print (rect)
        #print ( rect )
        k = ( rect[2] + 0.0) / rect[3]
        #print ( cv2.contourArea(cnt) )
        if ( 0.7 < k and k < 1.8  and cv2.contourArea(cnt) > 2500 ):
            count = count + 1
            #print("k = ", k)
            #print( "x = ", rect[0], "y = ", rect[1])
            #print("contourArea = ", cv2.contourArea(cnt))
            #print( cnt )
            squares.append( cnt )
    #print( len( contours ) )
    #print ( len( squares )  )
    if ( len( squares ) == 3 ):
        #imageForContoursDraw = cv2.imread( imageWithCellsFileName )
        #cv2.drawContours( imageForContoursDraw, contours, -1, (0, 255, 0), 3 )
        #cv2.imshow('squares', imageForContoursDraw )
        #cv2.waitKey(0)
        squares = sortSquares( squares )


    # НЕ ЗАБЫВАЕМ ВОЗВРАЩАТЬ ЧЕРНО-БЕЛОЕ ИЗОБРАЖЕНИЕ
    return squares, originalAdaptiveImage
    

#проверка заполненности ячейки
def checkImageOnMark( img, mod = 0 ):

    result = 0
    #print( input_image)
    #img = Image.open( input_image )
    pixels = list( img.getdata() )

    black = 0
    white = 0
    for pixel in pixels:
        if  mod == 0 :
                #for i in pixel:
                if pixel == 255:
                        white = white + 1
                else:
                        black = black + 1
        else:
                if pixel == 255:
                        white = white + 1
                else:
                        black = black + 1  
    #print( white / ( black + white ) * 100 )
    if ( ( white / ( black + white ) * 100 ) >= 3):
        result = 1
    return result

def getImageByContour( contour, imageWithCells ):

        x,y,w,h = cv2.boundingRect( contour  )
        crop = imageWithCells[y:y+h,x:x+w]
        return crop

#возврат 1 - если успешно оберезали ячейку
# вовзврат 0 - если неуспешно
def prepareCell( imagePIL, sourceImage ):
        start_x = getX_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX ) * 2
        start_y = getY_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX ) * 2
        width = imagePIL.width - start_x * 2 - RESERVE_PIXELS_VALUE
        height = imagePIL.height - start_y * 2 - RESERVE_PIXELS_VALUE
        cell = crop_image( imagePIL, 0, start_x, start_y, width, height )
        return cell



#если большой код не нашелся
def startScan( sourceImage,\
               idToken ):

        imageWorker = ImageWorker( sourceImage,\
                                   PIL_IMAGE )
        
        # Заносим информацию о том, что распознавание НАЧАЛОСЬ
        # также, создаем объект scanResult, который будет содержать в себе
        # всю информацию по результату распознавания

        try:
                tokenFileWorker = TokenFileWorker()
                scanResult = ScanResult()
                scanResult.setIdToken( idToken )
                scanResult.setStatus( IN_PROGRESS )
                tokenFileWorker.setScanResult( scanResult )



                #ВАРИАНТ ГРУБОЙ СИЛЫ
                coordinateOfQRCode, imageWorker, symData = thirdVariantOfAlgorithm( imageWorker )

                #sourceImage.save( "check1.png" )
                #coordinateOfQRCode, sourceImage, symData = thirdVariantOfAlgorithm( sourceImage, \
                #                                                                    WAS_ROTATED )
                sourceImage = imageWorker.getPILImage()
                #sourceImage.save( "OnlyForm.jpg" )
                
                #sourceImage.save( "check.png" )
                if ( len( coordinateOfQRCode ) > 0 ):
                        
                        bootomLeftCorners = coordinateOfQRCode[ 1 ]
                        bottomRightCorners = coordinateOfQRCode[ 2 ]
                        start_x = bottomRightCorners[ x ] - int ( ( bottomRightCorners[ x ] - bootomLeftCorners[ x ]  ) / 2 )
                        start_y = bottomRightCorners[ y ]
                        listOfQRCodes, dataList = findAllQRCodeOnColumn( imageWorker, start_x, start_y )

                        
                        if ( len ( listOfQRCodes ) > 0 ):
                                #выводим и записываем большой QR
                                bigQRCodeData = BigQRCodeData()
                                bigQRCodeData.parseDataFromStr( str( symData ) )
                                scanResult.setBigQRCodeData( bigQRCodeData )
                                sys.stdout.write( str( symData ) + "\n" )
                                #print( symData )
                                #начинаем вырезать ячейки по каждому коду

                                for i in range( 0, int( len( listOfQRCodes) / 2 ) ):
                                        
                                        #print( dataList[ i ] )
                                        smallQRCodeData = SmallQRCodeData()
                                        smallQRCodeData.setData( str( dataList[ i ] ) )
                                        sys.stdout.write( str( dataList[ i ] ) + "\n" ) 
                                        listOfResult = []
                                        #fileNameImageWithCells = FOLDER_IMAGE_WITH_CELLS + \
                                        #                         str( i ) + \
                                        #                         IMAGE_FILENAME_IMAGE_WITH_CELLS
                        
                                        imgWithCells = getImageWithCells( sourceImage, listOfQRCodes[ i * 2 + 1 ] )
                                        thresholdValue = 200
                                        squares, imgWithCellsThresh = find_squares( imgWithCells, imageWorker, thresholdValue )
                                        #imageWorker.copyOpenCVImageToPIL(imgWithCellsThresh, 1)
                                        #imgWithCells = imgWithCellsThresh
                                        #cv2.imwrite("NEW_image_with_cells.jpg", imgWithCells)
                                        countOfCells = len ( squares )
                                        #3 ячейки!
                                        cells = []
                                        listOfResult = []
                                        if ( countOfCells == 3 ):
                                                #изображения с ячейками
                                                for k in range ( 0, countOfCells):

                                                        #imgWithCells.save("image_with_cells.jpg")
                                                        #imageWorker.copyPILImageToOpenCV(imgWithCells)
                                                        cellImage = getImageByContour( squares[ k ],\
                                                                                       imgWithCellsThresh)

                                                        #cv2.imwrite("test_cell.jpg", cellImage)
                                                        
                                                        imageWorker.copyOpenCVImageToPIL( cellImage, 1 )
                                                        image = prepareCell( imageWorker.getPILImage(), \
                                                                             sourceImage )
                                                        cells.append( image )
                                                        #image.save( cellFileName )
                                                        #image.save("cell.jpg")
                                                        listOfResult.append( checkImageOnMark( image ) )
                                                sys.stdout.write( str( listOfResult ) + "\n" )
                                                #print( listOfResult )
                                        else:
                                                # Если вдруг, по результатам алгоритма поиска ячеек (по контурам),
                                                # их оказалось БОЛЕЕ 3-ех. Тогда вырезаем ВРУЧНУЮ (опираясь на
                                                # ИЗВЕСТНОЕ расстояние между ячейками в пикселях.

                                                cellsDetector = CellsDetector( sourceImage,\
                                                                               imgWithCells )
                                               
                                                firstCellImg, secondCellImg, thirdCellImg  = cellsDetector.start()
                                                listOfResult.append( checkImageOnMark( firstCellImg ) )
                                                listOfResult.append( checkImageOnMark( secondCellImg ) )
                                                listOfResult.append( checkImageOnMark( thirdCellImg ) )
                                                sys.stdout.write( str( listOfResult ) + "\n" )
                                        smallQRCodeData.setResultList( listOfResult )
                                        scanResult.addSmallQRCodeData( smallQRCodeData )
                                        
                                scanResult.setStatus( SUCCESS )
                                        
                                        
                        else:
                                #print( "there is no something about small QR codes :(");
                                sys.stderr.write( str( SMALL_QR_CODES_ARE_NOT_HERE ) )
                                scanResult.setStatus( FILED_SMALL_QR_CODE )
                else:
                        sys.stderr.write( str( FORM_NOT_FOUNDED ) )
                        # Не найден большой QR код.
                        scanResult.setStatus( FAILED_BIG_QR_CODE )
                        
        except BaseException:
                
                scanResult.setStatus( FAILED )

        return scanResult
