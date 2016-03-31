# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

import settings
import pymysql
import pymysql.cursors

class PDFGenDAOMySQL:
    _connect = None

    def __init__(self):
        self.conn = pymysql.connect(user=settings.DB_USER, passwd=settings.DB_PASSWORD,
                                    db=settings.DB_NAME, host=settings.DB_HOST,
                                    port=settings.DB_PORT)

    def __del__(self):
        self.conn.close()

    def check_premise(self, id_user):
        return self.__execute("select id_premise from User where id_user = " + str(id_user))

    def get_question(self, id_meeting):
        return self.__execute("select sequence_no, question  from Question where id_meeting = " + str(id_meeting) + " order by sequence_no asc")

    def get_title(self, id_meeting, id_user):
        SQL='select Owner.name, Owner.patronymic, Owner.surname, Building.address, Building.street,Building.street_number,Premise.number,Building.block_type, Property_rights.regnumber, Property_rights.share_numerator, Property_rights.share_denominator,Property_rights.regdate,Premise.area_rosreestr from Meeting,Building, Premise, Property_rights, Owner, User where Meeting.id_meeting = ' + str(id_meeting) + ' AND User.id_user = ' + str(id_user) + ' AND User.id_owner = Owner.id_owner AND Meeting.id_building = Building.id_building AND Building.id_building = Premise.id_building AND Premise.id_premise = Property_rights.id_premise AND Property_rights.id_owner = Owner.id_owner'

        return self.__execute(SQL)

    def __execute(self, query):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        finally:
            cursor.close()

        return result
