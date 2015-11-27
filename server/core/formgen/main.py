# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from core.formgen.RenderHtml import RenderHtml
from weasyprint import HTML

render = RenderHtml()
value = render.split_question_on_pages()
pdf = HTML(value)
pdf.write_pdf(value + ".pdf")