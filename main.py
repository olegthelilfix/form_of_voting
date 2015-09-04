# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg'
import qrcode
import os

qr_code_form = "PNG"
qr_code_dir_to_big = "img/big"
qr_code_dir_to_small = "img/small"
qr_code_save_dir = "html/"
qr_code_fit = True
html_dir_to_file = os.getcwd() + "/html/htmlcode.html"

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


def get_date():
    date = {key[0]: "Заголовок", key[1]: "тестовое имя", key[2]: "Город", key[3]: "Улица", key[4]: "42", key[5]: "42",
            key[6]: "+799999999999", key[7]: "4444", key[8]: "999999", key[9]: "10-11-1019",
            key[10]: "Существует в 5 измерении", key[11]: "1000", key[12]: "1000%"}
    return date


def get_questions():
    questions = ["вопрос 1", "Вопрос 2", "Вопрос 3", "Вопрос 4"]
    return questions


def create_html(date, questions, dir_to_big_qr_code):
    html = get_head()
    html += get_doc_title(date, dir_to_big_qr_code)
    html += "</body> </html>"
    f = open(html_dir_to_file, 'w')
    f.write(html)
    f.close()
    return html_dir_to_file


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


"""key = ("title", "fio", "city", "street", "houseNumb", "apartment", "phoneNumber", "formSeries", "formNumber",
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


create_html(get_date(), [2], create_big_qr_code("dfdsfdsfdsfsdfdfsdfdfdsfdsfd"))
