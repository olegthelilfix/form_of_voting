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


# пример использования
image = Image.open( SOURCE_IMAGE )
idToken = generateIdToken()
startScanForm( image,\
               idToken )


    


    
