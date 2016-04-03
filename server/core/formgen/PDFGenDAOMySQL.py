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
        SQL = "select id_premise from Users where id = " + str(id_user)
        result = self.__execute(SQL)

        self.__debug(SQL, result)

        return result

    def get_question(self, id_meeting):
        SQL = "select sequence_no, question, id_question  from Question where id_meeting = " + str(id_meeting) + " order by sequence_no asc"
        result = self.__execute(SQL)

        self.__debug(SQL, result)

        return result

    def get_title(self, id_meeting, id_user):
        SQL='select Owner.name, Owner.patronymic, Owner.surname, Building.address, Building.street,Building.street_number,Premise.number,Building.block_type, Property_rights.regnumber, Property_rights.share_numerator, Property_rights.share_denominator,Property_rights.regdate,Premise.area_rosreestr, Premise.id_premise, Owner.id_owner from Meeting,Building, Premise, Property_rights, Owner, Users where Meeting.id_meeting = ' + str(id_meeting) + ' AND Users.id = ' + str(id_user) + ' AND Users.id_owner = Owner.id_owner AND Meeting.id_building = Building.id_building AND Building.id_building = Premise.id_building AND Premise.id_premise = Property_rights.id_premise AND Property_rights.id_owner = Owner.id_owner'
        result = self.__execute(SQL)

        self.__debug(SQL, result)

        return result

    def get_css(self, id_meeting):
        SQL = "select Markup_style.css_style from Markup_style, Meeting where Meeting.id_meeting="+ str(id_meeting) + " AND Markup_style.id_markup_style = Meeting.id_markup_style"
        result = self.__execute(SQL)

        self.__debug(SQL, result)

        return result

    def __debug(self, SQL, result):
        if settings.IS_DEBUG:
            print("SQL = " + str(SQL) + "\n")
            print("RETURN = " + str(result) + '\n')

    def __execute(self, query):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        finally:
            cursor.close()

        return result
