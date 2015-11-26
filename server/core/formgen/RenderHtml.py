# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

import codecs
import os
from jinja2 import Environment, FileSystemLoader
from QrCodeGen import QrCodeGen
from FormData import FormData


class RenderHtml:
    html_dir_to_file = os.getcwd() + "/result/htmlcode"
    max_string_len = 55
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

    def split_string(self, string, max_count):
        result_mas = []
        sub_string = ""
        count = 0
        string_end_flag = "<br>"
        is_space = False

        for char in string:
            if count == max_count:
                if is_space:
                    sub_string += "-"
                result_mas.append(sub_string + string_end_flag)
                sub_string = ""
                count = 0
            sub_string += char
            count += 1
            is_space = not (char == ' ')

        if len(sub_string) > 0:
            result_mas.append(sub_string + string_end_flag)

        return result_mas

    def split_questions(self):
        questions = self.formData.get_questions()
        list = []
        for qs in questions:
            list.append(self.split_string(qs, self.max_string_len))
        return list

    def split_question_on_pages(self):
        self.resultList = []

        title_date = self.formData.get_date()
        questions = self.split_questions()
        small_qr_code_date = self.create_small_qr_code_dates(len(questions))

        pageID = -1
        while len(questions) > 0:
            pageID += 1
            if pageID == 0:
                if self.culcSelectedElement(questions, 4) < 8:
                    questions = self.join_questions(questions, small_qr_code_date, 4, pageID, title_date, True)
                elif self.culcSelectedElement(questions, 3) <= 14:
                    questions = self.join_questions(questions, small_qr_code_date, 3, pageID, title_date, True)
                elif self.culcSelectedElement(questions, 2) <= 20:
                    questions = self.join_questions(questions, small_qr_code_date, 2, pageID, title_date, True)
                elif self.culcSelectedElement(questions, 2) <= 26:
                    questions = self.join_questions(questions, small_qr_code_date, 2, pageID, title_date, True)
            else:
                if self.culcSelectedElement(questions, 6) <= 20:
                    questions = self.join_questions(questions, small_qr_code_date, 6, pageID, title_date, False)
                elif self.culcSelectedElement(questions, 5) <= 26:
                    questions = self.join_questions(questions, small_qr_code_date, 5, pageID, title_date, False)
                elif self.culcSelectedElement(questions, 4) <= 32:
                    questions = self.join_questions(questions, small_qr_code_date, 4, pageID, title_date, False)
                elif self.culcSelectedElement(questions, 2) <= 38:
                    questions = self.join_questions(questions, small_qr_code_date, 2, pageID, title_date, False)
                elif self.culcSelectedElement(questions, 1) <= 44:
                    questions = self.join_questions(questions, small_qr_code_date, 1, pageID, title_date, False)

        return self.resultList

    def calcLen(self, qs):
        i = 0
        for q in qs:
            i += 1
        return i

    def remove_element(self, qs, numb):
        i = 0
        while i < numb:
            del qs[i]
            i += 1
        return qs

    def join_questions(self, qs, qr, numb, pageID, date, isFirstPage):
        join_qs = []
        ln = self.calcLen(qs)

        if numb > ln:
            numb = ln
        i = 0
        qrcodes = []
        while i < numb:
            element = qs.pop(0)
            qrcodes.append(qr.pop(0))
            join_qs.append(self.join_str(element))
            i += 1

        dir_to_file = self.html_dir_to_file + str(pageID) + ".html"

        if isFirstPage:
            with codecs.open(dir_to_file, 'w', 'utf8') as f2:
                f2.write(self.render_html(self.get_qs_and_small_qr_code(join_qs, qrcodes), date))
        else:
            with codecs.open(dir_to_file, 'w', 'utf8') as f2:
                f2.write(self.render_html_until_title(self.get_qs_and_small_qr_code(join_qs, qrcodes)))

        self.resultList.append(dir_to_file)

        return qs

    def join_str(self, mass):
        result = ""
        for str in mass:
            result += str
        return result

    def culcSelectedElement(self, element, numb):
        i = 0
        result = 0
        val = self.calcLen(element)
        if numb > val:
            numb = val
        while i < numb:
            result += len(element[i])
            i += 1
        return result
