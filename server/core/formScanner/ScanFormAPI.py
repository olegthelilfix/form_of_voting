from ScanResult import *
from TokenFileWorker import *
from AlgorithmScan import *
from PIL import Image


# Имя файла с изображением бланка.
#---------------------------------------------------
SOURCE_IMAGE = "003.jpg"
#---------------------------------------------------

tokenFileWorker = TokenFileWorker()

# возвращает доступный idToken 
def generateIdToken():
    
    scanResult = ScanResult()
    scanResult.setStatus( BEFORE_SCAN )
    
    return tokenFileWorker.addScanResult( scanResult )


# начинаем работу алгоритма распознавания.
#
# image - исходное изображение(формат - PIL).
# idToken - номер маркера, по которому будет идентифицироваться
# результат распознавания.
def startScanForm( image,\
                   idToken ):

    # получаем результат распознавания.
    scanResult = startScan( image,
                            idToken )
    #заносим результат в TokeData( файл с результатами распознавания ).
    tokenFileWorker.setScanResult( scanResult )

# получаем статус распознавания по маркеру.
def getStatus( idToken ):

    scanResult = tokenFileWorker.getScanResult( idToken )
    return scanResult.getStatus()
    

#ПРИМЕР ИСПОЛЬЗОВАНИЯ
image = Image.open( SOURCE_IMAGE )
idToken = generateIdToken()
startScanForm( image,\
              idToken )
print( getStatus( idToken ) )

    


    
