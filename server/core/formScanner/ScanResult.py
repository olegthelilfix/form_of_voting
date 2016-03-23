import json
from ScanResultEnums import *
from BigQRCodeData import *

class ScanResult:

    def __init__( self ):

        self.m_IdToken = 0
        self.m_Status = UNAVAILABLE_SCAN_RESULT_RECORD
        self.m_BigQRCodeData = BigQRCodeData()
        self.m_SmallQRCodeDataList = []

    def addSmallQRCodeData( self,\
                            smallQRCodeData ):

        self.m_SmallQRCodeDataList.append( smallQRCodeData )

    def setIdToken( self,\
                    idToken ):
        self.m_IdToken = idToken
        
    def setStatus( self,\
                   status ):
        self.m_Status = status

    def getIdToken( self ):
        
        return self.m_IdToken
    
    def getStatus( self ):

        return self.m_Status

    def setBigQRCodeData( self,\
                          bigQRCodeData ):
        
        self.m_BigQRCodeData = bigQRCodeData

