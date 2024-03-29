import os, os.path, shutil, sqlite3
from settings import *

def makeDB():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imdb (imdbID, title, year, released, rated, genres, actors, directors, writers, plot, rating, votes, type, poster, time)")
    conn.close()

def generateStatic(html=True, json=True):
    if os.path.exists(cacheDir): shutil.rmtree(cacheDir)
    
    if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)
    if not os.path.exists(HTMLDir) and html:
        os.makedirs(HTMLDir)
    if not os.path.exists(JSONDir) and json:
        os.makedirs(JSONDir)
    
    f = open(cacheDir+"/app.css", "w")
    f.write(css)
    f.close()
    
    f = open(cacheDir+"/imdb.js", "w")
    f.write(script)
    f.close()

def generateTemplates(app=False, query=False):
    if os.path.exists(templateDir): shutil.rmtree(templateDir)
    if not os.path.exists(templateDir): os.makedirs(templateDir)
    
    if app:
        f = open(templateDir+"/app.html", "w")
        f.write(templateHTML)
        f.close()
    
    if query:
        f = open(templateDir+"/jquery.html", "w")
        f.write(templateAltHTML)
        f.close()
        
        f = open(cacheDir+"/imdb.js", "w")
        f.write(script)
        f.close()

generateTemplates(app=True)