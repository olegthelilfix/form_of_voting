# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg'
import qrcode
import os

qr_code_form = "PNG"
qr_code_dir_to_big = os.getcwd() + "/img/big"
qr_code_dir_to_small = os.getcwd() + "/img/small"
qr_code_fit = True
"""Функция создает qr code с задаными параметрами"""
def create_qr_code(text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=3, border=4):
    qr = qrcode.QRCode(version, error_correction, box_size, border)
    qr.add_data(text)
    qr.make(fit=qr_code_fit)
    return qr.make_image()
""" Функция для сохраниения qr code с заданым путем"""
def save_qr_code_in_file(img, dir_to_file):
    img.save(dir_to_file, qr_code_form)
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
