#Версия бланка 1.1
# Находит qr коды методом "грубой силы".
# вырезает ячейки расположенные напротив каждого найденного кода
# вырезает каждую ячейку
# реализован анализ каждой ячейки на заполнение, но не вызывается явно.
# также, сейчас, для упрощения на стадии тестирования, вырезаются ячейки только первого кода (маленького)

import numpy as np
import cv2
import PIL
from PIL import Image
from numpy import arccos
from scipy import ndimage
from scipy import misc
import libzbar as zbar
import math
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2

######
ROTATED_ON_180 = 1
ROTATED_TO_NORMAL = 2
WAS_NOT_ROTATED = 3

#ДЛЯ ПОИСКА МЕТКИ
WIDTH_OF_LABEL = 20
HEIGHT_OF_LABEL = 20

LIMIT_POSITION_ON_HEIGHT_FOR_LABEL = 100

STEP_X_FOR_FIND_LABEL = WIDTH_OF_LABEL
STEP_Y_FOR_FIND_LABEL = HEIGHT_OF_LABEL

TRESHOLD_FOR_LABEL = 0.7;
#стоит замедлить шаг поиска
MINIMAL_TRESHOLD_FOR_LABEL = 0.3
####################

#ДЛЯ ЯЧЕЕК 
NUM_OF_FIRST_CELL = 0
NUM_OF_SECOND_CELL = 1
NUM_OF_THIRD_CELL = 2

TRESHOLD = 12.4

WIDTH_OF_CELL = 64
WIDTH_BETWEEN_CELLS = 117
HEIGHT_OF_CELL = 59

WIDTH_OF_TABLE = 4


WIDTH_FROM_QR_CODE_TO_CELL = 98
########################

#отступить немного в сторону, чтобы ухватить всю область с кодами
STEP_SIZE_ON_X_POSITION = 5

SIZE = 762, 1080

ALLOWABLE_ROTATION = 10
COUNT_OF_CELLS = 3
FACTOR = 100
y = 1
x = 0


###########################
HEIGHT_OF_BIG_QR_CODE = 100
WIDTH_OF_BIG_QR_CODE = 100

MAX_HEIGHT_OF_BIG_QR_CODE = 0
MAX_WIDTH_OF_BIG_QR_CODE  = 0


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
#возвращает контуры найденных МЕТОК
# мне скорее всего имеет смысл возвращать параметры из rect

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    cv2.imshow('gray', gray)
    #threshold(gray, gray, 100, 255, THRESH_BINARY)
    #gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    retval, bin = cv2.threshold( gray, 150, 255, cv2.THRESH_BINARY_INV)
    #bin = cv2.bitwise_not( bin )
    cv2.imshow('bin', bin)
    #cv2.findContours(gray, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE)
    bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    print ( len( contours) )
    count = 0
    for cnt in contours:
        rect = cv2.boundingRect( cnt )
        #print (rect)
        #print ( rect )
        k = ( rect[2] + 0.0) / rect[3]
        #print( " k = ", k, "contour = ", cv2.contourArea(cnt), "\n" )
        #rint ( cv2.contourArea(cnt) )
        if ( 1 < k and k < 1.8 and cv2.contourArea(cnt) > 200 and cv2.contourArea(cnt) < 400 ):
            count = count + 1
            print("k = ", k)
            print( "x = ", rect[0], "y = ", rect[1])
            print("contourArea = ", cv2.contourArea(cnt))
            squares.append( cnt )
            #if ( count == 5 ):
             #   break
    """


    
    squares = []
    img = cv2.GaussianBlur(img, (5, 5), 0)
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    #print ( max_cos )
                    if max_cos < 0.1:
                         squares.append(cnt)
"""                      
                    
    return squares

def resizeImage( sourceFileName, destinationFileName, size ):
    #fileName = 'blank1.png'
    im = Image.open( sourceFileName )
    #im.save( fileName, dpi = ( 100,100) )
    im_resized = im.resize( size, Image.ANTIALIAS)
    im_resized.save( destinationFileName )
    return im_resized


def getParametersForBigQRCode( symbols ):
    topLeftCorners = -1
    bottomLeftCorners = - 1
    bottomRightCorners = -1
    topRightCorners = -1
    for symbol in symbols:
        if symbol.type == "ZBAR_QRCODE":
            #66 = B
             if symbol.data[ 0 ] == 66:
                 topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in symbol.locator]
                 break
    return topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners


#находим ВСЕ коды в "столбце"
def findAllQRCodeOnColumn( source_image, start_x ):
#ОЖИДАЕМ ЧТО ИЗОБРАЖЕНИЕ УЖЕ ПЕРЕВЕНУТО
#БЕРЕМ В КАЧЕСТЕ ЭТАЛОНА РАЗМЕР БОЛЬШОГО КОДА
    height = HEIGHT_OF_BIG_QR_CODE
    width = WIDTH_OF_BIG_QR_CODE + 40
    fileNameImgWithPossibleQr = "img_with_possible_qr.png"
    start_y = 0
    start_x = start_x - 10
    step_y = 1
    im = Image.open( source_image )
    heghtOfImage = im.height
    #max_count_y = int( ( im.height / step_y ) - ( start_y / step_y ) )
    #print( "max_count_y", max_count_y)
    im.close()
    #count_y = 0
    topLeftCorners = -1
    bottomLeftCorners = -1
    bottomRightCorners = -1
    topRightCorners = -1
    data = ""
    listOfQRCodes = []
    while( 1 ):
        img_with_possible_qr = crop_image( source_image, 1, start_x, start_y, width, height )
        #img_with_possible_qr.save( str( start_y ) + fileNameImgWithPossibleQr )
        img_with_possible_qr.save(fileNameImgWithPossibleQr)
        symbols = scanImageForQRCode( fileNameImgWithPossibleQr )
        if len( symbols ):
            #получаем значение y кода на исходном изображении
            for sym in symbols:
                coordinateOfQRCode = [item for item in sym.locator]
                coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                start_y = int ( start_y + ( height ) )
                listOfQRCodes.append( sym )
                listOfQRCodes.append( coordinateOfQRCode )
                #listOfQRCodes.append( topLeftCorners )
                #listOfQRCodes.append( bottomLeftCorners )
                #listOfQRCodes.append( bottomRightCorners )
                #listOfQRCodes.append( topRightCorners )
            print(' I FIND QR!!!!')
            print( str( start_y ) + fileNameImgWithPossibleQr )
        
        start_y = start_y + step_y
        #print( "start_x", start_x, "start_y", start_y)
        #count_y = count_y + 1

        if ( ( start_y + height ) >= heghtOfImage ):
            print("finished find qr codes")
            print( len( listOfQRCodes ) )
            break

    return listOfQRCodes
        
        
def scanImageForQRCode( sourceImage, isItFileName = 1 ):
    if ( isItFileName == 1 ):
        pil = Image.open( sourceImage ).convert('L')
    else:
        pil = sourceImage
    symbols = zbar.Image.from_im( pil ).scan()
    return symbols

#heightOfCell - высота ячейки
#widthOfCell - ширина ячейки
#numberOfCell - номер ячейки по счету, которую собираемся брать
#imageWithCells - изображения с ячейками по линии с QR кодом
def getCellValue( heightOfCell, widthOfCell, widthBetweenCells, numberOfCell, imageWithCells ):
    
    cropBefore = numberOfCell * widthBetweenCells
    #numberOfCell = numberOfCell - 1
    cropBefore = cropBefore + numberOfCell * widthOfCell
    cropBefore = cropBefore + WIDTH_OF_TABLE
    print("cropbefore=", cropBefore)
    img_with_crop = crop_image( imageWithCells, 1, cropBefore, 0, widthOfCell - WIDTH_OF_TABLE - 2, heightOfCell )
    return img_with_crop

	
def isThatImageReversed( topLeftCorners, bottomLeftCorners ):
    result = 0
    #topLeftCorners[ y ], bottomLeftCorners[ y ]
    if topLeftCorners[ y ] > bottomLeftCorners[ y ]:
        result = 1
    return result

#добавить проверку на чистые 90
def getRotateValue( topLeftCorners, bottomLeftCorners, topRightCorners ):
    
    apexA = topLeftCorners
    apexC = bottomLeftCorners
    apexB = [ bottomLeftCorners[ x ], topRightCorners[ y ] ]
    betta = 0
    #AB
    sideC = math.sqrt( ( apexC[ x ] - apexA[ x ] ) ** 2 + ( apexC[ y ] - apexA[ y ] ) ** 2)
    #BC 
    sideA = math.sqrt( ( apexC[ x ] - apexB[ x ] ) ** 2 + ( apexC[ y ] - apexB[ y ] ) ** 2)
    #AC
    
    sideB = math.sqrt( ( apexB[ x ] - apexA[ x ] ) ** 2 + ( apexB[ y ] - apexA[ y ] ) ** 2)
    if sideC + sideA > sideB and sideC + sideB > sideA and sideB + sideA > sideC:
            
        aRad = math.acos( ( sideB * sideB + sideC * sideC - sideA * sideA ) / ( 2 * sideB * sideC ) )
        bRad = math.acos( ( sideA ** 2 + sideC ** 2 - sideB ** 2 ) / ( 2 * sideA * sideC ) )
        alpha = aRad * 180 / 3.14
        betta = bRad * 180 / 3.14
        gamma = 180 - alpha - betta
        
        if ( topLeftCorners[ x ] < bottomLeftCorners[ x ] ):
            betta = -betta
    return betta

def crop_image( input_image, isItFileName, start_x, start_y, width, height ):
   
    if ( isItFileName == 1):
        input_img = Image.open(input_image)
    else:
        input_img = input_image
    box = (start_x, start_y, start_x + width, start_y + height)
    #print("BOX = ", box)
    output_img = input_img.crop( box )
    return output_img
def isAllowableRotation( topLeftCorners, bottomLeftCorners ):

    result = 0
    currentRotation = abs( topLeftCorners[ x ] - bottomLeftCorners[ x ] )
    if currentRotation <= ALLOWABLE_RATION :
        result = 1
    return result


def getRotationStatusOfImage( topLeftCorners, bottomLeftCorners ):

    if ( topLeftCorners[ y ] ) < ( bottomLeftCorners[ y ] ) :
        result = getNecessaryRotationOfImage( topLeftCorners, bottomLeftCorners )
    else:
        result = DEFAULT_ROTATION

    return result
        


def getNecessaryRotationOfImage( topLeftCorners, bottomLeftCorners ):

    if isAllowableRotation( topLeftCorners, bottomLeftCorners )  :
        result = NORMAL_ROTATION_STATUS
    else:
        if ( topLeftCorners[ x ] ) > ( bottomLeftCorners[ x ] ):
            result = LEFT_ROTATION
        else:
            result = RIGHT_ROTATION

    return result

def getBalckAndWhiteAndSizeValueForImage( input_image ):
    
    pixels = list( input_image.getdata() )
    black = 1
    white = 0
    for pixel in pixels:
        S = pixel[ 0 ] + pixel[ 1 ] + pixel [ 2 ]
        if ( S > ( ( ( 255 + FACTOR ) / 2) * 3 ) ):
            white = white + 1        
        else:
            black = black + 1 
    lenOfPixels = len( pixels ) 

    return black, white, lenOfPixels

def checkImageOnMark( input_image ):

    result = 0
    pixels = list( input_image.getdata() )
    print ( len( pixels ) )
    black = 1
    white = 0
    for pixel in pixels:

        if pixel == 0:
            black = black + 1
        else:
            white = white + 1
    print ( "white = ", white)
    print ( "black = ", black)
    if ( len ( pixels ) ) / black  <= TRESHOLD:
        result = 1
    return result
    
#функция возраващает список из элементов следующей структуры:
# [A, B]
# А - порядковый номер ячейки(1, 2, 3)
# B - статус заполнения (1/0)
def detectEachCell( fileName ):
     resultList = []
     img = cv2.imread( fileName )
     height, width, channels = img.shape
     print ("width = ", width)
     width = int(width / COUNT_OF_CELLS)
     print ("width = ", width)
     #squares = find_squares( img )
     #cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
     #cv2.imshow('squares', img)
     #cv2.waitKey(0)
     currentCell = 0
     start_x = 0
     start_y = 0
     for currentCell in range(0, COUNT_OF_CELLS):
         #print( "sqaure = ", square )
         #topLeftCorners = square[ 0 ]
         #bottomLeftCorners = square[ 1 ]
         #bottomRightCorners = square[ 3 ]
         #topRightCorners = square[ 1 ]
         #width = abs( bottomRightCorners[ x ] - bottomLeftCorners[ x ] )
         #height = abs( bottomRightCorners[ y ] - topRightCorners[ y ] )
         
         print( "topLeftCorners[ x ] = ", start_x)
         print( "topLeftCorners[ y ] = ", start_y )
         print( "width = ", width )
         print( "height = ", height )
         img_with_crop = crop_image( fileName, start_x, start_y, width, height )
         start_x = start_x + width
         img_with_crop.save( "cell" + str( currentCell ) + ".png" )
         resultList.append( checkImageOnMark( img_with_crop ) )
         if ( currentCell == 3 ):
             break
     return resultList

def findFirstQRCode( sourceImageFileName ):
    symbols = scanImageForQRCode( sourceImageFileName, 0 )
    coordinateOfQRCode = []
    if ( len( symbols) > 0 ):
        sym = symbols[ 0 ]
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in sym.locator]
        coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners

    return coordinateOfQRCode


#корректирует координаты найденного кода в соответствии с его реальным расположением на
#изображении
def correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y ):
    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
    topLeftCorners = topLeftCorners[ x ] + start_x, topLeftCorners[ y ] + start_y
    bottomLeftCorners = bottomLeftCorners[x ] + start_x, start_y + bottomLeftCorners[ y ]
    topRightCorners = topRightCorners[ x ] + start_x, topRightCorners[ y ] + start_y
    bottomRightCorners = bottomRightCorners[ x ] + start_x, bottomRightCorners[ y ] + start_y
    coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
    return coordinateOfQRCode

def thirdVariantOfAlgorithm( sourceImageFileName ):
    d = int( math.sqrt(HEIGHT_OF_BIG_QR_CODE ** 2 + WIDTH_OF_BIG_QR_CODE ** 2) )
    MAX_HEIGHT_OF_BIG_QR_CODE = MAX_WIDTH_OF_BIG_QR_CODE = d

    height = MAX_HEIGHT_OF_BIG_QR_CODE
    width = MAX_WIDTH_OF_BIG_QR_CODE

    im = Image.open( sourceImageFileName ).convert('L')
    max_width = im.width
    max_height = im.height
    start_x = 0
    start_y = height
    coordinateOfQRCode = []
    while( 1 ):
        crop_img = crop_image( im, 0, start_x, start_y, width, height )
        coordinateOfQRCode = findFirstQRCode( crop_img )
        if ( len( coordinateOfQRCode ) != 0 ):
            print( coordinateOfQRCode )
            print( "start_x", start_x, "start_y", start_y)
            coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
            topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
            print( coordinateOfQRCode )
            img_with_crop = crop_image( sourceImageFileName, 1, bottomLeftCorners[x], topLeftCorners[y], bottomRightCorners[x] - bottomLeftCorners[x], bottomLeftCorners[y] - topLeftCorners[y] )
            print( coordinateOfQRCode )
            print( "QR code" )
            crop_img.save("First QR code.jpg")
            break

        start_x = start_x + 10
        if ( ( start_x + width ) >= max_width ):
            start_x = 0
            start_y = start_y + 10
        if ( ( start_y + height )  >= max_height ):
            print( "that's all :( ")
            break

    return coordinateOfQRCode


def doThreshold( sourceImageFileName, destinationImageFileName, threshold = 200):
    img = cv2.imread( sourceImageFileName )
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    retval, bin = cv2.threshold( gray, threshold, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite( destinationImageFileName, bin )
    
def isItBigQRCode( symbol ):
    if symbol.data[ 0 ] == 66:
        return 1
    return 0
    
#функция возвращает 3 состояния:
# - было повернуто на 180гр (ROTATED_ON_180)
# - было повернуто до нормального состояния( ROTATED_TO_NORMAL)
# - не было повернуто, все нормально (WAS_NOT_ROTATED)
def rotateImageByCoordinateOfQRCode( coordinateOfQRCode, sourceImageFileName ):
    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
    if isThatImageReversed( topLeftCorners, bottomLeftCorners ):
        image = misc.imread( sourceImageFileName )
        rotated = ndimage.rotate( image, 180 )
        misc.imsave( sourceImageFileName, rotated )
        return ROTATED_ON_180
    print(  "hey = ",topLeftCorners, bottomLeftCorners, topRightCorners )
    rotateValue = getRotateValue( topLeftCorners, bottomLeftCorners, topRightCorners )
    print("rotateValue=", rotateValue)
    if abs(rotateValue) > 0:
        #дублирующийся код!!!!
        rotateValue = rotateValue + 2.4
        image = misc.imread( sourceImageFileName )
        rotated = ndimage.rotate( image,  rotateValue, reshape = False )
        misc.imsave( sourceImageFileName, rotated )
        return ROTATED_TO_NORMAL
   
    return WAS_NOT_ROTATED

def analyzingCellsForEachQRCode( listOfQRCodes, sourceImageFileName ):
    result = []
    size = len( listOfQRCodes )
    imageWithCells = "image_with_cells.png"
    imageCell = "image_cell_"
    j = 0
    while( j < size ):
        if ( isItBigQRCode( listOfQRCodes[j] ) == 0 ):
            #print (symbol )
            print( listOfQRCodes[j])
            print( listOfQRCodes[j + 1])
            subResult = []
            #print ( symbol )
            #topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in symbol.locator]
            distance_to_first_cell = WIDTH_FROM_QR_CODE_TO_CELL + WIDTH_BETWEEN_CELLS * 2 + WIDTH_OF_CELL * 3
            topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = listOfQRCodes[j + 1]
            print( bottomLeftCorners )

            start_x =  bottomLeftCorners[x] - distance_to_first_cell
            print( "start_x = ", start_x)
            start_y = bottomLeftCorners[y] - HEIGHT_OF_CELL
            print( "start_y = ", start_y)
            width = distance_to_first_cell - WIDTH_FROM_QR_CODE_TO_CELL
            print( "width = ", width )
            print( "height", HEIGHT_OF_CELL )
            subResult.append( listOfQRCodes[j] )
            #print( listOfQRCodes[j] )
            img_with_crop = crop_image( sourceImageFileName, 1, start_x, start_y, width, HEIGHT_OF_CELL )
            img_with_crop.save( imageWithCells )
            doThreshold( imageWithCells, imageWithCells )
            for NUM_CELL in ( NUM_OF_FIRST_CELL, NUM_OF_SECOND_CELL, NUM_OF_THIRD_CELL ):
                img_with_cell = getCellValue( HEIGHT_OF_CELL, WIDTH_OF_CELL, WIDTH_BETWEEN_CELLS, NUM_CELL, imageWithCells )
                img_with_cell.save( imageCell + str(NUM_CELL) + ".png" )
                subResult.append( checkImageOnMark( img_with_cell ) )
                result.append( subResult )
            break
        else:
            print( "BIG QR CODE IS HERE!!!!")
        j = j + 2
    print( result )

def getImageWithCells( sourceImageFileName, QRCode ):
    imageWithCells = "image_with_cells.png"
    distance_to_first_cell = WIDTH_FROM_QR_CODE_TO_CELL + WIDTH_BETWEEN_CELLS * 2 + WIDTH_OF_CELL * 3
    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = QRCode
    print( topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners )
    start_x =  bottomLeftCorners[x] - distance_to_first_cell
    start_y = bottomLeftCorners[y] - HEIGHT_OF_CELL
    width = distance_to_first_cell
    img_with_crop = crop_image( sourceImageFileName, 1, start_x, start_y, width, HEIGHT_OF_CELL )
    img_with_crop.save( imageWithCells )
    doThreshold( imageWithCells, imageWithCells )


#ПЕРЕДЕЛАТЬ МЕТОД
def repeatWhileBlackInRow( pixels, x, y, width ):
    counter = 0
    i = 0
    for i in range(x, width):
       counter = counter + 1
       if ( pixels[ i, y ] == 255 ):
           return i, counter
    return i, counter
	
#ПЕРЕДЕЛАТЬ МЕТОД
def repeatWhileBlackInColumn( pixels, x, y ):
    counter = 0
    j = 0
    for j in range(y, 0, -1):
        counter = counter + 1
        if ( pixels[ x, j ] == 255 ):
            return j, counter
    return abs( j ), counter
	
#ПЕРЕДЕЛАТЬ МЕТОД
def repeatWhileWhiteInRow( pixels, x, y, width ):
    counter = 0
    i = 0
    for i in range(x, width):
       counter = counter + 1
       if ( pixels[ i, y ] == 0 ):
           return ( i, counter )
    return i, counter
	
#ПЕРЕДЕЛАТЬ МЕТОД
def repeatWhileWhiteInColumn( pixels, x, y ):
    counter = 0
    j = 0
    for j in range(y, 0, -1):
        counter = counter + 1
        if ( pixels[ x, j ] == 0 ):
            return j, counter
    return abs( j ),counter

#ПЕРЕДЕЛАТЬ МЕТОД
def whitePixelCountOnThisLine( pixels, x, y, width ):
    print ("x = ", x)
    print( "y=", y)
    print( "width = ", width)
    count = 0
    for i in range( x, width ):
        print( pixels[ i, y ] )
        if ( pixels[ i, y ] == 255 ):
            count = count + 1
    return count

def getEachCellFromImageWithCells( sourceImageFileName ):
    input_image = Image.open( sourceImageFileName ).convert('L')
    width = input_image.width
    height = input_image.height
    height = int( height / 2 )
    result = 0
    pixels = input_image.load()#pixels = list( input_image.getdata() )
    #print ( len( pixels ) )
    
    black = 1
    white = 0
    watchStep = 10
    whitePixelIsOn = 0
    #pixels = pixels[ height:(height + width) ]
    whitePixelIsFinded = 0
    startPosForWhitePixel = 0
    blackPixelIsFinded = 0
    print( "width = ", width )
    print( "height", height )

    start_x_l = 0
    for i in range( 1, 4 ):

        print("---------------------------------")
        print("шли до левой рамки")
        start_x_l, counter = repeatWhileBlackInRow( pixels, start_x_l, height, width )
        print( "counter = ", counter )
        #огибаем левую рамку
        print("обогнули левую рамку:")
        start_x_l, counter= repeatWhileWhiteInRow( pixels, start_x_l, height, width ) 
        print( "counter = ", counter )
        #поиск правой рамки
        print("прошли до правой рамки, отступив до этого от левой рамки в ширину ячейки")
        start_x_r, counter = repeatWhileBlackInRow( pixels, start_x_l + WIDTH_OF_CELL - 15, height, width )
        print( "counter = ", counter )
        #поиск нижней рамки
        h, counter = repeatWhileBlackInColumn(pixels, start_x_r - 5, input_image.height - 1) 
        #spaceFromDown - завел для того, чтобы указывать нижнюю границу для среза
        spaceFromDown = input_image.height - 1
        print( "первоначально нижняя граница рамки = ",spaceFromDown)
        print("мы пытались найти нижнюю рамку и вот что вышло")
        print("h", h, "counter", counter)
        if ( counter <= int( HEIGHT_OF_CELL / 2 ) ):
            spaceFromDown = spaceFromDown - counter
            #мы нашли нижнюю рамку, надо преодолеть ее.
            #не забываем отступать немного влево по Х
            #так как мы на правой рамке по X  с прошлого поиска (start_x_r)
            h, counter = repeatWhileWhiteInColumn(pixels, start_x_r - 5, h)
            spaceFromDown = spaceFromDown - counter
            print("мы измеряли нижнюю рамку")
            print("h", h, "counter", counter)
            #вот теперь уже точно верхняя рамка
            h, counter = repeatWhileBlackInColumn(pixels, start_x_r - 5, h)
            print("мы искали верхнюю рамку и прошли:")
            print("h", h, "counter", counter)
            print("сейчас будем вырезать рамку до низа = ", spaceFromDown)
            print( "но сперва посмотрим, какое количество белых пикселей на этом уровне")
            while(  whitePixelCountOnThisLine( pixels, start_x_l + 1, spaceFromDown - 1, start_x_r - 5 ) > 3 ):
                spaceFromDown = spaceFromDown - 1
            print ( "обрезали нижнюю границу = ", spaceFromDown )
        #start_y = input_image.height - WIDTH_OF_TABLE - h
        #от spaceFromDown - 1, т.к. срез идет включительно
        #отняли единичку от ширины т.к. мы остановились на белом поле
        img_with_crop = crop_image( sourceImageFileName, 1, start_x_l + 1, h + 1, start_x_r - start_x_l - 4, spaceFromDown - 10)
        img_with_crop.save("HELLO" + str(i) + ".png")
        #огибаем правую рамку
        start_x_l, counter= repeatWhileWhiteInRow( pixels, start_x_r, height, width ) 
        print( "counter = ", counter )
        print("огибаем правую рамку")
"""
    for i in range(1, width):
        pixel = pixels[ i, height ]
        print( pixel )
        print ( i )
        if pixel == 255:
            whitePixelIsFinded = 1
            startPosForWhitePixel = i
        if ( whitePixelIsFinded == 1 and pixel == 0 ):
            whitePixelIsFinded = 0
            start_y = input_image.height - HEIGHT_OF_CELL
            start_x = i + 5
            img_with_crop = crop_image( sourceImageFileName, 1, start_x, start_y, WIDTH_OF_CELL, HEIGHT_OF_CELL )
            img_with_crop.save("HELLO.png")
            print( "HI!!!")
            return
"""
            
                    
            
            
if __name__ == '__main__':

    sourceImageFileName = "001_1"
    resizedFileName = "resized_" + sourceImageFileName + ".png"
    im_resized = resizeImage( sourceImageFileName + ".jpg", resizedFileName, SIZE )
    
    fileNameOfQRBigCode = "BIGQRCODE.png"
    imageWithCells = "image_with_cells.png"
    #ВАРИАНТ ГРУБОЙ СИЛЫ
    coordinateOfQRCode = thirdVariantOfAlgorithm( resizedFileName )
    resultOfRotation = rotateImageByCoordinateOfQRCode( coordinateOfQRCode, resizedFileName )
    print( "result of rotation", resultOfRotation  )
    if ( resultOfRotation  == ROTATED_ON_180 ):
        print( "!NNOOO!" )
        coordinateOfQRCode = thirdVariantOfAlgorithm( resizedFileName )
        rotateImageByCoordinateOfQRCode( coordinateOfQRCode, resizedFileName )

    topLeftCorners = coordinateOfQRCode[0]
    start_x =  topLeftCorners[ x ]
    print( topLeftCorners )
    listOfQRCodes = findAllQRCodeOnColumn( resizedFileName, start_x )
    print( len( listOfQRCodes ) )
    print( listOfQRCodes )
    getImageWithCells( resizedFileName, listOfQRCodes[ 3 ] )
    getEachCellFromImageWithCells( imageWithCells )
    
    #analyzingCellsForEachQRCode( listOfQRCodes, resizedFileName )

