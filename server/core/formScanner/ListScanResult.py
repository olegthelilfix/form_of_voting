from ScanResult import *
from SmallQRCodeData import *
from BigQRCodeData import *


class ListScanResult:

    def __init__(self):
        
        self.m_ScanResultList = []

    def addScanResult( self,\
                       scanResult ):

        idToken = self.getNextAvailableTokenId()
        scanResult.setIdToken( idToken )
        self.m_ScanResultList.append( scanResult )

        return idToken

    

    #Меняем инофрмацию о распознавании по токену
    def setScanResultByIdToken( self,\
                                scanResult ):
        index = 0
        for item in self.m_ScanResultList:
            
            if ( item.getIdToken() == scanResult.getIdToken()):
                self.m_ScanResultList[ index ] = scanResult
                return
            
            index = index + 1

        #такого idToken еще нет.
        #добавляем scanResult с его установленным idToken по умолчанию
        #addScanResult( scanResult )
                

    def getScanResultByIdToken( self,\
                                idToken ):

        scanResult = ScanResult()
        for item in self.m_ScanResultList:
            if ( item.getIdToken() == idToken ):
                return item

        return scanResult
        
    def toJSON( self ):
        return json.dumps( self,\
                           default = lambda o: o.__dict__,\
                           sort_keys=True,
                           indent=4)
    def fromJSON( self,\
                  strParse ):
        size = len(strParse)
        for item in strParse:
            scanResult = ScanResult()
            #большой код
            bigQRCodeData = BigQRCodeData()
            bigQRCodeData.setData( item["m_BigQRCodeData"]["m_Data"] )
            scanResult.setBigQRCodeData(bigQRCodeData)
            scanResult.setIdToken( item["m_IdToken"] )
            scanResult.setStatus(item["m_Status"])
            
            #маленькие коды парсим
            smallQRCodeList = item["m_SmallQRCodeDataList"]
            for smallQRCode in smallQRCodeList:
                smallQRCodeData = SmallQRCodeData()
                smallQRCodeData.setData(smallQRCode["m_Title"])
                lst = []
                lst = smallQRCode["m_ResultList"]
                smallQRCodeData.setResultList(lst)
                scanResult.addSmallQRCodeData(smallQRCodeData)
            
            self.m_ScanResultList.append(scanResult)
            
    def getNextAvailableTokenId( self ):

        idTokenList = []
        nexTokenId = 0
        for scanResult in self.m_ScanResultList:
            idTokenList.append( scanResult.getIdToken() )

        if ( len( idTokenList ) > 0 ): 
            nexTokenId = max(idTokenList) + 1
            
        return nexTokenId
        
        
