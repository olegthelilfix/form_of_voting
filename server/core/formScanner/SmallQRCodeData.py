

class SmallQRCodeData:

    #resultList - список ячеек принадлежавщих вопросу
    #установленное значение - ячейка помечена
    #0 - не помечена
    def __init__( self ):
        
        self.m_Title = ''
        self.m_ResultList = []

    def setData( self,\
                 data):        
        self.m_Title  = data

    def setResultList( self,\
                       resultList ):

        self.m_ResultList = resultList

    def getData( self ):

        return self.m_SmallQRCodeTitle

    def getResultList( self ):

        return self.m_ResultList
