from ImageWorker import *
from CellsParameters import *
from QRCodeParameters import *
from BaseEnums import *
import libzbar as zbar

class QRScanAlgorithm:

    #точка старта алгоритма
    # imageFileName - исходное изображение
    def start( self, imageFileName ):
        self.imageWorker = ImageWorker( imageFileName )
        #поиск БОЛЬШОГО QR кода
        coordinatesOfBigQRCode = self.findBigQRCode( self.imageWorker )
        #берем координаты Левого нижнего угла большого кода
        bottomLeftCorners = coordinatesOfBigQRCode[ 1 ]
        start_x = bottomLeftCorners[ X ]
        start_y = bottomLeftCorners[ Y ]
        listOfQRCodes = self.findAllSmallQRCodeInColumn( self.imageWorker, start_x, start_y )
        return listOfQRCodes
        

    #проверка заполненности ячейки
    #input_image - PIL изображение!
    def checkImageOnMark( self, input_image ):
        
        result = 0
        #print( input_image)
        pixels = list( img.getdata() )
        #print ( len( pixels ) )
        black = 0
        white = 0
        for pixel in pixels:
            if pixel == 0:
                white = white + 1
            else:
                black = black + 1
        print ( "white = ", white)
        print ( "black = ", black)
        if ( white / len ( pixels ) )  >= TRESHOLD_ON_MARKED_STATUS:
            result = 1
        return result


    #корректировка координат найденного кода
    #относительно ИСХОДНОГО ИЗОБРАЖЕНИЯ
    def correctCoordinateOfQRCode( self, coordinateOfQRCode, start_x, start_y ):
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
        topLeftCorners = topLeftCorners[ X ] + start_x, topLeftCorners[ Y ] + start_y
        bottomLeftCorners = bottomLeftCorners[ X ] + start_x, start_y + bottomLeftCorners[ Y ]
        topRightCorners = topRightCorners[ X ] + start_x, topRightCorners[ Y ] + start_y
        bottomRightCorners = bottomRightCorners[ X ] + start_x, bottomRightCorners[ Y ] + start_y
        coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
        
        return coordinateOfQRCode


    def getPixelValueBySizeInInch( self, DPI, inch ):
        
        return ( int ) ( inch * DPI ) * 3


    #сканирует изображение на наличие QR кода
    def scanImageForQRCode( self, image ):
    
        symbols = zbar.Image.from_im( image ).scan()
        return symbols


    #поиск ПЕРВОГО ПОПАВШЕГОСЯ qr кода
    def findFirstQRCode( self, image ):
        symbols = self.scanImageForQRCode( image )
        coordinateOfQRCode = []
        if ( len( symbols) > 0 ):
                sym = symbols[ 0 ]
                topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = [item for item in sym.locator]
                coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners

        return coordinateOfQRCode
    
    #этап поиска большого QR кода
    #поиск осуществляется методом грубой силы
    #начинаем поиск с верхнего левого угла
    def findBigQRCode( self, image ):
        #изображение может быть повернуто на 45 гр.
        #считаем диагналь QR кода
        #d = int( math.sqrt(HEIGHT_OF_BIG_QR_CODE ** 2 + WIDTH_OF_BIG_QR_CODE ** 2) )
        #MAX_HEIGHT_OF_BIG_QR_CODE = MAX_WIDTH_OF_BIG_QR_CODE = 
        self.height_big_qr_code_pixel = self.getPixelValueBySizeInInch( image.getDPI(), HEIGHT_OF_BIG_QR_CODE_INCH )
        self.width_big_qr_code_pixel = self.getPixelValueBySizeInInch( image.getDPI(), WIDHT_OF_BIG_QR_CODE_INCH )

        #im = Image.open( sourceImageFileName ).convert('L')
        width_source_image = image.getImageWidth()
        height_source_mage = image.getImageHeight()
        start_x = 0
        start_y = 0
        coordinateOfQRCode = []
        while( 1 ):
    
                #crop_img = image.createCopy()
                #image.saveImage( "test.jpg" )
                crop_img = image.cropImage( start_x, start_y, self.width_big_qr_code_pixel, self.height_big_qr_code_pixel )
                #crop_img.saveImage( "test1.jpg")
                coordinateOfQRCode = self.findFirstQRCode( crop_img )
                if ( len( coordinateOfQRCode ) != 0 ):
                            coordinateOfQRCode = self.correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                            topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                            #вырезаем исключительно только найденный код из исходного ИЗОБРАЖЕНИЯ
                            img_with_crop = image.cropImage( bottomLeftCorners[ X ], topLeftCorners[ Y ], bottomRightCorners[ X ] - bottomLeftCorners[ X ], bottomLeftCorners[ Y ] - topLeftCorners[ Y ] )
                            #img_with_crop.save( "2223.png" )
                            #print( coordinateOfQRCode
                            print( "I FIND HIM!!!!" )
                            #crop_img.save("I_FIND_HIM.jpg")
                            break

                start_x = start_x + int( self.width_big_qr_code_pixel / 10 ) 
                if ( ( start_x + int( self.width_big_qr_code_pixel )  ) >= width_source_image ):
                            start_x = 0
                            start_y = start_y + int( self.height_big_qr_code_pixel / 10 )
                if ( ( start_y + int( self.height_big_qr_code_pixel ) )  >= height_source_mage ):
                            print( "that's all :( ")
                            break

        return coordinateOfQRCode

    #вырезает ЯЧЕЙКИ заданного маленького QR кода
    def getImageWithCells( self, sourceImageFileName, QRCode, fileNameImageWithCells ):
        
        distance_to_first_cell = getPixelValueBySizeInInch (WIDTH_FROM_QR_CODE_TO_CELL_INCH) + getPixelValueBySizeInInch(WIDTH_BETWEEN_CELLS_INCH) * 2 + getPixelValueBySizeInInch(WIDTH_OF_CELL_INCH)* 3
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = QRCode
        print( topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners )
        start_x =  bottomLeftCorners[x] - distance_to_first_cell
        start_y = bottomLeftCorners[y] - getPixelValueBySizeInInch(HEIGHT_OF_CELL_INCH)
        width = distance_to_first_cell
        print( start_x, start_y, width, getPixelValueBySizeInInch(HEIGHT_OF_CELL_INCH) )
        img_with_crop = crop_image( sourceImageFileName, 0, start_x, start_y, width, getPixelValueBySizeInInch(HEIGHT_OF_CELL_INCH) )
        img_with_crop.save( fileNameImageWithCells )
        #doThreshold( imageWithCells, imageWithCells )

    #пытаемся вырзеать ВНУТРЕННОСТЬ ячейки.
    #если не получается - считаем что ячейка 100% чем-то заполнена
    def prepareCell( self, image_with_cell, threshold_value ):
        img = cv2.imread(image_with_cell)
        gray = cv2.imread(image_with_cell,0)
        ret,thresh = cv2.threshold(gray,threshold_value ,255,1)
        bin, contours, h= cv2.findContours(thresh,1,2)
        result = 0
        for cnt in contours:
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                if len(approx)==4:
                        getImageByContour( cnt, img, image_with_cell )
                        result = 1
                        break
                        #i = 1
                        #cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        return result


    def divValueBy( self, value, divValue ):
        value = int(value / divValue)
        return value


    #возврат формата ОБРАТНО
    def convertCoordinatesOfCodeToBack( self, coordinateOfQRCode ):
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode

        topLeftCorners = self.divValueBy( topLeftCorners[ X ], 2) , self.divValueBy( topLeftCorners[ Y ], 2)
        
        bottomLeftCorners = self.divValueBy( bottomLeftCorners[ X ], 2), self.divValueBy( bottomLeftCorners[ Y ], 2)
        
        bottomRightCorners = self.divValueBy( bottomRightCorners[ X ], 2), self.divValueBy( bottomRightCorners[ Y ], 2)
        
        topRightCorners = self.divValueBy( topRightCorners[ X ], 2), self.divValueBy( topRightCorners[ Y ], 2)
  
        coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
        
        return coordinateOfQRCode


    #поиск на изображении кода через threshold!
    def tryToScanQRCodeByThreshold( self, imgWithPossibleQR ):
        
        symbols = []
        for i in range( 1, 10 ):
            imageWithThreshold = ImageWorker( imgWithPossibleQR, IT_IS_IMAGE_ALREADY)
            threshold = 200 - i * 10
            imageWithThreshold.doThreshold( threshold )
            symbols = self.scanImageForQRCode( imageWithThreshold.getImage() )
            if ( len ( symbols ) > 0 ):
                break
            
        return symbols
        
    #поиск ВСЕХ маленьких кодов
    #при поиске, отталкиваемся от того,
    #что все маленькие коды расположены в одну колонку на равне с большим кодом
    def findAllSmallQRCodeInColumn( self, imageWorker, start_x, start_y ):
    #ОЖИДАЕМ ЧТО ИЗОБРАЖЕНИЕ УЖЕ ПЕРЕВЕНУТО
    #БЕРЕМ В КАЧЕСТЕ ЭТАЛОНА РАЗМЕР БОЛЬШОГО КОДА
        height = int( self.height_big_qr_code_pixel / 2 )
        width = self.width_big_qr_code_pixel
        
        fileNameImgWithPossibleQr = "img_with_possible_qr.png"
        
        step_y = int ( height / 10 )
        heghtOfImage = imageWorker.getImageHeight()

        topLeftCorners = -1
        bottomLeftCorners = -1
        bottomRightCorners = -1
        topRightCorners = -1
        data = ""
        listOfQRCodes = []
        c = 0
        while( 1 ):
            imgWithPossibleQR = imageWorker.cropImage( start_x, start_y, width, height )
            #img_with_possible_qr = resizeImage2( img_with_possible_qr, ( img_with_possible_qr.width * 2, img_with_possible_qr.height * 2) )
            #img_with_possible_qr.save( str( start_y ) + fileNameImgWithPossibleQr )
            c = c + 1
            #imgWithPossibleQR.save( "test2/" + "original" + str(c) + fileNameImgWithPossibleQr )
            
            symbols = self.tryToScanQRCodeByThreshold( imgWithPossibleQR )
            if ( len( symbols ) > 0 ):
                print( "yes!!" )
                for sym in symbols:
                    coordinateOfQRCode = [item for item in sym.locator]
                    #так как мы увеличивали изображение - переводим координаты обратно
                    coordinateOfQRCode = self.convertCoordinatesOfCodeToBack( coordinateOfQRCode ) 
                    coordinateOfQRCode = self.correctCoordinateOfQRCode( coordinateOfQRCode, start_x, start_y )
                    topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
                    img_with_crop = imageWorker.cropImage( bottomLeftCorners[X], topLeftCorners[Y], bottomRightCorners[X] - bottomLeftCorners[X], bottomLeftCorners[Y] - topLeftCorners[Y] )
                    img_with_crop.save("resQr.png")
                    start_y = bottomLeftCorners[ Y ]
                    listOfQRCodes.append( sym )
                    listOfQRCodes.append( coordinateOfQRCode )
                    #listOfQRCodes.append( topLeftCorners )
                    #listOfQRCodes.append( bottomLeftCorners )
                    #listOfQRCodes.append( bottomRightCorners )
                    #listOfQRCodes.append( topRightCorners )
                print(' I FIND QR!!!!')
                print( str( c ) + fileNameImgWithPossibleQr )
                return listOfQRCodes

            start_y = start_y + step_y
            #print( "start_x", start_x, "start_y", start_y)
            #count_y = count_y + 1

            if ( ( start_y + height ) >= heghtOfImage ):
                print("finished find qr codes")
                print( len( listOfQRCodes ) / 2 )
                break

        return listOfQRCodes

