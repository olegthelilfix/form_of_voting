# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from RenderHtml import RenderHtml
from weasyprint import HTML
import codecs
import settings

class PdfGen:
    __dirToProject = settings.DIR_TO_PROJECT
    __dir = __dirToProject + "result/htmlcode.html"
    __file_name = 'result.pdf'
    __result_dir = __dirToProject + "result/"

    def execute(self, id_user, id_meeting):
        render = RenderHtml(id_user, id_meeting, self.__dirToProject)
        value = render.render_doc()

        with codecs.open(self.__dir, 'w', 'utf8') as file:
            file.write(value)

        pdf = HTML(self.__dir)
        newName = str(id_user) + str(id_meeting) + self.__file_name
        pdf.write_pdf(self.__result_dir + newName)

        res = []
        res.append(newName)
        res.append(self.__result_dir)

        return res
