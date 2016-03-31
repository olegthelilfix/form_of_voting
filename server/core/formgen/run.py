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

@get('/') # or @route('/login')
def login():
    return '''
        <form action="/" method="post">
            <p>UserID: <input name="p1" type="text" /></p>
            <p>MeetingID: <input name="p2" type="text" /></p>
            <input value="Send" type="submit" />
        </form>
    '''

@post('/') # or @route('/login', method='POST')
def do_login():
    global mutex
    global pg

    def getForm(name):
        return int(request.forms.get(name))

    while mutex:
        pass

    mutex = True

    os.system("rm -R " + settings.DIR_TO_PROJECT + "result/img")
    #os.mkdir(settings.DIR_TO_PROJECT + "result")
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
