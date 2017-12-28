#Gets and Parses data from IMDb's unofficial API and
#presents data as part of a class
import requests

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

class IMDbAPI:
    def __init__(self, imdbID):
        self.url = 'https://app.imdb.com/title/maindetails?tconst=' + imdbID
        self.r = requests.get(self.url, headers={ 'User-Agent': 'IMDb Flask Website v' + str(0.1) })
        self.data = self.r.json()['data']
        
        
        self.title = self.data['title'].replace('"','&quot;').replace("'","&#39;")
        self.year = self.year()
        self.released = self.released()
        self.rated = self.data['certificate']['certificate'] if 'certificate' in self.data else 'N/A'
        self.genres = ', '.join(self.data['genres']) if 'genres' in self.data and len(self.data['genres']) > 0 else 'N/A'
        self.actors = arrJoin(self.data['cast_summary']) if 'cast_summary' in self.data else 'N/A'
        self.writers = arrJoin(self.data['writers_summary'], 'w') if 'writers_summary' in self.data else 'N/A'
        self.directors = arrJoin(self.data['directors_summary']) if 'directors_summary' in self.data else 'N/A'
        self.plot = self.plot()
        self.type = imdb_type(self.data['type'])
        self.rating = str(self.data['rating']) if 'rating' in self.data else 'N/A'
        self.numVotes = str("{:,}".format(int(self.data['num_votes']))) if 'num_votes' in self.data else 'N/A'
        self.poster = self.data['image']['url'].replace('http://','https://') if 'image' in self.data else 'N/A'
    
    def year(self):
        year = self.data['year']
        if year == '????':
            year = 'N/A'
            
        if imdb_type(self.data['type']) == 'series':
            if 'year' in self.data and 'year_end' in self.data:
                if self.data['year'] == self.data['year_end']:
                    year = year
                elif self.data['year_end'] == '????':
                    year += '-'
                elif self.data['year_end'] != '????':
                    year = str(self.data['year']) + '-' + str(self.data['year_end'])
            else:
                year = 'N/A'
        return year
    
    def released(self):
        released = ''
        if imdb_type(self.data['type']) != 'series':
            try:
                d = str(self.data['release_date']['normal'])
                released = d[8:] + ' ' + m[int(d[5:7]) - 1] + ' ' + d[:4]
                
                if self.year == 'N/A':
                    self.year = released[-4:]
            except:
                released = 'N/A'
            
        if imdb_type(self.data['type']) == 'series':
            released = self.year[:4]
    
        if self.year == 'N/A' and released != 'N/A' and imdb_type(self.data['type']) != 'series':
            self.year = released[-4:]
                
        if self.year != 'N/A' and released == 'N/A' and imdb_type(self.data['type']) != 'series':
            released = self.year[:4]
        
        return released
    
    def plot(self):
        if 'best_plot' in self.data:
            if 'summary' in self.data['best_plot']:
                plot = self.data['best_plot']['summary']
            elif 'outline' in self.data['best_plot']:
                plot = self.data['best_plot']['outline']
        elif 'plot' in self.data:
            plot = self.data['plot']['outline']
        else:
            plot = 'N/A'
            
        return plot.replace('"','&quot;').replace("'","&#39;")

x = IMDbAPI('tt2379308')
print(x.title)
print(x.year)