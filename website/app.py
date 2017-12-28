#IMDb Flask App (using IMDb API & SQLite)
from flask import Flask, request, redirect, url_for, send_from_directory, Response, render_template, stream_with_context, send_file
import time, urllib, sqlite3, pymysql.cursors
from imdb import *

app = Flask(__name__)

db_file = '../imdb.db'

@app.route('/')
@app.route('/<imdbID>/')
def IMDb(imdbID='tt1839578'):
    conn = sqlite3.connect(db_file)
    
    x = imdb(imdbID, conn)
    x.add_row()
    html = x.html()
    
    conn.close()
    return html

@app.route('/json/')
@app.route('/json/<imdbID>/')
def JSON(imdbID='tt1839578'):
    conn = sqlite3.connect(db_file)
    
    x = imdb(imdbID, conn)
    x.add_row()
    resp = Response(x.imdb_json(), mimetype='application/json')
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    
    conn.close()
    return resp

@app.route('/img/<imdbID>/')
def img(imdbID):
    conn = sqlite3.connect(db_file)
    
    url = imdb(imdbID, conn).poster()
    req = urllib.request.urlopen(urllib.request.Request(url))
    
    conn.close()
    return Response(req, content_type=req.headers['content-type'])

@app.route('/sitemap.xml')
def sitemap():
    conn = sqlite3.connect(db_file)
    return Response(imdb('tt1839578', conn).sitemap(request.url_root), mimetype='application/xml')

@app.route('/favicon.ico')
def favicon():
    return errors, 500

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return errors, 500

def main():
    conn = sqlite3.connect(db_file)    
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imdb (imdbID MEDIUMTEXT, title MEDIUMTEXT, year MEDIUMTEXT, released MEDIUMTEXT, rated MEDIUMTEXT, genres MEDIUMTEXT, actors MEDIUMTEXT, directors MEDIUMTEXT, writers MEDIUMTEXT, plot MEDIUMTEXT, rating MEDIUMTEXT, votes MEDIUMTEXT, type MEDIUMTEXT, poster MEDIUMTEXT, time MEDIUMTEXT)")
    conn.close()
    
    return app.run('0.0.0.0')

if __name__ == '__main__':
    main()