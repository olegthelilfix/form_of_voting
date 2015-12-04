# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from core.formgen.RenderHtml import RenderHtml
from weasyprint import HTML
import codecs
import os

dir = os.getcwd() + "/result/htmlcode"
render = RenderHtml()
value = render.split_question_on_pages()
with codecs.open(dir, 'w', 'utf8') as f2:
    f2.write(value)
pdf = HTML(dir)
pdf.write_pdf(os.getcwd() + "/result/result.pdf")
