from BaseEnums import *

import math
from PIL import Image
from numpy import arccos
import numpy as np
import cv2

class FormRotation:

    #imagePIL - изображение PIL
    #coordinatesOfQRCode - координаты кода, на основании которого
    #                      осуществляем доворот
    def __init__( self, imageFileName, coordinatesOfQRCode ):

        self.imagePIL = imageFileName
        self.imageFileName = imageFileName
        self.coordinatesOfQRCode = coordinatesOfQRCode

    def rotateImage( self, fname, angle ):

        image = cv2.imread(fname, -1)

        center = tuple(np.array(image.shape[0:2])/2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotate = cv2.warpAffine(image, matrix, image.shape[0:2], flags=cv2.INTER_LINEAR)

        newFile = "rotation.png"

        cv2.imwrite(newFile, rotate)
    
    def convertMarksCoordinate( self, marksCoordinates ):
   
        xTopLeft =  marksCoordinates[ 0 ][ X ]
        yTopLeft = marksCoordinates[ 0 ][ Y ]

        xBottomLeft =  marksCoordinates[ 1 ][ X ]
        yBottomLeft = marksCoordinates[ 1 ][ Y ]
        
        xTopRight = marksCoordinates[ 2 ][ X ]
        yTopRight = marksCoordinates[ 2 ][ Y ]

        topLeftCorners = [ xTopLeft, yTopLeft ]
        bottomLeftCorners = [ xBottomLeft, yBottomLeft ]
        topRightCorners = [ xTopRight, yTopRight ]

        return topLeftCorners, bottomLeftCorners, topRightCorners
    
    def getRotateValue( self, topLeftCorners, bottomLeftCorners, topRightCorners ):

        #print( 'getRotateValue = ', topLeftCorners, bottomLeftCorners, topRightCorners)
        apexA = topLeftCorners
        apexC = bottomLeftCorners
        apexB = [ bottomLeftCorners[ X ], topRightCorners[ Y ] ]
        betta = 0
        #AB
        sideC = math.sqrt( ( apexC[ X ] - apexA[ X ] ) ** 2 + ( apexC[ Y ] - apexA[ Y ] ) ** 2)
        #BC 
        sideA = math.sqrt( ( apexC[ X ] - apexB[ X ] ) ** 2 + ( apexC[ Y ] - apexB[ Y ] ) ** 2)
        #AC
        
        sideB = math.sqrt( ( apexB[ X ] - apexA[ X ] ) ** 2 + ( apexB[ Y ] - apexA[ Y ] ) ** 2)
        if sideC + sideA > sideB and sideC + sideB > sideA and sideB + sideA > sideC:
                
            aRad = math.acos( ( sideB * sideB + sideC * sideC - sideA * sideA ) / ( 2 * sideB * sideC ) )
            bRad = math.acos( ( sideA ** 2 + sideC ** 2 - sideB ** 2 ) / ( 2 * sideA * sideC ) )
            alpha = aRad * 180 / 3.14
            betta = bRad * 180 / 3.14
            gamma = 180 - alpha - betta
            #print( alpha, betta, gamma )
            if ( topLeftCorners[ X ] < bottomLeftCorners[ X ] ):
                betta = -betta
                
        return betta

    #Возврат 1 - если был осуществлен доворот
    #        0 - если не был
    def start( self ):
        result = 0
        image = self.imagePIL
        topLeftCorners,bottomLeftCorners,bottomRightCorners,topRightCorners = self.coordinatesOfQRCode
        
        if ( bottomLeftCorners[ X ] != topLeftCorners[ X ] ):
            rotationValue = self.getRotateValue( topLeftCorners, bottomLeftCorners, topRightCorners )
            #self.rotateImage( self.imageFileName, rotationValue )
            image = self.imagePIL.rotate( rotationValue, resample=Image.BICUBIC, expand=True )
            #image.save( "rotation.png" )
            result = 1
            #self.imagePIL.save( "rotatiom.png" )
            
        return result, image
