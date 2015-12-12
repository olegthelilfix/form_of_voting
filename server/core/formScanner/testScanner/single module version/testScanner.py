import cv2
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import libzbar as zbar
from numpy import arccos
from scipy import ndimage
from scipy import misc
import math

INCH = 2.54

#САНТИМЕТРЫ
WIDHT_OF_BIG_QR_CODE_CENTIMETER = 2.3
HEIGHT_OF_BIG_QR_CODE_CENTIMETER = 2.3

#ДЮЙМЫ
WIDHT_OF_BIG_QR_CODE_INCH = WIDHT_OF_BIG_QR_CODE_CENTIMETER / INCH 
HEIGHT_OF_BIG_QR_CODE_INCH = HEIGHT_OF_BIG_QR_CODE_CENTIMETER / INCH 

counter = 0

COUNT_OF_QR_CODES_ON_PAGE = 3

######
ROTATED_ON_180 = 1
ROTATED_TO_NORMAL = 2
WAS_NOT_ROTATED = 3

TRESHOLD_ON_MARKED_STATUS = 0.086

y = 1
x = 0

height_big_qr_code = 0
width_big_qr_code = 0


WIDTH_FROM_QR_CODE_TO_CELL_CENTIMETER = 2.7
WIDTH_BETWEEN_CELLS_CENTIMETER = 3.2
WIDTH_OF_CELL_CENTIMETER = 1.7
HEIGHT_OF_CELL_CENTIMETER = 1

WIDTH_FROM_QR_CODE_TO_CELL_INCH = WIDTH_FROM_QR_CODE_TO_CELL_CENTIMETER / INCH 
WIDTH_BETWEEN_CELLS_INCH = WIDTH_BETWEEN_CELLS_CENTIMETER / INCH
WIDTH_OF_CELL_INCH = WIDTH_OF_CELL_CENTIMETER / INCH 
HEIGHT_OF_CELL_INCH = HEIGHT_OF_CELL_CENTIMETER / INCH 

DPI = 0

def getDPIValue( img ):
        info = img._getexif()
        exifObj = {}
        if info != None:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exifObj[decoded] = value
        print( exifObj['XResolution'] )
        return exifObj['XResolution'][0]/exifObj['XResolution'][1]


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

        return coordinateOfQRCode


def resizeImage2( sourceImage, size ):
        size = sourceImage.width * 2, sourceImage.height * 2
        im_resized = sourceImage.resize( size, Image.BILINEAR)
        return im_resized

def divValueBy( value, divValue ):
        value = int(value / divValue)
        return value


def convertCoordinatesOfCodeToBack( coordinateOfQRCode ):
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode

        topLeftCorners = divValueBy( topLeftCorners[ x ], 2) ,divValueBy( topLeftCorners[ y ], 2)
        
        bottomLeftCorners = divValueBy( bottomLeftCorners[ x ], 2), divValueBy( bottomLeftCorners[ y ], 2)
        
        bottomRightCorners = divValueBy( bottomRightCorners[ x ], 2), divValueBy( bottomRightCorners[ y ], 2)
        
        topRightCorners = divValueBy( topRightCorners[ x ], 2), divValueBy( topRightCorners[ y ], 2)
  
        coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
        return coordinateOfQRCode


def findAllQRCodeOnColumn( source_image, start_x, start_y ):
#ОЖИДАЕМ ЧТО ИЗОБРАЖЕНИЕ УЖЕ ПЕРЕВЕНУТО
#БЕРЕМ В КАЧЕСТЕ ЭТАЛОНА РАЗМЕР БОЛЬШОГО КОДА
    height = int(height_big_qr_code )
    width = width_big_qr_code 
    print( "width of big qr code = ", width )
    print( "height of big qr code = ", height )
    fileNameImgWithPossibleQr = "img_with_possible_qr.png"
    
    step_y = int ( height / 10 )
    heghtOfImage = source_image.height

    topLeftCorners = -1
    bottomLeftCorners = -1
    bottomRightCorners = -1
    topRightCorners = -1
    data = ""
    listOfQRCodes = []
    c = 0
    while( 1 ):
        img_with_possible_qr = crop_image( source_image, 0, start_x, start_y, width, height )
        img_with_possible_qr = resizeImage2( img_with_possible_qr, ( img_with_possible_qr.width * 2, img_with_possible_qr.height * 2) )
        #img_with_possible_qr.save( str( start_y ) + fileNameImgWithPossibleQr )
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
                #так как мы увеличивали изображение - переводим координаты обратно
                coordinateOfQRCode =  convertCoordinatesOfCodeToBack(coordinateOfQRCode) 
                coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                img_with_crop = crop_image( source_image, 0, bottomLeftCorners[x], topLeftCorners[y], bottomRightCorners[x] - bottomLeftCorners[x], bottomLeftCorners[y] - topLeftCorners[y] )
                img_with_crop.save("qr codes/small_qr_code_" + str( c ) + ".png")
                start_y = bottomLeftCorners[ y ]
                listOfQRCodes.append( sym )
                listOfQRCodes.append( coordinateOfQRCode )
                #listOfQRCodes.append( topLeftCorners )
                #listOfQRCodes.append( bottomLeftCorners )
                #listOfQRCodes.append( bottomRightCorners )
                #listOfQRCodes.append( topRightCorners )
            print('i find small qr')
            print( str( c ) + fileNameImgWithPossibleQr )
        
        start_y = start_y + step_y
        #print( "start_x", start_x, "start_y", start_y)
        #count_y = count_y + 1

        if ( ( start_y + height ) >= heghtOfImage ):
            print("finished find qr codes")
            print( len( listOfQRCodes ) / 2 )
            break

    return listOfQRCodes

def thirdVariantOfAlgorithm( sourceImage ):
#изображение может быть повернуто на 45 гр.
#считаем диагналь QR кода
        #d = int( math.sqrt(HEIGHT_OF_BIG_QR_CODE ** 2 + WIDTH_OF_BIG_QR_CODE ** 2) )
        #MAX_HEIGHT_OF_BIG_QR_CODE = MAX_WIDTH_OF_BIG_QR_CODE = d
        global DPI
        DPI = getDPIValue( sourceImage)
        global height_big_qr_code 
        global width_big_qr_code
        height_big_qr_code = getPixelValueBySizeInInch( HEIGHT_OF_BIG_QR_CODE_INCH )
        width_big_qr_code = getPixelValueBySizeInInch( WIDHT_OF_BIG_QR_CODE_INCH )

        #im = Image.open( sourceImageFileName ).convert('L')
        width_source_image = sourceImage.width
        height_source_mage = sourceImage.height
        start_x = 0
        start_y = 0
        coordinateOfQRCode = []
        while( 1 ):
                crop_img = crop_image( sourceImage, 0, start_x, start_y, width_big_qr_code, height_big_qr_code )
                coordinateOfQRCode = findFirstQRCode( crop_img )
                if ( len( coordinateOfQRCode ) != 0 ):
                            coordinateOfQRCode = correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                            topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                            img_with_crop = crop_image( sourceImage, 0, bottomLeftCorners[x], topLeftCorners[y], bottomRightCorners[x] - bottomLeftCorners[x], bottomLeftCorners[y] - topLeftCorners[y] )
                            img_with_crop.save( "qr codes/big qr code.png" )
                            #print( coordinateOfQRCode )
                            print( "i find BIG QR CODE" )
                            #crop_img.save("I_FIND_HIM.jpg")
                            break

                start_x = start_x + int( width_big_qr_code / 10 ) 
                if ( ( start_x + int( width_big_qr_code )  ) >= width_source_image ):
                            start_x = 0
                            start_y = start_y + int( height_big_qr_code / 10 )
                if ( ( start_y + int( height_big_qr_code ) )  >= height_source_mage ):
                            print( "that's all :( ")
                            break

        return coordinateOfQRCode



#проверяем, перевернуто ли это изображение на более чем 180 градусов
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


#функци возвращает 3 состояния:
# - было повернуто на 180гр (ROTATED_ON_180)
# - было повернуто до нормального состояния( ROTATED_TO_NORMAL)
# - не было поверунто, все нормально (WAS_NOT_ROTATED)
def rotateImageByCoordinateOfQRCode( coordinateOfQRCode, sourceImage ):
    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
    if isThatImageReversed( topLeftCorners, bottomLeftCorners ):
        sourceImage = sourceImage.rotate( 180, expand=True)
        #rotated = ndimage.rotate( image, 180 )
        #misc.imsave( sourceImageFileName, rotated )
        return ROTATED_ON_180, sourceImage
        #читаем еще раз, т.к. перевернули
        #symbols = scanImageForQRCode( sourceImageFileName )
        #topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = symbols[ 0 ].locator
    print(  "hey = ",topLeftCorners, bottomLeftCorners, topRightCorners )
    rotateValue = getRotateValue( topLeftCorners, bottomLeftCorners, topRightCorners )
    print("rotateValue=", rotateValue)
    if abs(rotateValue) > 0:
        #дублирующийся код!!!!
        #rotateValue = rotateValue + 2.4
        #image = misc.imread( sourceImageFileName )
        #rotated = ndimage.rotate( image,  rotateValue, reshape = False )
        #misc.imsave( sourceImageFileName, rotated )
        sourceImage = sourceImage.rotate( rotateValue, expand=True)
        return ROTATED_TO_NORMAL, sourceImage
        #читаем еще раз, т.к. перевернули
        #symbols = scanImageForQRCode( fileName )
        #topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = symbols[ 0 ].locator
    #coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
    return WAS_NOT_ROTATED, sourceImage

def getPixelValueBySizeInInch( inch ):

        return ( int ) ( inch * DPI ) * 3

def getImageWithCells( sourceImageFileName, QRCode, fileNameImageWithCells ):
        
        distance_to_first_cell = getPixelValueBySizeInInch (WIDTH_FROM_QR_CODE_TO_CELL_INCH) + getPixelValueBySizeInInch(WIDTH_BETWEEN_CELLS_INCH) * 2 + getPixelValueBySizeInInch(WIDTH_OF_CELL_INCH)* 3
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = QRCode
        #print( topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners )
        start_x =  abs( bottomLeftCorners[x] - distance_to_first_cell )
        start_y = topLeftCorners[y]
        width = bottomLeftCorners[ x ] - start_x
        height = bottomLeftCorners[y] - topLeftCorners[y]
        #print( start_x, start_y, width, getPixelValueBySizeInInch(HEIGHT_OF_CELL_INCH) )
        img_with_crop = crop_image( sourceImageFileName, 0, start_x, start_y, width, height )
        img_with_crop.save( fileNameImageWithCells )
        #doThreshold( imageWithCells, imageWithCells )


def doThreshold( sourceImageFileName, destinationImageFileName, threshold = 200):
    
    img = cv2.imread( sourceImageFileName )
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    retval, bin = cv2.threshold( gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite( destinationImageFileName, bin )



def find_squares(img, thresholdValue ):
#возвращает контуры найденных МЕТОК

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    #cv2.imshow('gray', gray)
    #threshold(gray, gray, 100, 255, THRESH_BINARY)
    #gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    retval, bin = cv2.threshold( gray, thresholdValue, 255, cv2.THRESH_BINARY_INV)
    #bin = cv2.bitwise_not( bin )
    #cv2.imshow('bin', bin)
    #cv2.findContours(gray, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE)
    bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    #print ( len( contours) )
    count = 0
    for cnt in contours:
        rect = cv2.boundingRect( cnt )
        #print (rect)
        #print ( rect )
        k = ( rect[2] + 0.0) / rect[3]
        #print( " k = ", k, "contour = ", cv2.contourArea(cnt), "\n" )
        #rint ( cv2.contourArea(cnt) )
        if ( 0.8 < k and k < 1.8  and cv2.contourArea(cnt) > 3000 ):
            count = count + 1
            #print("k = ", k)
            #print( "x = ", rect[0], "y = ", rect[1])
            #print("contourArea = ", cv2.contourArea(cnt))
            #print( cnt )
            squares.append( cnt )                
                    
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
        #print ( pixel )
        for i in pixel:
                if i == 255:
                    white = white + 1
                else:
                    black = black + 1
    #print ( "white = ", white)
    #print ( "black = ", black)
    #print ( "len of pixels = ", white + black )
    if ( black / (white + black))  >= TRESHOLD_ON_MARKED_STATUS:
        result = 1
    return result

def getImageByContour( contour, imageWithCells, outputImageFileName ):

        x,y,w,h = cv2.boundingRect( contour  )
        crop = imageWithCells[y:y+h,x:x+w]
        cv2.imwrite( outputImageFileName, crop)

#возврат 1 - если успешно оберезали ячейку
# вовзврат 0 - если неуспешно
def prepareCell( image_with_cell, threshold_value ):
        img = cv2.imread(image_with_cell)
        gray = cv2.imread(image_with_cell,0)
        ret,thresh = cv2.threshold(gray,threshold_value ,255,1)
        bin, contours, h= cv2.findContours(thresh,1,2)
        result = 0
        for cnt in contours:
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                if len(approx)==4 or len(approx)==5:
                        getImageByContour( cnt, img, image_with_cell )
                        result = 1
                        break
                        #i = 1
                        #cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        return result

#238 - между ячейками в paint'e
#64 - высота ячейки
#64 - ширина
fileName = "4.jpg"
img = Image.open( fileName )
#ВАРИАНТ ГРУБОЙ СИЛЫ
coordinateOfQRCode = thirdVariantOfAlgorithm( img )
if ( len( coordinateOfQRCode ) > 0 ):
        bottomLeftCorners = coordinateOfQRCode[ 1 ]
        start_x = bottomLeftCorners[ x ]
        start_y = bottomLeftCorners[ y ]
        listOfQRCodes = findAllQRCodeOnColumn( img, start_x, start_y )
        if ( len ( listOfQRCodes ) > 0 ):
                #начинаем вырезать ячейки по каждому коду
                print (" LEN = ", len( listOfQRCodes ) )
                for i in range( 0, int( len( listOfQRCodes) / 2 ) ):
                        listOfResult = []
                        fileNameImageWithCells = "image with cells/" + str( i ) + "image_with_cells.png"
                        img = Image.open( fileName )
                        getImageWithCells( img, listOfQRCodes[ i * 2 + 1 ], fileNameImageWithCells )
                        img = cv2.imread( fileNameImageWithCells )
                        thresholdValue = 200
                        countOfCells = 0
                        squares = []
                        while ( countOfCells != 3 ):
                                squares = find_squares( img, thresholdValue )
                                countOfCells = len ( squares);
                                thresholdValue = thresholdValue - 10
                                if ( thresholdValue == 0 ):
                                        break
                        print( "threshold value = ", thresholdValue )
                        if (countOfCells == 3 ):
                                j = 0
                                for contour in squares:
                                        getImageByContour( contour, img, "cell" + str( j ) + ".png" )
                                        j = j + 1
                                for k in range ( 0, j ):
                                        cellFileName = "cell" + str( k ) + ".png"
                                        thresholdCellFileName = "threshold " + str( j )  + cellFileName
                                        doThreshold( cellFileName, thresholdCellFileName, thresholdValue )
                                        #while( 1 ):
                                               # if ( prepareCell( thresholdCellFileName, thresholdValue ) == 0 ):
                                                       # break
                                        #проверяем ячейку на заполннность
                                        prepareCell( thresholdCellFileName, thresholdValue )
                                        img = Image.open( thresholdCellFileName )
                                        img.save("cells/final_cell_" + str( i ) + "_" + str( k ) + ".png")
                                        listOfResult.append( checkImageOnMark( thresholdCellFileName ) )
                                #выводим результат пометки
                                print( listOfResult)
                        else:
                                print( "there is no cells :(")
                        #cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
                        #cv2.imshow('squares', img)
                        #cv2.waitKey(0)
        else:
                print( "there is no something about small QR codes :(");
else:
        print( "there is no BIG QR code :(")




