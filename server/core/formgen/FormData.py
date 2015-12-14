# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from core.DAO.PDFGenDAOPostgres import PDFGenDAOPostgres


class FormData:
    dao = PDFGenDAOPostgres(user="postgres", password="smith620695", database="form")
    qs = []
    small_qr = []

    def __init__(self,  id_meeting):
        qs_small_qr = self.dao.get_question(id_meeting)
        for value in qs_small_qr:
            self.small_qr.append(value[0])
            self.qs.append(value[1])


    def get_date(self):
        return {"title": "Заголовок", "fio": "Петров Петр Петрович", "city": "Город", "street": "Улица",
                "houseNumb": "42",
                "apartment": "42", "phoneNumber": "__________________________", "formSeries": "4444", "formNumber": "999999",
                "formDateOfIssue": "10-11-1019", "propertyType": "Существует в 5 измерении", "propertyS": "1000",
                "share": "1000%"}

    """Заглушка для данных"""

    # версия| id_user | id_owner| id_premise | id meeting | количество страниц| и номер текущей|
    def get_big_qr_code_date(self):
        return "0.1|12345|67890|123456|7890|5|1"

    """Заглушка для данных"""
    def get_questions(self):
        return self.qs

    def get_small_qr_code_date(self):
        return self.small_qr