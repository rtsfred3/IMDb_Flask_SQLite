import re, time, json, sqlite3, urllib.request, pymysql.cursors

m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
errors = '<center>The location you are looking for is not here, please try again.</center>'
css = "<style>html, body, div, span, h1, h2, p, pre, a, em, img, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, ol, ul, li, fieldset, form, label, legend, table, tr, th, td, embed, header, menu { margin: 0; padding: 0; border: 0; font-size: 100%; font: inherit; vertical-align: baseline; outline: none; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; } html { overflow-y: scroll; } body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 62.5%; line-height: 1; margin-bottom: 35px; margin-top: 20px; color: #555; background: gray; } br { display: block; line-height: 1.6em; } header { display: block; } ol, ul { list-style: none; } table { border-collapse: collapse; border-spacing: 0; } img { border: 0; max-width: 100%; width: 225px; } a { color: #3d6abc; } a:hover { color: #6387c7; } h2 {font-size: 2.7em; line-height: 1.4em; font-weight: bold; margin-bottom: 8px; color: #444; } p { font-size: 1.4em; line-height: 1.15em; margin-bottom: 15px; } p.genre { font-size: 1.2em; color: #777; font-style: italic; margin-bottom: 12.5px; } #w { display: block; width: 750px; margin: 0 auto; padding: 12px; background: white; -webkit-box-shadow: 1px 2px 1px rgba(0,0,0,0.35); -moz-box-shadow: 1px 2px 1px rgba(0,0,0,0.35); box-shadow: 1px 2px 1px rgba(0,0,0,0.35); } #imdbcontents { display: block; width: 100%; } .floatright { display: block; float: right; margin-left: 10px; margin-bottom: 5px; } .clearfix:after { content: \".\"; display: block; clear: both; visibility: hidden; line-height: 0; height: 0; } .clearfix { display: inline-block; } html[xmlns] .clearfix { display: block; } * html .clearfix { height: 1%; }</style>"

checkIMDb = lambda i: (len(i) == 9) and (re.search('^tt\d{7}$', i) != None)

def imdb_type(t):
    if t == 'tv_series' or t == 'tv_episode' or t == 'video_game':
        return t.replace('tv_', '').replace('video_', '')
    elif t == 'feature':
        return 'movie'
    elif t == 'short':
        return t
    else:
        return 'unknown'

def arrJoin(arr, ver=None, out=''):
    for i in range(0,len(arr)):
        if i == (len(arr) - 1):
            if ver == 'w':
                out += arr[i]['name']['name'].replace('&','').strip() + ' ' + arr[i]['attr'].replace('&','').strip()
            else:
                out += arr[i]['name']['name'].replace('&','').strip()
        else:
            if ver == 'w':
                out += arr[i]['name']['name'].replace('&','').strip() + ' ' + arr[i]['attr'].replace('&','').strip() + ', '
            else:
                out += arr[i]['name']['name'].replace('&','').strip() + ', '
    return out.replace(' and,',',').replace('...','').replace('"','&quot;').replace("'","&#39;")

class imdb:
    insert = ''
    
    def __init__(self, imdbID, conn):
        if not checkIMDb(imdbID):
            raise Exception('Not valid IMDb ID' + imdbID)
        self.imdbID = imdbID
        self.conn = conn
    
    #Searches the main table (imdb) for the imdbID and returns false if it is there and true if it is not there.
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
            self.fromIMDb()
            c.execute("INSERT INTO imdb VALUES (" + self.insert + str(int(time.time())) + "')")
            self.conn.commit()
        elif self.search(c) == False:
            c.execute("SELECT * FROM imdb WHERE imdbID='" + self.imdbID + "'")
            for row in c:
                if (time.time() - float(row[14]))/86400 > 3:
                    data = json.loads(self.fromIMDb())
                    c.execute("UPDATE imdb SET rating='" + data['Rating'] + "', votes='" + data['Votes'] + "', time='" + str(int(time.time())) + "' WHERE imdbID='" + self.imdbID + "'")
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
                
                head = '<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<title>' + row[1] + ' (' + row[2] + ')</title>\n\t\t' + css + '\n\t</head>\n\t<body>'
                main = '\n\t\t<div id="w" class="clearfix">\n\t\t\t<img src="../img/%s/" width="225px" class="floatright">\n\t\t\t<h2>%s</h2>\n\t\t\t<p class="genre">%s | %s | %s | %s |  %s based on %s votes</p>\n\t\t\t<p>%s</p>\n\t\t\t<p><a href="http://imdb.com/title/%s/" target=\"_blank\">View on IMDb &rarr;</a></p>\n\t\t</div>' % (row[0],row[1], media, row[2], row[4], row[5], str(row[10]), str(row[11]), row[9], row[0])
                break
        
        return head + main + '\n\t</body>\n</html>'
    
    #Provides a sitemap for the website
    def sitemap(self, url=None, main=''):
        #conn = pymysql.connect(host='localhost', port=8889, user='imdb', password='movie', db='imdb')
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
    
    #Good luck trying to figure this out
    #Scrapes IMDb's (semi-official) api then puts it in a format to be put into the database
    def fromIMDb(self):
        url = 'https://app.imdb.com/title/maindetails?tconst=' + self.imdbID
        req = urllib.request.Request(url, None, { 'User-Agent': 'IMDb Flask Website v' + str(0.1) })
        response = urllib.request.urlopen(req)
        if response.getcode() != 200:
            return False
        
        data = json.loads(response.read().decode('utf-8'))['data']
        title = data['title'].replace('"','&quot;').replace("'","&#39;")
        
        try:
            rating = str(data['rating'])
            numVotes = str("{:,}".format(int(data['num_votes'])))
        except:
            rating, numVotes = 'N/A', 'N/A'
        
        try:
            poster = data['image']['url'].replace('http://','https://')
        except:
            poster = 'N/A'
        
        year = data['year']
        if year == '????':
            year = 'N/A'
        
        if imdb_type(data['type']) == 'series':
            try:
                if data['year'] == data['year_end']:
                    year = year
                elif data['year_end'] == '????':
                    year += '-'
                elif data['year_end'] != '????':
                    year = str(data['year']) + '-' + str(data['year_end'])
            except:
                pass
        
        try:
            rated = data['certificate']['certificate']
        except:
            rated = 'N/A'
        
        if imdb_type(data['type']) != 'series':
            try:
                d = str(data['release_date']['normal'])
                released = d[8:] + ' ' + m[int(d[5:7]) - 1] + ' ' + d[:4]
                
                if year == 'N/A':
                    year = released[-4:]
            except:
                released = 'N/A'
        
        if imdb_type(data['type']) == 'series':
            released = year[:4]
        
        if year == 'N/A' and released != 'N/A' and imdb_type(data['type']) != 'series':
            year = released[-4:]
        
        if year != 'N/A' and released == 'N/A' and imdb_type(data['type']) != 'series':
            released = year[:4]
        
        try:
            try:
                plot = data['best_plot']['summary']
            except:
                plot = data['best_plot']['outline']
        except:
            try:
                plot = data['plot']['outline']
            except:
                plot = 'N/A'
        
        plot = plot.replace('"','&quot;').replace("'","&#39;")
        
        genres = 'N/A'
        if len(data['genres']) > 0:
            genres = ', '.join(data['genres'])
            
        try:
            writers = arrJoin(data['writers_summary'], 'w')
        except:
            writers = 'N/A'
        
        try:
            directors = arrJoin(data['directors_summary'])
        except:
            directors = 'N/A'
        
        try:
            actors = arrJoin(data['cast_summary'])
        except:
            actors = 'N/A'
        
        main = '{"Title":"' + title + '","Year":"' + year + '","Released":"' + released + '","Rated":"' + rated + '","Actors":"' + actors + '","Directors":"' + directors.replace('"', '&quot;') + '","Writers":"' + writers + '","Genres":"' + genres + '","Plot":"' + plot + '","Rating":"' + str(rating) + '","Votes":"' + str(numVotes) + '","Type":"' + imdb_type(data['type']) + '","imdbID":"' + self.imdbID + '","Poster":"' + poster + '"}'
        
        self.insert = "'" + self.imdbID + "','" + title + "','" + year + "','" + released + "','" + str(rated) + "','" + genres + "','" + actors + "','" + directors + "','" + writers + "','" + plot + "','" + str(rating) + "','" + str(numVotes) + "','" + imdb_type(data['type']) + "','" + poster + "','"
        
        self.insert = self.insert.replace('û','&ucirc;').replace('Ô','&Ocirc;').replace('ô','&ocirc;').replace('é','&eacute;').replace('î','&icirc;')
        self.insert = self.insert.replace('â','&acirc;').replace('ü','&uuml;').replace('ä','&auml;').replace('è','&egrave;').replace('ñ','&ntilde;').replace('-','-')
        self.insert = self.insert.replace('·','&middot;').replace('ĂŠ','&eacute;').replace('Ă´','&ocirc;').replace('Ã´','&ocirc;').replace('Ăť','&ocirc;')
        self.insert = self.insert.replace('Ă','&Ocirc;').replace('Ă','').replace('รป','&ucirc;').replace('','&Eacute;').replace('É','&Eacute;')
        self.insert = self.insert.replace('Ž','&icirc;')
        
        return main

def test(imdbID="tt1839578"):
    #conn = pymysql.connect(host='localhost', port=8889, user='imdb', password='movie', db='imdb')
    conn = sqlite3.connect('imdb.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imdb (imdbID MEDIUMTEXT, title MEDIUMTEXT, year MEDIUMTEXT, released MEDIUMTEXT, rated MEDIUMTEXT, genres MEDIUMTEXT, actors MEDIUMTEXT, directors MEDIUMTEXT, writers MEDIUMTEXT, plot MEDIUMTEXT, rating MEDIUMTEXT, votes MEDIUMTEXT, type MEDIUMTEXT, poster MEDIUMTEXT, time MEDIUMTEXT)")

    start = time.time()
    x = imdb(imdbID, conn)
    x.add_row()
    print(x.html())
    totalTime = time.time() - start
    print(str(totalTime) + " seconds")
    
    conn.close()
    return

#test("tt0113568")