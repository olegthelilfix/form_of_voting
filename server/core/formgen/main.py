# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from server.core.formgen.PdfGen import PdfGen

pg = PdfGen()
print(pg.execute(16, 9))
