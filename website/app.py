#IMDb Flask App (using OMDb API & SQLite)
#Calls Database to get HTML & JSON data
from flask import Flask, request, redirect, url_for, send_from_directory, Response, render_template, stream_with_context, send_file
import time, requests, sqlite3, os, os.path, shutil

from imdb import *
from settings import *
from generateStatic import *

app = Flask(__name__)

@app.route('/')
@app.route('/<imdbID>/')
def IMDb(imdbID='tt1839578'):
    conn = sqlite3.connect(db_file)
    
    x = imdb(imdbID, conn)
    x.add_row()
    html = x.altHTML()
    
    conn.close()
    return html

@app.route('/json/')
@app.route('/json/<imdbID>/')
@app.route('/json/<imdbID>.json')
def JSON(imdbID='tt1839578'):
    conn = sqlite3.connect(db_file)
    
    x = imdb(imdbID, conn)
    x.add_row()
    
    req = Response(x.imdb_json(), mimetype='application/json')
    req.headers['Access-Control-Allow-Origin'] = '*'
    req.headers['Cache-Control'] = 'max-age=7200'
    
    conn.close()
    return req

@app.route('/img/')
@app.route('/img/<imdbID>/')
def img(imdbID=None):
    conn = sqlite3.connect(db_file)
    
    if imdbID != None:
        url = imdb(imdbID, conn).poster()
    else:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/ProhibitionSign2.svg/1200px-ProhibitionSign2.svg.png"
    req = requests.get(url)
    
    conn.close()
    return Response(req, content_type=req.headers['content-type'])

@app.route('/favicon.ico')
def favicon():
    req = requests.get("https://m.media-amazon.com/images/G/01/imdb/images/favicon-2165806970._CB499613556_.ico")
    return Response(req, content_type=req.headers['content-type'])

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return errors, 500

def main():
    if apiKey == "":
        print("Missing API Key")
        return 0
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imdb (imdbID, title, year, released, rated, genres, actors, directors, writers, plot, rating, votes, type, poster, time)")
    conn.close()
    
    generateStatic(False, False)
    #generateTemplates()
    
    return app.run('0.0.0.0')

if __name__ == '__main__':
    main()