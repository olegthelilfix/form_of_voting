__author__ = 'vladthelittleone'

from bottle import *
import os

@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@route('/upload', method='POST')
def do_upload():
    image = request.files.get('file')
    destination = '/Users/vladthelittleone/IdeaProjects/form_of_voting_gen/server/bottle-server'

    if os.path.isdir(destination):
        destination = os.path.join(destination, image.filename)

    if not os.path.exists(destination):
        image.save(destination)
    else:
        print "Error: Image already upload"

    return "Image successfully uploaded"

run(host='localhost', port=8085, debug=True)
