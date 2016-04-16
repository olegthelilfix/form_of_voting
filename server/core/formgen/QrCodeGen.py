# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

import qrcode
import settings

class QrCodeGen:
    __qr_code_form = "PNG"
    __qr_code_dir_to_small = "img/small"
    __qr_code_save_dir = settings.DIR_TO_PROJECT + "result/"
    __qr_code_fit = True

    def __init__(self, dirToProject):
        self.__qr_code_save_dir = dirToProject + "result/"

    """Функция создает qr code с задаными параметрами"""

    def create_qr_code(self, text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=3, border=2):
        qr = qrcode.QRCode(version, error_correction, box_size, border)
        qr.add_data(text)
        qr.make(fit=self.__qr_code_fit)
        return qr.make_image()

    """ Функция для сохраниения qr code с заданым путем"""

    def save_qr_code_in_file(self, img, dir_to_file):
        img.save(self.__qr_code_save_dir + dir_to_file, self.__qr_code_form)

    """ Функция создания qr code, который размещен в заголовке бланка, функция возвращает путь до qr кода"""

    def create_big_qr_code(self, text, name):
        code = self.create_qr_code(text)
        new_dir = name + "." + self.__qr_code_form
        self.save_qr_code_in_file(code, new_dir)
        return new_dir

    """Функция для создания qr code, который размещается возле вариантов ответа, функция возвращает путь до qr кода"""

    def create_small_qr_code(self, text, index):
        # параметры qr code - информация для кодирование, версия, уровень коррекции, размер квадратииков из которых
        #  состоит qr код, размер рамки вокруг qr кода(лучше 0б что бы ничего не съехало)
        code = self.create_qr_code(text, 1, qrcode.constants.ERROR_CORRECT_H, 3, 0)
        new_dir = self.__qr_code_dir_to_small + str(index) + "." + self.__qr_code_form
        self.save_qr_code_in_file(code, new_dir)
        return new_dir

