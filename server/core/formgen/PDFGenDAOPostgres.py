# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

import pg8000
import settings

class PDFGenDAOPostgres:
    _connect = None

    def __init__(self):
        # conn = pg8000.connect(user="postgres", password="smith620695", database="form")
        self.conn = pg8000.connect(user=settings.DB_USER, password=settings.DB_PASSWORD,
                                   database=settings.DB_NAME, host=settings.DB_HOST,
                                   port=settings.DB_PORT)

    def __del__(self):
        self.conn.close()

    def check_premise(self, id_user):
        return self.__execute("select id_premise from \"User\" where id_user = " + str(id_user))

    def get_question(self, id_meeting):
        return self.__execute("select sequence_no, question  from question where id_meeting = " + str(
            id_meeting) + " order by sequence_no asc")

    def get_title(self, id_meeting, id_user):
        return self.__execute("select "
                              "owner.name, "
                              "owner.patronymic,"
                              "owner.surname,"
                              "building.address,"
                              "building.street,"
                              "building.street_number,"
                              "premise.number,"
                              "building.block_type, "
                              "property_rights.regnumber,"
                              "property_rights.share_numerator,"
                              "property_rights.share_denominator,"
                              "property_rights.regdate,"
                              "premise.area_rosreestr "

                              "from "
                              "meeting,"
                              "building,"
                              "premise,"
                              "property_rights,"
                              "owner,"
                              "\"User\""
                              "where "
                              "meeting.id_meeting = " + str(id_meeting) + " AND "
                                                                          "\"User\".id_user = " + str(id_user) + " AND "
                                                                                                                 "\"User\".id_owner = owner.id_owner AND "
                                                                                                                 "meeting.id_building = building.id_building AND "
                                                                                                                 "building.id_building = premise.id_building AND "
                                                                                                                 "premise.id_premise = property_rights.id_premise AND "
                                                                                                                 "property_rights.id_owner = owner.id_owner")

    def __execute(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result
