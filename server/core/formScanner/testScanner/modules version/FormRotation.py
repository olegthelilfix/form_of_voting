from ImageWorker import *
import math
from numpy import arccos

class FormRotation:

    def __init__( self, imageWorker, marksCoordinates ):
        
        self.imageWorker = imageWorker
        self.marksCoordinates = marksCoordinates


    
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

        print( 'getRotateValue = ', topLeftCorners, bottomLeftCorners, topRightCorners)
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
            print( alpha, betta, gamma )
            if ( topLeftCorners[ X ] < bottomLeftCorners[ X ] ):
                betta = -betta
        return betta
    
	
    def start( self ):
        result = 0
        topLeftCorners, bottomLeftCorners, topRightCorners = self.convertMarksCoordinate( self.marksCoordinates )
        rotationValue = self.getRotateValue( topLeftCorners, bottomLeftCorners, topRightCorners )
        if ( rotationValue != 0 ):
            self.imageWorker.rotate( 1 )
            result = 1
            #self.imageWorker.saveImage( "rotation.jpg" )
        return result, self.imageWorker
