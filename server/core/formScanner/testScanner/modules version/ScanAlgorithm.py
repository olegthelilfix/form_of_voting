from ImageWorker import *
from FindBigQRCode import *
from FormDetector import *
from FindSmallQRCodes import *

class ScanAlgorithm:

    def __init__( self, fileName ):
        
        self.fileName = fileName

    def start( self ):

        #загрузка изображения
        self.imageWorker = ImageWorker( self.fileName, \
                                        FILE_NAME, \
                                        YES_EXIF )
        #поиск листа на изображении
        self.formDetector = FormDetector( self.imageWorker )
        self.imageWorker = ImageWorker( self.formDetector.start(),\
                                        IMAGE_WORKER )
        '''
        #поиск БОЛЬШОГО КОДА
        self.findBigQRCode = FindBigQRCode( self.imageWorker )
        
        resultSearchOfBiQR, symbol, coordinates = self.findBigQRCode.start()
        if ( resultSearchOfBiQR != 0 ):

            print( symbol )
            """
            self.imageWorker.getCropImage( coordinates[ X ], \
                                           coordinates[ Y ], \
                                           coordinates[ WIDTH ], \
                                           coodinates[ HEIGHT ] )
            """
        '''
		#поиск маленьких кодов
        self.findSmallQRCodes = FindSmallQRCodes( self.imageWorker )
        self.findSmallQRCodes.start()
