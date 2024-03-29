#IMDb Flask App (using OMDb API & SQLite)
#Uses a dict to cache HTML & JSON data
from flask import Flask, request, redirect, url_for, send_from_directory, Response, render_template, stream_with_context, send_file
import time, requests, sqlite3, os, os.path, shutil

import getDict
from imdb import *
from settings import *
from generateStatic import *

makeDB()
imdbDict = getDict.loadDBtoDict()

app = Flask(__name__)

@app.route('/')
@app.route('/<imdbID>/')
def IMDb(imdbID='tt1839578'):
    getDict.appendToDict(imdbID, imdbDict)
    return imdbDict[imdbID]['html']

@app.route('/json/')
@app.route('/json/<imdbID>/')
def JSON(imdbID='tt1839578'):
    getDict.appendToDict(imdbID, imdbDict)
    
    resp = Response(imdbDict[imdbID]['json'], mimetype='application/json')
    return resp

@app.route('/img/')
@app.route('/img/<imdbID>/')
def img(imdbID=None):
    if imdbID != None:
        url = imdbDict[imdbID]['json']['Poster']
    else:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/ProhibitionSign2.svg/1200px-ProhibitionSign2.svg.png"
    req = requests.get(url)
    return Response(req, content_type=req.headers['content-type'])

@app.route('/favicon.ico')
def favicon():
    return errors, 500

@app.route('/hello')
def E451():
    return "<html><head><title>Unavailable For Legal Reasons</title></head><body><h1>Unavailable For Legal Reasons</h1><p>This request may not be serviced in the Roman Province of Judea due to the Lex Julia Majestatis, which disallows access to resources hosted on servers deemed to be operated by the People's Front of Judea.</p></body></html>", 451

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return errors, 500

def main():
    if apiKey == "":
        print("Missing API Key")
        return 0
    
    generateStatic(False, False)
    return app.run('0.0.0.0')

if __name__ == '__main__':
    main()
