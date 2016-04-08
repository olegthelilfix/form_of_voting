import io
import json

# from PIL import Image
# from ScanFormAPI import *

from beaker.middleware import SessionMiddleware
from cork import Cork

import bottle
from bottle import *
from uploadManager import UploadManager
from tokenContainer import TokenContainer

__author__ = 'vladthelittleone'

bottle.debug(True)

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('config', email_sender='vladthelittleone@gmail.com', smtp_url='smtp://smtp.magnet.ie')

# alias the authorization decorator with defaults
authorize = aaa.make_auth_decorator(fail_redirect="/auth", role="user")

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


# #  Bottle methods  # #

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


@post('/auth')
def auth():
    """Authenticate users"""
    username = request.json["username"].strip()
    password = request.json["password"].strip()

    if aaa.login(username, password):
        print("Auth success: " + username + ":" + password)
        return 'OK'
    else:
        print("Auth failed: " + username + ":" + password)
        return 'FAILED'

        # , success_redirect='/home', fail_redirect='/auth'


@route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'
    return 'False'


@route('/logout')
def logout():
    aaa.logout()


@route('/check_status')
@authorize()
def check_status():
    session = bottle.request.environ.get('beaker.session')
    result = []

    for tid in TokenContainer.get(session.get('username')):
        # result.append(getStatus(tid))
        result.append(tid)

    return json.dumps(result)


@route('/upload', method='POST')
@authorize()
def do_upload():
    session = bottle.request.environ.get('beaker.session')
    print("Session from simple_webapp", repr(session))

    req_img = request.files.get('file')

    # pil_image = Image.open(io.BytesIO(req_img.file))
    # id_token = generateIdToken()

    # UploadManager.submit(startScanForm, pil_image, id_token)
    # TokenContainer.add(session.get('username'), id_token)

    TokenContainer.add(session.get('username'), "asdasd")
    TokenContainer.add(session.get('username'), "asdasd")

    return "success"


# #  Web application main  # #

def main():
    # Start the Bottle webapp
    bottle.debug(True)
    bottle.run(host='localhost', port=8085, app=app, quiet=False, reloader=True)


if __name__ == "__main__":
    main()
