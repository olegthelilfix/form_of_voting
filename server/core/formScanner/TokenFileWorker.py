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
                

        # Добавляет НОВЫЙ scanResult и возвращает idToken для него
        def addScanResult( self,\
                           scanResult,\
                           ADD_MODE = NEW_SCAN_RESULT ):
                
                lock = LockFile(self.m_TokenFileName)

		#ОБРАБОТКА НЕВОЗМОЖНОСТИ ДОЖДАТЬСЯ РАЗБЛОКИРОВАНИЯ ФАЙЛА
                lock.acquire( SECONDS_WAIT_FOR_UNLOCK )

                f = open(self.m_TokenFileName,\
                         'r+')
                f.seek(0)
                listScanResult = ListScanResult()
                text = f.read()
                idToken = 0
                
                if ( len(text) > 0 ):
                        strParse = json.loads(text)
                        if ( len(strParse) > 0 ):
                                parse = strParse["m_ScanResultList"]
                                listScanResult.fromJSON(parse)

                if ( ADD_MODE == TO_EXIST_SCAN_RESULT ):
                        listScanResult.setScanResultByIdToken( scanResult )
                else:
                        idToken = listScanResult.addScanResult( scanResult )

                f.seek(0)
                f.write( listScanResult.toJSON() )
                f.close()

                lock.release()
		
                return idToken
                

                
