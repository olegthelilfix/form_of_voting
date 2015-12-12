from ImageWorker import *
from QRCodeDetector import *

class FindBigQRCode:

    def __init__( self, imageWorker ):

        self.imageWorker = imageWorker

    def start( self ):
		#ввести константу для запаса
        widthOfQRCode = self.imageWorker.getX_PixelsByMillimeters( WIDHT_OF_BIG_QR_CODE )
        heightOfQRCode = self.imageWorker.getY_PixelsByMillimeters( HEIGHT_OF_BIG_QR_CODE )
        qrCodeDetector = QRCodeDetector( self.imageWorker )
		
        return qrCodeDetector.start( 0, 0, widthOfQRCode, heightOfQRCode, FULL_QR_SEARCH ) 
