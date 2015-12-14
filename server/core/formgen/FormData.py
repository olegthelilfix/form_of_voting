# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from core.DAO.PDFGenDAOPostgres import PDFGenDAOPostgres


class FormData:
    __dao = PDFGenDAOPostgres(user="postgres", password="smith620695", database="form")
    __qs = []
    __small_qr = []
    __version = "0.1"
    __id_user = "null"
    __id_owner = "null"
    __id_premise = "null"
    __id_meeting = "null"
    __fio = "______________________"

    def __init__(self, id_user, id_meeting):
        self.__id_meeting = str(id_meeting)
        self.__id_user = str(id_user)
        qs_small_qr = self.__dao.get_question(id_meeting)
        for value in qs_small_qr:
            self.__small_qr.append(value[0])
            self.__qs.append(value[1])
        self.__fio = self.__dao.get_owner_fio(id_user)

    def get_date(self):
        return {
            "fio": self.__fio,
            "city": "Город",
            "street": "Улица",
            "houseNumb": "42",
            "apartment": "42",
            "phoneNumber": "__________________________",
            "formSeries": "4444",
            "formNumber": "999999",
            "formDateOfIssue": "10-11-1019",
            "propertyType": "Существует в 5 измерении",
            "propertyS": "1000",
            "share": "1000%"
        }

    # версия| id_user | id_owner| id_premise | id meeting | количество страниц| и номер текущей|
    def get_big_qr_code_date(self):
        return self.__version + self.__id_user + self.__id_owner + self.__id_premise + self.__id_meeting

    def get_questions(self):
        return self.__qs

    def get_small_qr_code_date(self):
        return self.__small_qr
