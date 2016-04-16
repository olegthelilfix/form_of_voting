from BaseEnums import *
import re

class BigQRCodeData:

    def __init__( self ):

        self.m_PageBit = UNDEFINED_VALUE
        
        self.m_Version = UNDEFINED_VALUE
        self.m_IdUser = UNDEFINED_VALUE
        self.m_IdOwner = UNDEFINED_VALUE
        self.m_IdPremise = UNDEFINED_VALUE
        self.m_IdMeeting = UNDEFINED_VALUE

    def setDataFromJSON( self,\
                         data ):

        self.initializeData( data["m_PageBit"],\
                             data["m_Version"],\
                             data["m_IdUser"],\
                             data["m_IdOwner"],\
                             data["m_IdPremise"],\
                             data["m_IdMeeting"] )

    def initializeData( self,\
                        pageBit,\
                        version,
                        idUser,\
                        idOwner,\
                        idPremise,\
                        idMeeting ):

        self.m_PageBit = pageBit
        self.m_Version = version
        self.m_IdUser = idUser
        self.m_IdOwner = idOwner
        self.m_IdPremise = idPremise
        self.m_IdMeeting = idMeeting


    def getPageBit( self ):

        return self.m_PageBit
    
    def parseNumFromStr( self,\
                         sourceStr ):

        return re.findall('(\d+)', sourceStr )[0]

    
    def parseDataFromStr( self,\
                          strData ):
        # ВЕРСИЯ БЛАНКА!!!!!
        # число полей в большом коде может больше не совпадать!
        data = strData.split('|')
        pageBit = self.parseNumFromStr( data[0] )
        version  = self.parseNumFromStr( data[ 1 ] )
        idUser = self.parseNumFromStr( data[2] )
        idOwner = self.parseNumFromStr( data[3] )
        idPremise = self.parseNumFromStr( data[4] )
        idMeeting = self.parseNumFromStr( data[5] )
        self.initializeData( pageBit,\
                             version,\
                             idUser,\
                             idOwner,\
                             idPremise,\
                             idMeeting)

    # Этот большой qr код с большой страницы?
    def isThisQRCodeIsNotOnTheFirstPage( self ):

        return self.m_PageBit == 0
        
