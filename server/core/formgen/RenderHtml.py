# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from jinja2 import Environment, FileSystemLoader
from core.formgen.QrCodeGen import QrCodeGen
from core.formgen.FormData import FormData


class RenderHtml:
    qr = QrCodeGen()
    formData = FormData()
    resultList = []

    def create_small_qr_code_dates(self, size):
        value = []
        i = 0
        while i < size:
            value.append("S" + str(i))
            i += 1
        return value

    def get_qs_and_small_qr_code(self, qs, date):
        i = 0
        item_list = []
        while i < len(qs):
            item_list.append({"qs": qs[i],
                              "dir": self.qr.create_small_qr_code(date[i], i)})
            i += 1
        return item_list

    def render_html(self, qs, date):
        tmpl = Environment(loader=FileSystemLoader("html/"), trim_blocks=True)
        return tmpl.get_template('template.html').render(title=date["title"], fio=date["fio"], city=date["city"],
                                                         street=date["street"],
                                                         houseNumb=date["houseNumb"], apartment=date["apartment"],
                                                         phoneNumber=date["phoneNumber"],
                                                         formSeries=date["formSeries"], formNumber=date["formNumber"],
                                                         formDateOfIssue=date["formDateOfIssue"],
                                                         propertyType=date["propertyType"],
                                                         propertyS=date["propertyS"], share=date["share"],
                                                         big_qr_code=self.qr.create_big_qr_code(
                                                             self.formData.get_big_qr_code_date()),
                                                         item_list=qs)

    def render_html_until_title(self, qs):
        tmpl = Environment(loader=FileSystemLoader("html/"), trim_blocks=True)
        return tmpl.get_template('template.html').render(
            big_qr_code=self.qr.create_big_qr_code(self.formData.get_big_qr_code_date()),
            item_list=qs)

    def split_question_on_pages(self):
        self.resultList = []

        title_date = self.formData.get_date()
        questions = self.formData.get_questions()
        small_qr_code_date = self.create_small_qr_code_dates(len(questions))

        return self.render_html(self.get_qs_and_small_qr_code(questions, small_qr_code_date), title_date)



