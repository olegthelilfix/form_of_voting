
import bottle

from bottle import *
from beaker.middleware import SessionMiddleware

from cork import Cork

from PdfGen import PdfGen

bottle.debug(True)

app = bottle.app()

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'voting',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = SessionMiddleware(app, session_opts)

@route('/')
def static():
    pg = PdfGen()
    res = pg.execute(11, 9)
    return bottle.static_file(res[0], res[1])


# #  Web application main  # #

def main():

    # Start the Bottle webapp
    bottle.debug(True)
    bottle.default_app()
    bottle.run(host='localhost', port=8085, app=app, quiet=False, reloader=True)

if __name__ == "__main__":
    main()
