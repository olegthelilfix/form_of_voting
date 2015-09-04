# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg'
import qrcode
import os
from weasyprint import HTML

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


def create_qr_code(text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=3, border=4):
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
    code = create_qr_code(text, 1, qrcode.constants.ERROR_CORRECT_H, 2, 0)
    new_dir = qr_code_dir_to_small + str(index) + "." + qr_code_form
    save_qr_code_in_file(code, new_dir)
    return new_dir

""" Функция для создание всех необходимых qr кодов распологаемых возле вариантов ответа"""

def get_small_qr_codes(qr_code_date):
    mass = []
    index = 0
    for date in qr_code_date:
        mass.append(create_small_qr_code(date, index))
        index += 1
    return mass

"""Основная функция генерации html документа, возвращает путь до созданного html документа"""

def create_html(date, questions, dir_to_big_qr_code, dir_to_small_qr_code):
    html = get_head()
    html += get_doc_title(date, dir_to_big_qr_code)
    html += get_doc_questions(questions, dir_to_small_qr_code)
    html += "</body> </html>"
    f = open(html_dir_to_file, 'w')
    f.write(html)
    f.close()
    return html_dir_to_file

"""" функция создает заголовок html документа. Содержит используемые стили """

def get_head():
    html = "<!DOCTYPE html> <html lang='en'> <head> <meta charset='UTF-8'>"
    html += "<style>"
    html += " .title{ text-align: center; } "
    html += " .rightimg { float: right; } "
    html += " body { margin-top: 0; margin-left: 0; margin-right: 0; } "
    html += " button { border: 2px solid black; background: white; font-size: 14px; padding: 10px 20px;} "
    html += " .qs { display:inline-block; } "
    html += "</style>"
    html += " <title></title>  </head>"
    return html


""" Функция создает шапку документа, содержащую информацию о жильце
key = ("title", "fio", "city", "street", "houseNumb", "apartment", "phoneNumber", "formSeries", "formNumber",
       "formDateOfIssue", "propertyType", "propertyS", "share")"""
def get_doc_title(date, dir_to_big_qr_code):
    html = "<body> <h1><div class='title'>" + date["title"] + "</div> </h1> <br>"
    html += " <img src='" + dir_to_big_qr_code + "' class='rightimg'>"
    html += "Ф.И.О. собственника: " + date["fio"] + " <br>"
    html += " Адрес помещения:" + date["city"] + ","
    html += " Улица:" + date["street"] + ", Дом: " + date["houseNumb"] + ",<br>"
    html += "Квартира: " + date["apartment"] + ",<br>"
    html += " Телефон:" + date["phoneNumber"] + "<br>"
    html += "Свидетельство о государственной регистрации права собственности: бланк серии - " + date["formSeries"]
    html += ", №" + date["formNumber"] + ","
    html += "Дата выдачи:" + date["formDateOfIssue"] + ",<br>"
    html += "Тип помещения: " + date["propertyType"] + "<br>"
    html += "Общая площадь помещения(кв.м): " + date["propertyS"] + "<br>"
    html += "Размер доли в праве собственности: " + date["share"] + "<br>"
    return html

"""Функция создает список вопросов с вариантами ответов """

def get_doc_questions(questions, dir_to_qr_codes):
    html = "<h1><div class='title'>Вопросы, поставленные на голосование:</div> </h1> <br>"
    i = 0
    while i < len(questions):
        html += questions[i] + "<br>"
        html += "<div class='qs'><div><img src='" + dir_to_qr_codes[i] + "'></div></div>"
        html += "<div class='qs'><div> За<br><button></button></div></div>"
        html += "<div class='qs'><div><img src='" + dir_to_qr_codes[i] + "'></div></div>"
        html += "<div class='qs'><div> Против<br><button></button></div></div>"
        html += "<div class='qs'><div><img src='" + dir_to_qr_codes[i] + "'></div></div>"
        html += "<div class='qs'><div> Воздерживаюсь<br><button></button></div></div><br>"
        i += 1
    return html

"""Заглушка для данных"""

def get_date():
    return {key[0]: "Заголовок", key[1]: "тестовое имя", key[2]: "Город", key[3]: "Улица", key[4]: "42", key[5]: "42",
            key[6]: "+799999999999", key[7]: "4444", key[8]: "999999", key[9]: "10-11-1019",
            key[10]: "Существует в 5 измерении", key[11]: "1000", key[12]: "1000%"}

"""Заглушка для данных"""

def get_questions():
    return ["вопрос 1", "Вопрос 2", "Вопрос 3", "Вопрос 4"]

"""Заглушка для данных"""

def get_big_qr_code_date():
    return "blablablablablablablabla"

"""Заглушка для данных"""

def get_small_qr_code_dates():
    return ["id_1", "id_2", "id_3", "id_4"]


small_qr_codes = get_small_qr_codes(get_small_qr_code_dates())
create_html(get_date(), get_questions(), create_big_qr_code(get_big_qr_code_date()), small_qr_codes)
pdf = HTML(html_dir_to_file)
pdf.write_pdf(dir_to_pdf)
