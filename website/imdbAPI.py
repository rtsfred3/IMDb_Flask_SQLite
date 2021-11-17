#Gets and Parses data from OMDb API and presents data as part of a class
import requests
import settings

class IMDbAPI:
    def __init__(self, imdbID):
        self.imdbID = imdbID
        self.url = settings.baseURL + '&i={}&plot=full'.format(imdbID)# + imdbID + '&plot=full'
        self.r = requests.get(self.url, headers={ 'User-Agent': 'IMDb Flask Website v' + str(0.1) })
        self.data = self.r.json()
        
        print(self.url)
        
        self.title = self.data['Title'].replace("'", '&#39;')
        self.year = self.data['Year']
        self.released = self.data['Released']
        self.rated = self.data['Rated']
        
        self.genre = self.data['Genre']
        self.actors = self.data['Actors'].replace("'", '&#39;')
        self.writers = self.data['Writer'].replace('"', '&quot;').replace('...', '')
        self.directors = self.data['Director'].replace('"', '&quot;')
        
        self.plot = self.data['Plot'].replace("'", '&#39;').replace('"', '&quot;')
        self.Type = self.data['Type']
        self.rating = self.data['imdbRating']
        self.numVotes = self.data['imdbVotes']
        self.poster = self.data['Poster'].replace("http://", "https://")
    
    def getJSON(self):
        return '{"Title":"%s","Year":"%s","Released":"%s","Rated":"%s","Actors":"%s","Directors":"%s","Writers":"%s","Genres":"%s","Plot":"%s","Rating":"%s","Votes":"%s","Type":"%s","imdbID":"%s","Poster":"%s"}' % (self.title, self.year, self.released, self.rated, self.actors, self.directors, self.writers, self.genre, self.plot, self.rating, self.numVotes, self.Type, self.imdbID, self.poster)
    
    def getDetailedJSON(self):
        #return '{"Title":"%s","Year":"%s","Released":"%s","Rated":"%s","Actors":"%s","Directors":"%s","Writers":"%s","Genres":"%s","Plot":"%s","Rating":"%s","Votes":"%s","Type":"%s","imdbID":"%s","Poster":"%s"}' % (self.title, self.year, self.released, self.rated, self.actors, self.directors, self.writers, self.genre, self.plot, self.rating, self.numVotes, self.Type, self.imdbID, self.poster)
        
        return {
            "Title": self.title,
            "Year": self.year,
            "Released": self.released,
            "Rated": self.rated,
            "Actors": [person.strip() for person in self.actors.split(',')] if self.actors != 'N/A' else [],
            "Directors": [person.strip() for person in self.directors.split(',')] if self.directors != 'N/A' else [],
            "Writers": [person.strip() for person in self.writers.split(',')] if self.writers != 'N/A' else [],
            "Genres": "%s",
            "Plot": self.plot,
            "Rating": self.rating,
            "Votes": self.numVotes,
            "Type": self.Type,
            "imdbID": self.imdbID,
            "Poster": self.poster
        }
    
    def getSQL(self):
        insert = "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','" % (self.imdbID, self.title, self.year, self.released, self.rated, self.genre, self.actors, self.directors, self.writers, self.plot, self.rating, self.numVotes, self.Type, self.poster)
        
        insert = insert.replace('û','&ucirc;').replace('Ô','&Ocirc;').replace('ô','&ocirc;').replace('é','&eacute;').replace('î','&icirc;')
        insert = insert.replace('â','&acirc;').replace('ü','&uuml;').replace('ä','&auml;').replace('è','&egrave;').replace('ñ','&ntilde;').replace('-','-')
        insert = insert.replace('·','&middot;').replace('ĂŠ','&eacute;').replace('Ă´','&ocirc;').replace('Ã´','&ocirc;').replace('Ăť','&ocirc;')
        insert = insert.replace('Ă','&Ocirc;').replace('Ă','').replace('รป','&ucirc;').replace('','&Eacute;').replace('É','&Eacute;')
        insert = insert.replace('Ž','&icirc;')
        
        return insert

def test():
    api = IMDbAPI('tt1839578')
    print(api.getDetailedJSON())

if __name__ == '__main__':
    test()