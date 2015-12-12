from ImageWorker import *
from QRCodeDetector import *

class FindSmallQRCodes:

    def __init__( self, imageWorker ):

        self.imageWorker = imageWorker

    def start( self ):
        
		#ввести константу для запаса
        widthOfQRCode = self.imageWorker.getX_PixelsByMillimeters( WIDTH_OF_SMALL_QR_CODE + 2 )
        heightOfQRCode = self.imageWorker.getY_PixelsByMillimeters( HEIGHT_OF_SMALL_QR_CODE + 2 )

        qrCodeDetector = QRCodeDetector( self.imageWorker )
        startPos = self.imageWorker.getImageWidth() - \
                   self.imageWorker.getX_PixelsByMillimeters( START_POS_FOR_SMALL_QR_CODE_SEARCH )
        result, symbol, coordinates = qrCodeDetector.start( startPos,\
                                                            0,\
                                                            widthOfQRCode,\
                                                            heightOfQRCode,\
                                                            Y_QR_SEARCH )
        return result, symbol, coordinates
