# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

from RenderHtml import RenderHtml
from weasyprint import HTML
import codecs

class PdfGen:
    __dirToProject = "/home/legionem/pychar/form_of_voting_gen/server/core/formgen/"
    __dir = __dirToProject + "result/htmlcode.html"
    __file_name = 'result.pdf'
    __result_dir = __dirToProject + "result/"

    def execute(self, id_user, id_meeting):
        render = RenderHtml(id_user, id_meeting, self.__dirToProject)
        value = render.split_question_on_pages()
        with codecs.open(self.__dir, 'w', 'utf8') as f2:
            f2.write(value)

        pdf = HTML(self.__dir)
        newName = str(id_user) + str(id_meeting) + self.__file_name
        pdf.write_pdf(self.__result_dir + newName)

        res = []
        res.append(newName)
        res.append(self.__result_dir)

        return res
