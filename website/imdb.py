import re, time, json, sqlite3
import imdbAPI, settings

m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
css = "<link rel=\"stylesheet\" href=\"/static/app.css\">"

checkIMDb = lambda i: (len(i) == 9) and (re.search('^tt\d{7}$', i) != None)

class imdb:
    insert = ''
    
    def __init__(self, imdbID, conn):
        if not checkIMDb(imdbID):
            raise Exception('Not valid IMDb ID' + imdbID)
        self.imdbID = imdbID
        self.conn = conn
    
    #Searches the main table (imdb) for the imdbID and returns false if it is there and true if it is not there
    def search(self, c):
        c.execute("SELECT imdbID FROM imdb")
        for row in c:
            if row[0] == self.imdbID:
                return False
        return True
    
    #Deletes the selected imdbID
    def delete(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM imdb WHERE imdbID='" + self.imdbID + "'")
        self.conn.commit()
    
    def checkAge(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM imdb WHERE imdbID='" + self.imdbID + "'")
        for row in c:
            if row[0] == self.imdbID:
                return (time.time() - float(row[14]))/86400
    
    #Adds the imdbID and all relevant information to the database.
    def add_row(self):
        c = self.conn.cursor()
        if self.search(c):
            #self.fromIMDb()
            imdbInfo = imdbAPI.IMDbAPI(self.imdbID)
            c.execute("INSERT INTO imdb VALUES (" + imdbInfo.getSQL() + str(int(time.time())) + "')")
            self.conn.commit()
        elif self.search(c) == False:
            c.execute("SELECT * FROM imdb WHERE imdbID='" + self.imdbID + "'")
            for row in c:
                if (time.time() - float(row[14]))/86400 > settings.dbAge:
                    imdbInfo = imdbAPI.IMDbAPI(self.imdbID)
                    c.execute("UPDATE imdb SET rating='" + imdbInfo.rating + "', votes='" + imdbInfo.numVotes + "', time='" + str(int(time.time())) + "' WHERE imdbID='" + self.imdbID + "'")
                    self.conn.commit()
    
    #Returns the poster of imdbID from the database to be displayed to the visitor.
    def poster(self, conn=None):
        c = self.conn.cursor()
        c.execute("SELECT imdbID, poster FROM imdb WHERE imdbID='" + self.imdbID + "'")
        for row in c:
            if row[0] == self.imdbID:
                main = row[1]
                break
        return main
    
    #Outputs all relevant information from the database in JSON format
    def imdb_json(self, main=""):
        c = self.conn.cursor()
        c.execute("SELECT * FROM imdb WHERE imdbID='" + self.imdbID + "'")
        for row in c:
            if row[0] == self.imdbID:
                main = '{"Title":"%s","Year":"%s","Released":"%s","Rated":"%s","Actors":"%s","Directors":"%s","Writers":"%s","Genres":"%s","Plot":"%s","Rating":"%s","Votes":"%s","Type":"%s","imdbID":"%s","Poster":"%s"}' % (row[1], row[2], row[3], row[4], row[6], row[7], row[8], row[5], row[9], row[10], row[11], row[12], row[0], row[13])
                break
        return main
    
    #Outputs all relevant information from the database in HTML format
    def html(self, head="", main=""):
        global css
        c = self.conn.cursor()
        c.execute("SELECT * FROM imdb WHERE imdbID='" + self.imdbID + "'")
        for row in c:
            if row[0] == self.imdbID:
                media = row[12].capitalize()
                if row[12] == 'series':
                    media = 'TV'
                
                ident = "<!--%s-->\n" % row[0]
                head = ident + '<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<title>' + row[1] + ' (' + row[2] + ')</title>\n\t\t' + css + '\n\t</head>\n\t<body>'
                main = '\n\t\t<div id="w" class="clearfix">\n\t\t\t<img src="../img/%s/" width="225px" class="floatright">\n\t\t\t<h2>%s</h2>\n\t\t\t<p class="genre">%s | %s | %s | %s |  %s based on %s votes</p>\n\t\t\t<p>%s</p>\n\t\t\t<p><a href="http://imdb.com/title/%s/" target=\"_blank\">View on IMDb &rarr;</a></p>\n\t\t</div>' % (row[0],row[1], media, row[2], row[4], row[5], str(row[10]), str(row[11]), row[9], row[0])
                break
        
        return head + main + '\n\t</body>\n</html>'
    
    #Provides a sitemap for the website
    def sitemap(self, url=None, main=''):
        c = self.conn.cursor()    
        c.execute("SELECT * FROM imdb")
        
        if url is None:
            a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            a.connect(("8.8.8.8", 80))
            url = 'http://' + a.getsockname()[0] + ':5000/'
        
        for row in c:
            main += '\n\t<url>\n\t\t<loc>' + url + row[0] + '/</loc>\n\t</url>'
        self.conn.close()
        return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset>\n\t<url>\n\t\t<loc>' + url + '</loc>\n\t</url>' + main + '\n</urlset>'
    
    #Gets information OMDb API then puts it in a format to be put into the database
    def fromIMDb(self):
        imdbInfo = imdbAPI.IMDbAPI(self.imdbID)
        self.insert = imdbInfo.getSQL()
        return imdbInfo.getJSON()

def test(imdbID="tt1839578"):
    conn = sqlite3.connect('imdb.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imdb (imdbID, title, year, released, rated, genres, actors, directors, writers, plot, rating, votes, type, poster, time)")

    start = time.time()
    x = imdb(imdbID, conn)
    x.add_row()
    print(x.html())
    totalTime = time.time() - start
    print(str(totalTime) + " seconds")
    
    conn.close()
    return