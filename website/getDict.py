import os, time, json, sqlite3
import imdb, imdbAPI
from settings import *

#Adds & Updates IMDb ID's when called
def appendToDict(imdbID, imdbDict):
    if (not imdbID in imdbDict) or (imdbID in imdbDict and (time.time() - imdbDict[imdbID]["time"])/60 > dictAge):
        conn = sqlite3.connect(db_file)
        x = imdb.imdb(imdbID, conn)
        x.add_row()
        
        imdbDict[imdbID] = {"html": x.html(), "json":json.loads(x.imdb_json()), "time":time.time()}
        conn.close()
        
        if __name__ == '__main__':
            if not imdbID in imdbDict: print(imdbID, "was added")
            else: print(imdbID, "was updated")

#Loads database into a dictionary
def loadDBtoDict(dbDict={}):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT imdbID FROM imdb")
    for row in c:
        x = imdb.imdb(row[0], conn)
        x.add_row()
        
        dbDict[row[0]] = {"html": x.html(), "json":json.loads(x.imdb_json()), "time":time.time()}
    
    conn.close()
    return dbDict

def testHTML(file):
    start = time.time()
    
    f = open(file, "r")
    html = f.read()
    f.close()
    
    totalTime = time.time() - start
    print("File took:", totalTime, "seconds")
    return totalTime

def testDict(dbDict, imdbID):
    start = time.time()
    
    html = dbDict[imdbID]['html']
    
    totalTime = time.time() - start
    print("Dict took:", totalTime, "seconds")
    return totalTime

def testDB(imdbID):
    start = time.time()
    
    conn = sqlite3.connect(db_file)
    x = imdb.imdb(imdbID, conn)
    x.add_row()
    html = x.html()
    conn.close()
    
    totalTime = time.time() - start
    print("DB took:", totalTime, "seconds")
    return totalTime

def main():
    dbDict = loadDBtoDict()
    
    imdbID = "tt1839578"
    fname = imdbID+".html"
    
    conn = sqlite3.connect(db_file)
    x = imdb.imdb(imdbID, conn)
    x.add_row()
    html = str(x.html().encode('utf8'))#.replace("-","&minus;").replace("=","&equals;")
    conn.close()
    
    f = open(fname, 'w')
    f.write(html)
    f.close()
    
    fileSpeed = testHTML(fname)
    dictSpeed = testDict(dbDict, imdbID)
    dbSpeed = testDB(imdbID)
    
    print()
    print("Dict is", round(dbSpeed/dictSpeed, 5), "times faster than using the Database")
    print("Dict is", round(fileSpeed/dictSpeed, 5), "times faster than an HTML file")
    
    print("Database is", round(fileSpeed/dbSpeed, 5), "times faster than an HTML file")
    
    os.remove(fname)

if __name__ == '__main__':
    main()