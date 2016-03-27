
import bottle

from bottle import *
from PdfGen import PdfGen
import os
import settings

bottle.debug(True)

app = bottle.app()

mutex = False

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
    while mutex :
        print ("wait")
    os.system("rm -R " + settings.DIR_TO_PROJECT + "result")
    os.mkdir(settings.DIR_TO_PROJECT + "result")
    os.mkdir(settings.DIR_TO_PROJECT + "result/img")
    mutex = True
    pg = PdfGen()
    p1 = request.forms.get('p1')
    p2 = request.forms.get('p2')
    res = pg.execute(int(p1), int(p2))
    mutex = False
    return bottle.static_file(res[0], res[1])

# #  Web application main  # #

def main():
    # Start the Bottle webapp
    bottle.debug(True)
    bottle.default_app()
    bottle.run(host='localhost', port=8080, app=app, quiet=False, reloader=True)

if __name__ == "__main__":
    main()
