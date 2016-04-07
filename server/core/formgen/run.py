# -*- coding: utf8 -*-
__author__ = 'Aleksandrov Oleg, 4231'

import bottle
from bottle import *
from PdfGen import PdfGen
import os
import settings

bottle.debug(True)

app = bottle.app()

mutex = False
pg = PdfGen()
css = '''
    .fio {
        font-size: 20px;
        font-weight: bold;
    }

    .address {
        font-size: 16px;
        font-weight: bold;
    }

    .street {
        font-size: 10px;
    }

    .houseNumb {
        font-size: 10px;
    }

    .apartment {
        font-size: 10px;
    }

    .formSeries {
        font-size: 10px;
    }

    .formDateOfIssue{
        font-size: 10px;
    }

    .propertyS {
        font-size: 10px;
    }

    .share {
        font-size: 10px;
    }

    .phoneNumber {
        font-size: 10px;
    }

    .head {
        font-size: 10px;
    }

    .title {
        text-align: center;
        font-size: 20px;
    }
      '''
qs = " "


@get('/edit')
def edit():
    global css
    global qs
    return template(settings.DIR_TO_PROJECT + 'template/edit.html', css=css, qs=qs[0])


@post('/edit')
def do_edit():
    def getForm(name):
        return request.forms.get(name)

    os.system("rm -R " + settings.DIR_TO_PROJECT + "result/img")
    # os.mkdir(settings.DIR_TO_PROJECT + "result")
    os.mkdir(settings.DIR_TO_PROJECT + "result/img")

    new_css = str(getForm('css'))
    new_qs = [str(getForm('qs'))]
    p1 = int(getForm('p1'))
    p2 = int(getForm('p2'))

    if len(new_qs[0]) < 2 and len(new_css) < 2:
        res = pg.execute(p1, p2)
    elif len(new_qs[0]) < 2:
        res = pg.execute(p1, p2, css=new_css)
    elif len(new_css) < 2:
        res = pg.execute(p1, p2, qs=new_qs)
    else:
        res = pg.execute(p1, p2, qs=new_qs, css=new_css)

    result = bottle.static_file(res[0], res[1])

    global css
    global qs
    qs = new_qs
    css = new_css

    return result


@get('/')  # or @route('/login')
def login():
    return template(settings.DIR_TO_PROJECT + 'template/main.html')


@post('/')  # or @route('/login', method='POST')
def do_login():
    global mutex
    global pg

    def getForm(name):
        return int(request.forms.get(name))

    while mutex:
        pass

    mutex = True

    os.system("rm -R " + settings.DIR_TO_PROJECT + "result/img")
    # os.mkdir(settings.DIR_TO_PROJECT + "result")
    os.mkdir(settings.DIR_TO_PROJECT + "result/img")

    res = pg.execute(getForm('p1'), getForm('p2'))
    result = bottle.static_file(res[0], res[1])

    mutex = False

    return result


# #  Web application main  # #

def main():
    # Start the Bottle webapp
    bottle.debug(True)
    bottle.default_app()
    bottle.run(host=settings.RUN_HOST, port=settings.RUN_PORT, app=app, quiet=False, reloader=True)


if __name__ == "__main__":
    main()
