from lockfile import LockFile
from ScanResult import *
from ListScanResult import *
import json
from BaseEnums import *
from ScanResultEnums import *

SECONDS_WAIT_FOR_UNLOCK = 5

class TokenFileWorker:

        # fileName - имя файла, в который будет записываться
        # вся инофрмация о распознавании
        def __init__( self,\
                      fileName = RESULTS_FILE_NAME ):
                self.m_TokenFileName = fileName

        # предназначен для ПЕРЕУСТАНОВКИ значения scanResult
        # по известному idToken
        # ПРЕДПОЛАГАЕТСЯ, ЧТО TOKEН СУЩЕСТВУЕТ
        def setScanResult( self,\
                           scanResult ):
                
                self.addScanResult( scanResult,\
                                    TO_EXIST_SCAN_RESULT )
                

        def loadScanResults( self,\
                             fileHandler ):

                fileHandler.seek(0)
                listScanResult = ListScanResult()
                text = fileHandler.read()
  
                if ( len(text) > 0 ):
                        strParse = json.loads(text)
                        if ( len(strParse) > 0 ):
                                parse = strParse["m_ScanResultList"]
                                listScanResult.fromJSON(parse)

                return listScanResult
                                
        # Добавляет НОВЫЙ scanResult и возвращает idToken для него
        def addScanResult( self,\
                           scanResult,\
                           ADD_MODE = NEW_SCAN_RESULT ):
                
                lock = LockFile(self.m_TokenFileName)

		#ОБРАБОТКА НЕВОЗМОЖНОСТИ ДОЖДАТЬСЯ РАЗБЛОКИРОВАНИЯ ФАЙЛА
                lock.acquire( SECONDS_WAIT_FOR_UNLOCK )

                f = open(self.m_TokenFileName,\
                         'r+')
                listScanResult = self.loadScanResults( f )

                idToken = 0
                
                if ( ADD_MODE == TO_EXIST_SCAN_RESULT ):
                        listScanResult.setScanResultByIdToken( scanResult )
                else:
                        idToken = listScanResult.addScanResult( scanResult )

                f.seek(0)
                f.write( listScanResult.toJSON() )
                f.close()
                lock.release()

                return idToken

        
        def getScanResult( self,\
                           idToken ):
                
                lock = LockFile(self.m_TokenFileName)
                # пока что так...
                lock.acquire( SECONDS_WAIT_FOR_UNLOCK )
                f = open(self.m_TokenFileName,\
                         'r+')
                listScanResult = self.loadScanResults( f )
                f.close()
                lock.release()
                
                scanResult = listScanResult.getScanResultByIdToken( idToken )

                return scanResult
                
                

                
