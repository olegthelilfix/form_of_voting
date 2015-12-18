import cv2
import PIL
from FormRotation import *
from BaseEnums import *
from PIL import Image
from PIL.ExifTags import TAGS
import libzbar as zbar
from numpy import arccos
from scipy import ndimage
from scipy import misc
import math
import sys

counter = 0

COUNT_OF_QR_CODES_ON_PAGE = 3


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


def findAllQRCodeOnColumn( source_image, start_x, start_y ):
#ОЖИДАЕМ ЧТО ИЗОБРАЖЕНИЕ УЖЕ ПЕРЕВЕНУТО
#БЕРЕМ В КАЧЕСТЕ ЭТАЛОНА РАЗМЕР БОЛЬШОГО КОДА
#УЧИТЫВАЕМ ЧТО ЛИСТ ПОД НАКЛОНОМ
    height = int( height_big_qr_code )
    width = width_big_qr_code
    fileNameImgWithPossibleQr = "img_with_possible_qr.png"
    
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
        
        c = c + 1
        img_with_possible_qr.save( "possible qr codes/" + str(c) + fileNameImgWithPossibleQr)
        imgFileName = "image_with_possible_qr.png"
        imgFileNameWithThreshold = "threshold_" + imgFileName
        img_with_possible_qr.save( imgFileName )
        symbols = []
        for i in range( 1, 10 ):
            threshold = 200 - i * 10
            doThreshold( imgFileName, imgFileNameWithThreshold, threshold )
            symbols = scanImageForQRCode( imgFileNameWithThreshold, 1 )
            if ( len( symbols ) > 0 ):
                    break
        if len( symbols ) > 0:
            #получаем значение y кода на исходном изображении
            for sym in symbols: 
                coordinateOfQRCode = [item for item in sym.locator]
                dataList.append( sym.data )
                coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                img_with_crop = crop_image( source_image, 0, bottomLeftCorners[x], topLeftCorners[y], bottomRightCorners[x] - bottomLeftCorners[x], bottomLeftCorners[y] - topLeftCorners[y] )
                img_with_crop.save("qr codes/small_qr_code_" + str( c ) + ".png")
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
        
        PIXELS_DISTANCE_TO_FORM_BOTTOM_SIDE = getY_PixelsFromSourceImageByQRCode( heightOfQRCode, DISTANCE_TO_FORM_BOTTOM_SIDE )
        height = heightOfQRCode + PIXELS_DISTANCE_TO_FORM_TOP_SIDE + PIXELS_DISTANCE_TO_FORM_BOTTOM_SIDE 

        PIXELS_DISTANCE_TO_FORM_RIGHT_SIDE = getX_PixelsFromSourceImageByQRCode( widthOfQRCode, DISTANCE_TO_FORM_RIGHT_SIDE )
        width = widthOfQRCode + PIXELS_DISTANCE_TO_FORM_RIGHT_SIDE + PIXELS_DISTANCE_TO_FORM_LEFT_SIDE
        img = crop_image( image, 0, posX, posY, width, height )
        return img


def getOpenCVImageFromPIL( imagePIL ):
        self.imageOpenCV = cv2.cvtColor( numpy.array( self.imagePIL ), cv2.COLOR_RGB2BGR)

def getPILImageFromOpenCV( imageOpenCV ):
        height, width = imageOpenCV.shape[:2]
        size = width, height
        imagePIL = Image.fromstring( flagConvert, size, imageOpenCV.tostring())
        return imagePIL


#ВОЗВРАЩАЕТ ЛИСТ
def thirdVariantOfAlgorithm( sourceImage ):

        global height_big_qr_code 
        global width_big_qr_code

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
        start_x = 0
        start_y = 0
        symData = ""
        coordinateOfQRCode = []
        while( 1 ):
                #threshold!!!!
                #исходный файл
                possibleQRCodeFileName = "possible big qr codes/big_code.png"
                #изображение
                threshPossibleQRCodeFileName = "possible big qr codes/thresh_big_code.png"
                crop_img = crop_image( sourceImage, 0, start_x, start_y, width_big_qr_code, height_big_qr_code )
                crop_img.save( possibleQRCodeFileName )
                for i in range( 1, 10 ):
                        threshold = 200 - i * 10
                        doThreshold( possibleQRCodeFileName, threshPossibleQRCodeFileName, threshold )
                        symbols = scanImageForQRCode( threshPossibleQRCodeFileName, 1 )
                        if ( len( symbols ) > 0 ):
                                sym = symbols[ 0 ]
                                symData = sym.data
                                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in sym.locator]
                                coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
                                break      
                #coordinateOfQRCode = findFirstQRCode( crop_img )
                if ( len( coordinateOfQRCode ) != 0 ):
                            coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                            topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                            img_with_crop = crop_image( sourceImage, 0, bottomLeftCorners[x], topLeftCorners[y], bottomRightCorners[x] - bottomLeftCorners[x], bottomLeftCorners[y] - topLeftCorners[y] )
                            img_with_crop.save( "qr codes/big qr code.png" )
                            formRotation = FormRotation( sourceImage, \
                                                         coordinateOfQRCode )
                            result, image = formRotation.start()
                            #Если был поворот - снова ищем код, т.к. координаты сменились
                            if ( result == 1 ):
                                    coordinateOfQRCode, sourceImage, symData = thirdVariantOfAlgorithm( image )
                                    break
                            sourceImage = detectFormByBigQRCode( image, coordinateOfQRCode )
                            #print( coordinateOfQRCode )
                            #crop_img.save("big_qr_code.jpg")
                            break

                start_x = start_x + int( width_big_qr_code / 10 ) 
                if ( ( start_x + int( width_big_qr_code )  ) >= width_source_image ):
                            start_x = 0
                            start_y = start_y + int( height_big_qr_code / 10 )
                if ( ( start_y + int( height_big_qr_code ) )  >= height_source_mage ):
                            break

        return coordinateOfQRCode, sourceImage, symData


#ДЛЯ ЛИСТА
def getX_PixelsByMillimeters( imagePIL, value,  ):

        return round( ( value ) * ( imagePIL.width / WIDTH_FORM ) ) + RESERVE_PIXELS_VALUE

#ДЛЯ ЛИСТА
def getY_PixelsByMillimeters( imagePIL, value ):

        return round( ( value  ) * ( imagePIL.height / HEIGHT_FORM ) ) + RESERVE_PIXELS_VALUE


def getCellImage( imageWithCells, sourceImage, startPos ):
                
        start_x = getX_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX )
        start_y = getY_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX )
        width = getX_PixelsByMillimeters( sourceImage, WIDTH_OF_CELL ) - start_x
        height = getY_PixelsByMillimeters( sourceImage, HEIGHT_OF_CELL ) - start_y
        cell = crop_image( imageWithCells, 0, startPos + start_x, start_y, width, height )
        return cell

def getImageWithCells( imagePIL, QRCode, fileNameImageWithCells ):

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
        height = bottomLeftCorners[y] - topLeftCorners[y] #ЗАПАС
        height = height + ( height / 2 )
        #print( start_x, start_y, width, getPixelValueBySizeInInch(HEIGHT_OF_CELL_INCH) )
        img_with_crop = crop_image( imagePIL, 0, start_x, start_y, width, height )
        img_with_crop.save( fileNameImageWithCells )
        #doThreshold( imageWithCells, imageWithCells )


def doThreshold( sourceImageFileName, destinationImageFileName, threshold = 200):
    
    img = cv2.imread( sourceImageFileName )
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    retval, bin = cv2.threshold( gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite( destinationImageFileName, bin )


def doAdaptiveThreshold( sourceImageFileName, \
                         destinationImageFileName,\
                         adaptiveThresholdParam = cv2.ADAPTIVE_THRESH_GAUSSIAN_C ):
        img = cv2.imread( sourceImageFileName )
        gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        img = cv2.medianBlur( gray,5 )
        th = cv2.adaptiveThreshold( img, \
                                255, \
                                adaptiveThresholdParam,\
                                cv2.THRESH_BINARY_INV, \
                                11, \
                                2 )
        cv2.imwrite( destinationImageFileName, th )


def getIndexOfMax( value, squares ):
        for i in range(0, len( squares ) ):
                if ( squares[i][0][0][0] == value ):
                        return i
        return -1

def sortSquares( squares ):

        squaresRes = []
        listSquares = [ squares[0][0][0][0], squares[1][0][0][0], squares[2][0][0][0] ]
        value = min(listSquares)
        squaresRes.append( squares[ getIndexOfMax( value, squares ) ] )
        listSquares.remove( value )

        value = min(listSquares)
        squaresRes.append( squares[ getIndexOfMax( value, squares ) ] )
        listSquares.remove( value )
        
        squaresRes.append( squares[ getIndexOfMax( listSquares[0] , squares ) ] )
        
        return squaresRes

def removeNoisy( sourceImageFileName, destinationImageFileName ):

    image = cv2.imread( sourceImageFileName )
    image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    blur = cv2.GaussianBlur( image, (5,5), 0 )
    ret3,th = cv2.threshold( blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU )
    cv2.imwrite( destinationImageFileName, th )

def find_squares(imageWithCellsFileName, thresholdValue ):
#возвращает контуры найденных МЕТОК

    #gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    threshImg = "thresh_" + imageWithCellsFileName
    doAdaptiveThreshold( imageWithCellsFileName, imageWithCellsFileName)
    #image = cv2.imread( threshImg, cv2.CV_8UC1 )
    #cv2.imshow('squares', image )
    #cv2.waitKey(0)
    #removeNoisy( imageWithCellsFileName,imageWithCellsFileName )
    image = cv2.imread( imageWithCellsFileName, cv2.CV_8UC1 )
    #cv2.imshow('squares', image )
    #cv2.waitKey(0)
    bin, contours, hierarchy = cv2.findContours( image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    count = 0
    for cnt in contours:
        rect = cv2.boundingRect( cnt )
        #print (rect)
        #print ( rect )
        k = ( rect[2] + 0.0) / rect[3]
        #rint ( cv2.contourArea(cnt) )
        if ( 0.7 < k and k < 1.8  and cv2.contourArea(cnt) > 2500 ):
            count = count + 1
            #print("k = ", k)
            #print( "x = ", rect[0], "y = ", rect[1])
            #print("contourArea = ", cv2.contourArea(cnt))
            #print( cnt )
            squares.append( cnt )
    #print( len( contours ) )
    #print ( len( squares )  )
    if ( len( contours ) == 3 ):
        #imageForContoursDraw = cv2.imread( imageWithCellsFileName )
        #cv2.drawContours( imageForContoursDraw, contours, -1, (0, 255, 0), 3 )
        #cv2.imshow('squares', imageForContoursDraw )
        #cv2.waitKey(0)
        squares = sortSquares( squares )
    return squares


def getImageByContour( contour, imageWithCells, outputImageFileName ):

        x,y,w,h = cv2.boundingRect( contour  )
        crop = imageWithCells[y:y+h,x:x+w]
        cv2.imwrite( outputImageFileName, crop)       

#проверка заполненности ячейки
def checkImageOnMark( input_image ):

    result = 0
    #print( input_image)
    img = Image.open( input_image )
    pixels = list( img.getdata() )
    black = 0
    white = 0
    for pixel in pixels:
        for i in pixel:
                if i == 255:
                        white = white + 1
                else:
                        black = black + 1
    #print( white / ( black + white ) * 100 )
    if ( ( white / ( black + white ) * 100 ) >= 3):
        result = 1
    return result

def getImageByContour( contour, imageWithCells, outputImageFileName ):

        x,y,w,h = cv2.boundingRect( contour  )
        imageWithCells = cv2.imread( imageWithCells )
        crop = imageWithCells[y:y+h,x:x+w]
        cv2.imwrite( outputImageFileName, crop)

#возврат 1 - если успешно оберезали ячейку
# вовзврат 0 - если неуспешно
def prepareCell( imagePIL, sourceImage ):
        start_x = getX_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX )
        start_y = getY_PixelsByMillimeters( sourceImage, WIDTH_OF_BOX)
        width = imagePIL.width - start_x - RESERVE_PIXELS_VALUE
        height = imagePIL.height - start_y - RESERVE_PIXELS_VALUE
        cell = crop_image( imagePIL, 0, start_x, start_y, width, height )
        return cell


if __name__ == "__main__":

        if ( len( sys.argv ) == 1 ):
                fileName = "forms/test_5.png"
        else:
                fileName = sys.argv[ 1 ]
        sourceImage = Image.open( fileName )
        #ВАРИАНТ ГРУБОЙ СИЛЫ
        coordinateOfQRCode, sourceImage, symData = thirdVariantOfAlgorithm( sourceImage )
        #sourceImage.save( "check1.png" )
        coordinateOfQRCode, sourceImage, symData = thirdVariantOfAlgorithm( sourceImage )
        print( symData )
        #sourceImage.save( "check.png" )
        if ( len( coordinateOfQRCode ) > 0 ):
                
                bootomLeftCorners = coordinateOfQRCode[ 1 ]
                bottomRightCorners = coordinateOfQRCode[ 2 ]
                start_x = bottomRightCorners[ x ] - int ( ( bottomRightCorners[ x ] - bootomLeftCorners[ x ]  ) / 2 )
                start_y = bottomRightCorners[ y ]
                listOfQRCodes, dataList = findAllQRCodeOnColumn( sourceImage, start_x, start_y )
                if ( len ( listOfQRCodes ) > 0 ):
                        #начинаем вырезать ячейки по каждому коду

                        for i in range( 0, int( len( listOfQRCodes) / 2 ) ):
                                print( dataList[ i ] )
                                listOfResult = []
                                fileNameImageWithCells = "image with cells/" + str( i ) + "image_with_cells.png"
                                img = sourceImage.copy()
                                getImageWithCells( img, listOfQRCodes[ i * 2 + 1 ], fileNameImageWithCells )
                                thresholdValue = 200
                                squares = find_squares( fileNameImageWithCells, thresholdValue )
                                
                                countOfCells = len ( squares)
                                #3 ячейки!
                                if ( countOfCells == 3 ):
                                        #изображения с ячейками
                                        cells = []
                                        listOfResult = []
                                        for k in range ( 0, countOfCells):
                                                cellFileName = "cells/cell_" + str( i ) + \
                                                               " _ " + str( k ) + ".png"
                                                getImageByContour( squares[ k ],\
                                                                   fileNameImageWithCells, \
                                                                   cellFileName )
                                                image = Image.open( cellFileName )
                                                image = prepareCell( image, sourceImage )
                                                cells.append( image )
                                                image.save( cellFileName )
                                                listOfResult.append( checkImageOnMark( cellFileName ) )
                                        print( listOfResult )
                                else:
                                       print( "не найдены ячейки :(") 
                                
                else:
                        print( "there is no something about small QR codes :(");
        else:
                print( "there is no BIG QR code :(")
