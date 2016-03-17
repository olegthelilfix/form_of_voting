from BaseEnums import *

class CellsDetector:
    
    #imagePIL - ИСХОДНОЕ ПЕРЕВЕРНУТОЕ ИЗОБРАЖЕНИЕ
    #координаты кода напротив которого нужные ячейки
    def __init__( self, \
                  imagePIL, \
                  imageWithCells ):

        self.imagePIL = imagePIL
        self.imageWithCells = imageWithCells
        #self.coordinatesOfQRCode
        #self.xPixelsValue = xPixelsValue
        #self.yPixelsValue = yPixelsValue


    #вырезаем изображение - координаты в ПИКСЕЛЯХ
    def crop_image( self, input_image, isItFileName, start_x, start_y, width, height ):
            
            if ( isItFileName == 1):
                    input_img = Image.open(input_image)
            else:
                    input_img = input_image

            box = (start_x, start_y, (int)( start_x + width), (int)(start_y + height))
            #print( box )
            output_img = input_img.crop( box )
            #output_img.save( "test/crop" + str( counter ) + ".jpg")
            return output_img


    #НА ОСНОВАНИИ ЛИСТА (в изображении только лист)
    def getX_PixelsByMillimeters( self, value):

            return round( ( value ) * ( self.imagePIL.width / WIDTH_FORM ) )

    #НА ОСНОВАНИИ ЛИСТА (в изображении только лист)
    def getY_PixelsByMillimeters( self, value ):

            return round( ( value  ) * ( self.imagePIL.height / HEIGHT_FORM ) )


    #отступать начинаем от левого края - так как именно
    #там был QR код

    
    def cutFirstCell( self ):
        
        #расстояние до первой ячейки это
        # - расстояние между ячейками * 2 (т.к. перед первой ячейки еще 2 есть)
        # - ширина 2 ячеек
        # - ширина 4 рамок
        distanceToFirstCell = self.getX_PixelsByMillimeters( WIDTH_OF_CELL ) * 3 + \
                              self.getX_PixelsByMillimeters( DISTANCE_BETWEEN_CELLS ) * 2 + \
                              self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * 6 + \
                              self.getX_PixelsByMillimeters( DISTANCE_FROM_CODE_TO_CELL )

        yStart = int ( self.imageWithCells.height / 2 ) - \
                 int ( self.getY_PixelsByMillimeters( HEIGHT_OF_CELL ) / 4 ) + \
                 RESERVE_PIXELS_VALUE
        #yStart = 0
        #yStart = self.getY_PixelsByMillimeters( DISTANCE_TO_CELL_FROM_TOP_SIDE_OF_CODE )
        #сдвигаем немного
        xStart = self.imageWithCells.width - distanceToFirstCell + \
                 int ( self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * 3 )
        width = int ( self.getX_PixelsByMillimeters( WIDTH_OF_CELL ) / 2 )
        #height = self.imageWithCells.height
        height = int ( self.getY_PixelsByMillimeters( HEIGHT_OF_CELL ) / 4 )
        return self.crop_image( self.imageWithCells, \
                                0, \
                                xStart, \
                                yStart,
                                width,
                                height )

    def cutSecondCell( self ):
        
        distanceToCell = self.getX_PixelsByMillimeters( WIDTH_OF_CELL ) * 2 + \
                          self.getX_PixelsByMillimeters( DISTANCE_BETWEEN_CELLS ) + \
                          self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * 4 + \
                          self.getX_PixelsByMillimeters( DISTANCE_FROM_CODE_TO_CELL )
        
        yStart = int ( self.imageWithCells.height / 2 ) - \
                 int ( self.getY_PixelsByMillimeters( HEIGHT_OF_CELL ) / 4 ) +\
                 RESERVE_PIXELS_VALUE
        #yStart = 0
        #yStart = self.getY_PixelsByMillimeters( DISTANCE_TO_CELL_FROM_TOP_SIDE_OF_CODE )
        #сдвигаем немного
        xStart = self.imageWithCells.width - distanceToCell + \
                 int ( self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * 3 )
        width = int ( self.getX_PixelsByMillimeters( WIDTH_OF_CELL ) / 2 )
        #height = self.imageWithCells.height
        height = int ( self.getY_PixelsByMillimeters( HEIGHT_OF_CELL ) / 4 )
        return self.crop_image( self.imageWithCells, \
                                0, \
                                xStart, \
                                yStart,
                                width,
                                height )
    def cutThirdCell( self ):
        
        distanceToCell = self.getX_PixelsByMillimeters( WIDTH_OF_CELL ) + \
                          self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * 2 + \
                          self.getX_PixelsByMillimeters( DISTANCE_FROM_CODE_TO_CELL )
        yStart = int ( self.imageWithCells.height / 2 ) - \
                 int ( self.getY_PixelsByMillimeters( HEIGHT_OF_CELL ) / 4 ) + \
                 RESERVE_PIXELS_VALUE
        #yStart = 0
        #yStart = self.getY_PixelsByMillimeters( DISTANCE_TO_CELL_FROM_TOP_SIDE_OF_CODE )
        #сдвигаем немного
        xStart = self.imageWithCells.width - distanceToCell + \
                 int ( self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * 3 )
        width = int ( self.getX_PixelsByMillimeters( WIDTH_OF_CELL ) / 2 )
        #height = self.imageWithCells.height
        height = int ( self.getY_PixelsByMillimeters( HEIGHT_OF_CELL ) / 4 )
        return self.crop_image( self.imageWithCells, \
                                0, \
                                xStart, \
                                yStart,
                                width,
                                height )
    
    def cutCenterOfCell( self, imageCell ):

        #обрезаем по 3 рамки сверху,снизу,слева,справа
        """
        countWidthOfBox = 3
        reserve = RESERVE_PIXELS_VALUE
        xStart = self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * countWidthOfBox + reserve 
        yStart = self.getX_PixelsByMillimeters( WIDTH_OF_BOX ) * countWidthOfBox + reserve 
        width = imageCell.width - xStart * 2
        height = imageCell.height - yStart * 3
        return self.crop_image( imageCell, \
                                0, \
                                xStart, \
                                yStart,
                                width,
                                height )
        """
        return imageCell
    def start( self,\
               firstCellFileName = "firstCell.png",\
               secondCellFileName = "secondCell.png",\
               thirdCellFileName = "thirdCell.png" ):
        
        self.cutFirstCell().save( firstCellFileName )
        self.cutSecondCell().save( secondCellFileName )
        self.cutThirdCell().save( thirdCellFileName )
        
                                 
                         
        
