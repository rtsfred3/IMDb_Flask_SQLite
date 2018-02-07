#IMDb Flask App (using OMDb API & SQLite)
from flask import Flask, request, redirect, url_for, send_from_directory, Response, render_template, stream_with_context, send_file
import time, requests, sqlite3, os, os.path, shutil, json
import json as js
import settings
from imdb import *
from settings import *

app = Flask(__name__)

@app.route('/')
@app.route('/<imdbID>/')
def IMDb(imdbID='tt1839578'):
    filename = HTMLDir + imdbID + ".html"
    if os.path.isfile(filename) and (time.time() - os.path.getmtime(filename))/(86400) < fileAge:
        f = open(filename, "r")
        html = f.read()
        f.close()
    else:
        conn = sqlite3.connect(db_file)
        
        x = imdb(imdbID, conn)
        x.add_row()
        html = x.html()
        
        f = open(filename, "w")
        f.write(html)
        f.close()
        
        conn.close()
    return html

@app.route('/json/')
@app.route('/json/<imdbID>/')
def JSON(imdbID='tt1839578'):
    filename = JSONDir + imdbID + ".json"
    if os.path.isfile(filename) and (time.time() - os.path.getmtime(filename))/(86400) < fileAge:
        f = open(filename, "r")
        jsoon = f.read()
        f.close()
    else:
        conn = sqlite3.connect(db_file)
        
        x = imdb(imdbID, conn)
        x.add_row()
        jsoon = x.imdb_json()
        
        f = open(filename, "w")
        f.write(jsoon)
        f.close()        
        
        conn.close()
    
    resp = Response(jsoon, mimetype='application/json')
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

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

@app.route('/app.css')
@app.route('/app.min.css')
def css():
    return Response(settings.css, mimetype='text/css')

@app.route('/favicon.ico')
def favicon():
    return errors, 500

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return errors, 500

def generateTemplates():
    if os.path.exists(templateDir): shutil.rmtree(templateDir)
    if not os.path.exists(templateDir): os.makedirs(templateDir)
    
    f = open(templateDir+"/app.html", "w")
    f.write(templateHTML)
    f.close()

def main():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imdb (imdbID, title, year, released, rated, genres, actors, directors, writers, plot, rating, votes, type, poster, time)")
    conn.close()
    
    if os.path.exists(cacheDir):
        shutil.rmtree(cacheDir)
    
    if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)
    if not os.path.exists(HTMLDir):
        os.makedirs(HTMLDir)
    if not os.path.exists(JSONDir):
        os.makedirs(JSONDir)
    
    f = open(cacheDir+"/app.css", "w")
    f.write(settings.css)
    f.close()
    
    #generateTemplates()
    
    return app.run('0.0.0.0')

if __name__ == '__main__':
    main()