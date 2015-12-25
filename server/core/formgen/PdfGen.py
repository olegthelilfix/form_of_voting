# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from core.formgen.RenderHtml import RenderHtml
from weasyprint import HTML
import codecs
import os


class PdfGen:
    __dir = os.getcwd() + "/result/htmlcode.html"
    __result_dir = os.getcwd() + "/result/result.pdf"

    def execute(self, id_user, id_meeting):
        render = RenderHtml(id_user, id_meeting)
        value = render.split_question_on_pages()
        with codecs.open(self.__dir, 'w', 'utf8') as f2:
            f2.write(value)

        pdf = HTML(self.__dir)
        pdf.write_pdf(self.__result_dir)

        return self.__result_dir
