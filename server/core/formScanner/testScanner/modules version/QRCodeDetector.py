import libzbar as zbar
from ImageWorker import *

class QRCodeDetector:

    def __init__( self, imageWorker ):

        self.imageWorker = imageWorker

    #startX - начало поиска для кода по Х
    #startY - начало поиска кода по Y
    #widthOfQRCode - ширина кода в ПИКСЕЛЯХ
    #heightOfQRCode - высота кода в ПИКСЕЛЯХ
    #searchStatus - параметры поиска:
        #


    def scanImageForQRCode( self, imagePIL ):

        symbols = zbar.Image.from_im( imagePIL ).scan()
        
        return symbols


    def correctCoordinateOfQRCode( self, coordinateOfQRCode, start_x, start_y ):

        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = coordinateOfQRCode
        #y = bottomLeftCorners[y] - topLeftCorners[y]
        topLeftCorners = topLeftCorners[ X ] + start_x, topLeftCorners[ Y ] + start_y
        #topLeftCorners[y] = topLeftCorners[ y ] + start_y
        bottomLeftCorners = bottomLeftCorners[ X ] + start_x, start_y + bottomLeftCorners[ Y ]
        #bottomLeftCorners[ y ] = bottomLeftCorners[ y ] + topLeftCornest[ y ]
        topRightCorners = topRightCorners[ X ] + start_x, topRightCorners[ Y ] + start_y
        #topRightCorners[ y ] = topRightCorners[ y ] + start_y
        bottomRightCorners = bottomRightCorners[ X ] + start_x, bottomRightCorners[ Y ] + start_y
        #bottomRightCorners[ y ] = bottomRightCorners[ y ] + topRightCorners[ y ]
        coordinateOfQRCode = topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners
        return coordinateOfQRCode

    def start( self, \
               startX, \
               startY, \
               widthOfQRCode, \
               heightOfQRCode, \
               searchStatus ):

        result = 0
        symbol = 0
        coordinates = [ startX, startY ]
        
        stepX = 10
        stepY = 10
        print( "stepY = ", stepY )
        print( "stepX = ", stepX )
        print ("widthOfQRCode =", widthOfQRCode)
        print ( "heightOfQRCode = ", heightOfQRCode)

        maxStartX = self.imageWorker.getImageWidth()
        maxStartY = self.imageWorker.getImageHeight()
        print( "maxStartX = ", maxStartX )

        counter = 0
        
        while( 1 ):

            #print( startX)
            #вырезаем изображение с потецниальным кодом
            imageWithPossibleQRCode = ImageWorker( self.imageWorker.getCropImage( startX, \
                                                                                  startY, \
                                                                                  widthOfQRCode, \
                                                                                  heightOfQRCode ),\
                                                   PIL_IMAGE )
            thresholdValue = 200
            #imageWithPossibleQRCode.getPILImage().save( "qrcodes/" + str(counter) + "thresh_source.jpg" )
            #применяем threshold
            for i in range ( 0, 13 ):
                thresholdValue = 200 - i * 10
                thresholdImg = ImageWorker( imageWithPossibleQRCode, \
                                            IMAGE_WORKER )
                #print( " i = ", i)
                #print("threshold value = ",  thresholdValue )
                thresholdImg.doThreshold( thresholdValue, \
                                          QR_CODE_DETECTOR_THRESHOLD_REASON )
                symbols = self.scanImageForQRCode( thresholdImg.getPILImage() )
                #thresholdImg.getPILImage().save("qrcodes/" + str(counter) + "_" + str( i ) + "thresh.jpg")
                if ( len( symbols ) > 0 ):
                    #print( "len( symbols ) > 0")
                    symbol = symbols[ 0 ]
                    topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in symbol.locator]
                    coordinateOfQRCode = topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners
                    coordinates = self.correctCoordinateOfQRCode( coordinateOfQRCode, startX, startY )
                    #imageWithPossibleQRCode.saveImage( "thresh.jpg" )
                    break

            counter = counter + 1
            if ( len ( symbols ) > 0 ):
                #print( "qr code")
                result = 1
                break

            if ( searchStatus == FULL_QR_SEARCH or \
                 searchStatus == X_QR_SEARCH ):
                
                startX = startX + stepX
                
                #если подобрались к границе изображения
                if ( startX + widthOfQRCode > maxStartX ):
                    
                    if ( searchStatus == X_QR_SEARCH ):
                        break
                    else:
                        startY = startY + stepY
                        startX = 0
                        if ( startY + stepY > maxStartY ):
                            break
            
            else:
                startY = startY + stepY
                if ( startY + stepY > maxStartY ):
                    break
                
        return result, symbol, coordinates


                
            
