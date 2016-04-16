# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from jinja2 import Environment, FileSystemLoader
from QrCodeGen import QrCodeGen
from FormData import FormData

class RenderHtml:
    qr = None
    formData = None
    resultList = []
    __dirToProject = ""
    __big_qr_code = ""
    __big_qr_code2 = ""
    __css = ""
    __questions = None

    def __init__(self, id_user, id_meeting, dirToProject, qs=None, css=None):
        self.formData = FormData(id_user, id_meeting)
        self.__dirToProject = dirToProject
        self.qr = QrCodeGen(dirToProject)
        if css is not None:
            self.__css = css
        else:
            self.__css = self.formData.get_css()

        if qs is not None:
            self.__questions = qs
        else:
            self.__questions = self.formData.get_questions()

    def set_css_qs(self, css, qs):
        self.__css = css
        self.__questions = qs

    def get_qs_and_small_qr_code(self, qs, date):
        i = 0
        item_list = []

        while i < len(qs):
            item_list.append({
                              "qs": qs[i],
                              "dir": self.qr.create_small_qr_code(date[i], i)
                             })
            i += 1

        return item_list

    def render_html(self, qs, date):
        tmpl = Environment(loader=FileSystemLoader(self.__dirToProject + "html/"), trim_blocks=True)

        result = tmpl.get_template('template.html').render(fio=date["fio"],
                                                         city=date["city"],
                                                         street=date["street"],
                                                         houseNumb=date["houseNumb"],
                                                         apartment=date["apartment"],
                                                         phoneNumber=date["phoneNumber"],
                                                         formSeries=date["formSeries"],
                                                         formDateOfIssue=date["formDateOfIssue"],
                                                         propertyS=date["propertyS"],
                                                         share=date["share"],
                                                         big_qr_code=self.__big_qr_code,
                                                         item_list=qs,
                                                         big_qr_code2=self.__big_qr_code2,
                                                         css=self.__css)
        self.formData.end()

        return result

    def render_html_until_title(self, qs):
        tmpl = Environment(loader=FileSystemLoader(self.__dirToProject + "html/"), trim_blocks=True)

        return tmpl.get_template('template.html').render(
            big_qr_code=self.qr.create_big_qr_code(self.formData.get_big_qr_code_date()),
            item_list=qs)

    def render_doc(self):
        self.resultList = []

        title_date = self.formData.get_date()
        small_qr_code_date = self.formData.get_small_qr_code_date()
        self.__big_qr_code = self.qr.create_big_qr_code(self.formData.get_big_qr_code_date(), "img/big")
        self.__big_qr_code2 = self.qr.create_big_qr_code(self.formData.get_big_qr_code_date2(),"img/big2")

        return self.render_html(self.get_qs_and_small_qr_code(self.__questions, small_qr_code_date), title_date)



