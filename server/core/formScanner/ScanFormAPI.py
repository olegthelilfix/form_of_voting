from ScanResult import *
from TokenFileWorker import *
from AlgorithmScan import *
from PIL import Image
import profile

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

    print("Get image and token id")
    # получаем результат распознавания.
    scanResult = startScan( image,
                            idToken )

    print("Set scan result")
    #заносим результат в TokeData( файл с результатами распознавания ).
    tokenFileWorker.setScanResult( scanResult )

    print("End scan form")

# получаем статус распознавания по маркеру.
def getStatus( idToken ):

    scanResult = tokenFileWorker.getScanResult( idToken )
    return scanResult.getStatus()
    

#ПРИМЕР ИСПОЛЬЗОВАНИЯ
#image = Image.open( SOURCE_IMAGE )
#idToken = generateIdToken()
#startScanForm( image,\
#               idToken )
#profile.run('startScanForm( image,\
#             idToken )')
#print( getStatus( idToken ) )

    


    
