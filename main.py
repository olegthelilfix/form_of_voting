# -*- coding: utf8 -*-
import timer
import time

__author__ = 'Aleksandrov Oleg'
import codecs
import qrcode
import os
from weasyprint import HTML
from jinja import from_string

qr_code_form = "PNG"
qr_code_dir_to_big = "img/big"
qr_code_dir_to_small = "img/small"
qr_code_save_dir = "html/"
qr_code_fit = True
html_dir_to_file = os.getcwd() + "/html/htmlcode.html"
dir_to_pdf = "generate.pdf"

key = ("title", "fio", "city", "street", "houseNumb", "apartment", "phoneNumber", "formSeries", "formNumber",
       "formDateOfIssue", "propertyType", "propertyS", "share")

"""Функция создает qr code с задаными параметрами"""
def create_qr_code(text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=5, border=2):
    qr = qrcode.QRCode(version, error_correction, box_size, border)
    qr.add_data(text)
    qr.make(fit=qr_code_fit)
    return qr.make_image()

""" Функция для сохраниения qr code с заданым путем"""
def save_qr_code_in_file(img, dir_to_file):
    img.save(qr_code_save_dir + dir_to_file, qr_code_form)

""" Функция создания qr code, который размещен в заголовке бланка, функция возвращает путь до qr кода"""
def create_big_qr_code(text):
    code = create_qr_code(text)
    new_dir = qr_code_dir_to_big + "." + qr_code_form
    save_qr_code_in_file(code, new_dir)
    return new_dir

"""Функция для создания qr code, который размещается возле вариантов ответа, функция возвращает путь до qr кода"""
def create_small_qr_code(text, index):
    code = create_qr_code(text, 1, qrcode.constants.ERROR_CORRECT_H, 4, 0)
    new_dir = qr_code_dir_to_small + str(index) + "." + qr_code_form
    save_qr_code_in_file(code, new_dir)
    return new_dir

def get_qs_and_small_qr_code():
    qs = get_questions()
    date = get_small_qr_code_dates()
    i = 0
    item_list = []
    while i < len(qs):
        item_list.append({"qs": qs[i],
                          "dir": create_small_qr_code(date[i], i)})
        i += 1
    return item_list

def render_html(open_file):
    tmpl = from_string(open_file)
    date = get_date()
    return tmpl.render(title=date["title"], fio=date["fio"], city=date["city"], street=date["street"],
                   houseNumb=date["houseNumb"], apartment=date["apartment"], phoneNumber=date["phoneNumber"],
                   formSeries=date["formSeries"], formNumber=date["formNumber"],
                   formDateOfIssue=date["formDateOfIssue"], propertyType=date["propertyType"],
                   propertyS=date["propertyS"], share=date["share"],
                   big_qr_code=create_big_qr_code(get_big_qr_code_date()), item_list=get_qs_and_small_qr_code())


"""Заглушка для данных"""
def get_date():
    return {key[0]: "Заголовок", key[1]: "Петров Петр Петрович", key[2]: "Город", key[3]: "Улица", key[4]: "42", key[5]: "42",
            key[6]: "+799999999999", key[7]: "4444", key[8]: "999999", key[9]: "10-11-1019",
            key[10]: "Существует в 5 измерении", key[11]: "1000", key[12]: "1000%"}

"""Заглушка для данных"""
def get_big_qr_code_date():
    return "blablablablablablablabla"


"""Заглушка для данных"""
def get_small_qr_code_dates():
    return ["id_1", "id_2", "id_3", "id_4", "id_5", "id_6"]



"""Заглушка для данных"""
def get_questions():
    return ["вопрос 1", "Вопрос 2", "Вопрос 3", "Вопрос 4", "Вопрос 5", "Вопрос 6"]


t1 = time.clock()

file = open('html/template.html', 'r')
with codecs.open(html_dir_to_file, 'w', 'utf8') as f2:
    f2.write(render_html(file.read()))
pdf = HTML(html_dir_to_file)
pdf.write_pdf(dir_to_pdf)

print(time.clock() - t1)
