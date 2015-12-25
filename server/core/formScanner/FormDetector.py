from ImageWorker import *
from FormRotation import *
#

class FormDetector:
    
    def __init__( self, imagePIL, coordinatesOfBigQRCode ):

        self.imagePIL = imagePIL
        self.coordinatesOfBigQRCode = coordinatesOfBigQRCode


    #обнаружение листа засчет меток
    #возвращает список из координат потенциальных меток
    def detectFormByMarks( self, imageWorker ):
        
        imageWorker.doAdaptiveThreshold()
        contours = imageWorker.findContours()
        squares = []
        resultsContours = []
        for cnt in contours:
            rect = cv2.boundingRect( cnt )
            x = rect[ X ]
            y = rect[ Y ]
            width = rect[ WIDTH ]
            height = rect[ HEIGHT ]
            k = width / height
            
            if ( 0.6 < k and \
                 k < 1.5  and \
                 cv2.contourArea(cnt) > 1500  and \
                 cv2.contourArea(cnt) < 3000 ):
                print ( rect )
                #print( "x = ", rect[0], "y = ", rect[1])
                print("contourArea = ", cv2.contourArea(cnt) )
                squares.append( [ x, y, width, height ] )
                resultsContours.append( cnt )

        if ( DEBUG_FORM_DETECTOR != 0 ):
            cv2.drawContours( self.imageWorker.getOpenCVImage(), contours, -1, (0, 255, 0), 3 )
            cv2.imshow('squares', self.imageWorker.getOpenCVImage())
            cv2.waitKey(0)
            
        return squares

    #возвращает координаты листа засчет координат меток
    #под координатами понимается (пиксели):
    #x - точка по ОСИ X
    #y - точка по ОСИ Y
    #width - ширина
    #height - высота
    def getCoordinateOfFormByMarksCoordinates( self, marksCoordinates ):

        xCoordinates = []
        yCoordinates = []
        xCoordinatesWithWidth = []
        yCoordinatesWithHeight = []

        for i in range( 0, len( marksCoordinates ) ):
            xCoordinates.append( marksCoordinates[ i ][ X ] )
            yCoordinates.append( marksCoordinates[ i ][ Y ] )
            xCoordinatesWithWidth.append( marksCoordinates[ i ][ X ] +\
                                          marksCoordinates[ i ][ WIDTH ] )
            yCoordinatesWithHeight.append( marksCoordinates[ i ][ Y ] +\
                                           marksCoordinates[ i ][ HEIGHT ] )

        x = min( xCoordinates )
        y = min ( yCoordinates )
        #здесь под x лучше все-таки понимать min( xCoordinates )
        width = max( xCoordinatesWithWidth ) - x
        #здесь под y лучше все-таки понимать min ( yCoordinates )
        height = max( yCoordinatesWithHeight ) - y

        return x, y, width, height


    def setWidthByPixelsOfQRCode ( self, width ):

        self.widthOfQRCode = width
        
    def setHeightByPixelsOfQRCode( self, height ):

        self.heightQRCode = height
        
    
    #Предполагается, что лист уже перевернут
    #и известны координаты большого кода
    def detectFormByQRCode( self ):

        
        
    #функция начала работы 
    def start( self ):

        self.imageWorker.rotate( 0.6 )
        imageForDetectByMarks = ImageWorker( self.imageWorker, IMAGE_WORKER )
        marksCoordinates = self.detectFormByMarks( imageForDetectByMarks )
        print ( len( marksCoordinates ) )

        #ПОВОРОТ
        '''
        formRotation = FormRotation( self.imageWorker, marksCoordinates )
        resultRotation, self.imageWorker = formRotation.start()
        if ( resultRotation != 0 ):
            #перевернули изображение - повторяем!
            imageForDetectByMarks = ImageWorker( self.imageWorker, IMAGE_WORKER )
            marksCoordinates = self.detectFormByMarks( imageForDetectByMarks )
        '''
        
        x, y, width, height = self.getCoordinateOfFormByMarksCoordinates( marksCoordinates  )
        cropImage = self.imageWorker.getCropImage( x, y, width, height )
        self.imageWorker = ImageWorker( cropImage,
                                        PIL_IMAGE,
                                        NO_EXIF,
                                        self.imageWorker.getDPI() )
        #СОХРАНЯЕМ ОБРЕЗАННОЕ ИЗОБРАЖЕНИЕ
        cropImage.save("hehe.jpg")
        return self.imageWorker
        
        
