# -*- coding: utf8 -*-

__author__ = 'Aleksandrov Oleg, 4231'

import time
import codecs
import qrcode
import os

import pdfkit


from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

qr_code_form = "PNG"
qr_code_dir_to_big = "img/big"
qr_code_dir_to_small = "img/small"
qr_code_save_dir = "html/"
qr_code_fit = True
html_dir_to_file = os.getcwd() + "/html/htmlcode"
dir_to_pdf = os.getcwd() + "/generate"
max_string_len = 55


"""Функция создает qr code с задаными параметрами"""
def create_qr_code(text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=3, border=2):
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
    # параметры qr code - информация для кодирование, версия, уровень коррекции, размер квадратииков из которых
    #  состоит qr код, размер рамки вокруг qr кода(лучше 0б что бы ничего не съехало)
    code = create_qr_code(text, 1, qrcode.constants.ERROR_CORRECT_H, 3, 0)
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

def get_qs_and_small_qr_code(qs, date):
    i = 0
    item_list = []
    while i < len(qs):
        item_list.append({"qs": qs[i],
                          "dir": create_small_qr_code(date[i], i)})
        i += 1
    return item_list

def render_html(qs, date):
    tmpl = Environment(loader=FileSystemLoader("html/"), trim_blocks=True)
    return tmpl.get_template('template.html').render(title=date["title"], fio=date["fio"], city=date["city"], street=date["street"],
                   houseNumb=date["houseNumb"], apartment=date["apartment"], phoneNumber=date["phoneNumber"],
                   formSeries=date["formSeries"], formNumber=date["formNumber"],
                   formDateOfIssue=date["formDateOfIssue"], propertyType=date["propertyType"],
                   propertyS=date["propertyS"], share=date["share"],
                   big_qr_code=create_big_qr_code(get_big_qr_code_date()), item_list=qs)

def render_html_until_title(qs):
    tmpl = Environment(loader=FileSystemLoader("html/"), trim_blocks=True)
    return tmpl.get_template('template.html').render(big_qr_code=create_big_qr_code(get_big_qr_code_date()), item_list=qs)

def split_string(string, max_count):
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

def split_questions():
    questions = get_questions()
    list = []
    for qs in questions:
        list.append(split_string(qs, max_string_len))
    return list

def split_question_on_pages():
    title_date = get_date()
    small_qr_code_date = get_small_qr_code_dates()
    questions = split_questions()

    pageID = -1
    while len(questions) > 0:
        pageID += 1
        if pageID == 0:
            if culcSelectedElement(questions, 4) < 8:
                questions = join_questions(questions, small_qr_code_date, 4, pageID, title_date, True)
            elif culcSelectedElement(questions, 3) <= 14:
                questions = join_questions(questions, small_qr_code_date, 3, pageID, title_date, True)
            elif culcSelectedElement(questions, 2) <= 20:
                questions = join_questions(questions, small_qr_code_date, 2, pageID, title_date, True)
            elif culcSelectedElement(questions, 2) <= 26:
                questions = join_questions(questions, small_qr_code_date, 2, pageID, title_date, True)
        else:
            if culcSelectedElement(questions, 6) <= 20:
                questions = join_questions(questions, small_qr_code_date, 6, pageID, title_date, False)
            elif culcSelectedElement(questions, 5) <= 26:
                questions = join_questions(questions, small_qr_code_date, 5, pageID, title_date, False)
            elif culcSelectedElement(questions, 4) <= 32:
                questions = join_questions(questions, small_qr_code_date, 4, pageID, title_date, False)
            elif culcSelectedElement(questions, 2) <= 38:
                questions = join_questions(questions, small_qr_code_date, 2, pageID, title_date, False)
            elif culcSelectedElement(questions, 1) <= 44:
                questions = join_questions(questions, small_qr_code_date, 1, pageID, title_date, False)


    return pageID

def calcLen(qs):
    i = 0
    for q in qs:
        i += 1
    return i

def remove_element(qs, numb):
    i = 0
    while i < numb:
        del qs[i]
        i += 1
    return qs

def join_questions(qs, qr, numb, pageID, date, isFirstPage):
    join_qs = []
    ln = calcLen(qs)

    if numb > ln:
        numb = ln
    i = 0
    qrcodes = []
    while i < numb:
        element = qs.pop(0)
        qrcodes.append(qr.pop(0))
        join_qs.append(join_str(element))
        i += 1

    if isFirstPage:
      #  file = open('html/template.html', 'r')
        with codecs.open(html_dir_to_file + str(pageID) + ".html", 'w', 'utf8') as f2:
             f2.write(render_html(get_qs_and_small_qr_code(join_qs, qrcodes), date))
    else:
#        file = open('html/template_until_title.html', 'r')
        with codecs.open(html_dir_to_file + str(pageID) + ".html", 'w', 'utf8') as f2:
             f2.write(render_html_until_title(get_qs_and_small_qr_code(join_qs, qrcodes)))

    return qs

def join_str(mass):
    result = ""
    for str in mass:
        result += str
    return result

def culcSelectedElement(element, numb):
    i = 0
    result = 0
    val = calcLen(element)
    if numb > val:
        numb = val
    while i < numb:
        result += len(element[i])
        i += 1
    return result

"""Заглушка для данных"""
def get_date():
    return {"title": "Заголовок", "fio": "Петров Петр Петрович", "city": "Город", "street": "Улица", "houseNumb": "42",
            "apartment": "42", "phoneNumber": "+799999999999", "formSeries": "4444", "formNumber": "999999",
            "formDateOfIssue": "10-11-1019", "propertyType": "Существует в 5 измерении", "propertyS": "1000",
            "share": "1000%"}

"""Заглушка для данных"""
def get_big_qr_code_date():
    return "B12321321321313,123213213"


"""Заглушка для данных"""
def get_small_qr_code_dates():
    return ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "s12", "S13", "S14", "S15", "S16", "S17"]



"""Заглушка для данных"""
def get_questions():
    return ["156789012345678 901234567890 123456789 012345 67891234540123 45678 901234567890 1234567890 1234 5678 9",
            "25678901234 567890123456789012 3456789012 34567891234 540123456789 12345678901 23456789 0123 56789",
            "3567890123456789012345678901234567890123456789123454012345678901234567890123456789012 3456789",
            "4567890123456789012345678901234567890123456789123454012345678901234567890123456789012 3456789",
            "55678901234567890123456789012345678901234567891234540123456789012345678901234567890123 456789",
            "6suck5678901234567890123456789012345678901234567891234540123456789012345678901234567890 123456789",
            "7suck5678901234567890123456789012345678901234567891234540123456789012345678901234567890 123456789",
            "8suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "9suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "10suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "11suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "12suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "13suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "14suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "15suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "16suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789",
            "17suck56789012345678901234567890123456789012345678912345401234567890123456789012345678901 23456789"]

val = split_question_on_pages()

i = 0
while i <= val:
    pdf = HTML(html_dir_to_file + str(i) + ".html")
    pdf.write_pdf(dir_to_pdf  + str(i) + ".pdf")
    i += 1