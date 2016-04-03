# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from PDFGenDAOPostgres import PDFGenDAOPostgres
from PDFGenDAOMySQL import PDFGenDAOMySQL
import settings

class FormData:
    __dao = None
    __qs = []
    __small_qr = []
    __version = "0.1"
    __id_user = "null"
    __id_owner = "null"
    __id_premise = "null"
    __id_meeting = "null"
    __fio = "______________________"
    __phoneNumber = "______________________"
    __city = '__________'
    __street = '___________'
    __houseNumb = '_____'
    __apartment = '_______'
    __form = '_____________'
    __share = '____________'
    __formDate = '_________'
    __propertyS = '___________'
    __css = ''

    def __init__(self, id_user, id_meeting):
        # init db type
        if settings.DB == "mysql":
            self.__dao = PDFGenDAOMySQL()
        else:
            self.__dao = PDFGenDAOPostgres()

        # clear date
        self.__small_qr = []
        self.__qs = []

        # get date
        self.__id_meeting = str(id_meeting)
        self.__id_user = str(id_user)
        qs_small_qr = self.__dao.get_question(id_meeting)

        for value in qs_small_qr:
            self.__small_qr.append('s' + str(value[2]))
            self.__qs.append(str(value[0]) + " " +value[1])

        if str(self.__dao.check_premise(self.__id_user)[0][0]) != 'None':
            result = self.__dao.get_title(id_meeting, id_user)
            self.__fio = result[0][2] + " " + result[0][0] + " " + result[0][1]
            self.__city = result[0][3]
            self.__street = result[0][4]
            self.__houseNumb = result[0][5]
            self.__apartment = str(result[0][6])
            self.__form = str(result[0][8])
            self.__share = str(round(result[0][9] * 100 / result[0][10], 2)) + '%'
            self.__formDate = str(result[0][11])
            self.__propertyS = str(result[0][12])
            self.__id_premise = str(result[0][13])
            self.__id_owner = str(result[0][14])

        self.__css = self.__dao.get_css(id_meeting)

    def get_date(self):
        return {
            "fio": self.__fio,
            "city": self.__city,
            "street": self.__street,
            "houseNumb": self.__houseNumb,
            "apartment": self.__apartment,
            "phoneNumber": self.__phoneNumber,
            "formSeries": self.__form,
            "formDateOfIssue": self.__formDate,
            "propertyS": self.__propertyS,
            "share": self.__share
        }

    # версия | 0 или 1| id_user | id_owner| id_premise | id meeting | количество страниц| и номер текущей|
    def get_big_qr_code_date(self):
        return 'b0|' + self.__get_big_qr_code_date()

    def get_big_qr_code_date2(self):
        return 'b1|' + self.__get_big_qr_code_date()

    def __get_big_qr_code_date(self):
        return self.__version.ljust(10, ' ') + '|' \
               + self.__id_user.ljust(10, ' ') + '|' \
               + self.__id_owner.ljust(10, ' ') + '|' \
               + self.__id_premise.ljust(10, ' ') + '|' \
               + self.__id_meeting.ljust(10, ' ')


    def get_questions(self):
        return self.__qs

    def get_small_qr_code_date(self):
        return self.__small_qr

    def get_css(self):
        return self.__css

    def end(self):
        self.__qs = []
        self.__small_qr = []
        self.__version = "0.1"
        self.__id_user = "null"
        self.__id_owner = "null"
        self.__id_premise = "null"
        self.__id_meeting = "null"
        self.__fio = "______________________"
        self.__phoneNumber = "______________________"
        self.__city = '__________'
        self.__street = '___________'
        self.__houseNumb = '_____'
        self.__apartment = '_______'
        self.__form = '_____________'
        self.__share = '____________'
        self.__formDate = '_________'
        self.__propertyS = '___________'
