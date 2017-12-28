import json, time, webbrowser, requests, pymysql.cursors

headers = {'user-agent': 'ryTest/0.0.1'}

def search(c, table, imdbID):
    c.execute("SELECT * FROM " + table + " WHERE imdbID='" + imdbID + "'")
    for row in c:
        if row[0] == imdbID:
            return False
    return True

def add_row(conn, imdbID):
    c = conn.cursor()
    if search(c, 'temp', imdbID) and search(c, 'imdb', imdbID):
        c.execute("INSERT INTO temp VALUES ('" + imdbID + "')")
        conn.commit()

def reddit_imdb(conn, i=0, after='', page=1, old=0):
    req = requests.get('https://www.reddit.com/domain/imdb.com/new/.json', params={"count":str(i), "after":str(after)}, headers=headers)
    data = json.loads(req.text)
    
    c = conn.cursor()
    
    x = data['data']['children']
    for i in range(len(x)):
        if old >= 25:
            break
        url = x[i]['data']['url']
        if '/title/' in url:
            imdbID = url.split('/title/', 1)[1]
            imdbID = imdbID.split('/', 1)[0]
            if imdbID != 'title':
                if search(c, 'imdb', imdbID) and search(c, 'temp', imdbID) and search(c, 'episodes', imdbID):
                    print(imdbID)
                    add_row(conn, imdbID)
                else:
                    old += 1
        #time.sleep(1/60)
    print('----------')
    
    if old >= 25:
        return 0
    if page <= 15:
        time.sleep(201/100)
        reddit_imdb(conn, i+25, data['data']['after'], page+1, old)

def main():
    conn = pymysql.connect(host='localhost', port=8889, user='imdb', password='movie', db='imdb')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS temp (imdbID MEDIUMTEXT)")
    
    print('Starting...')
    reddit_imdb(conn)
    print('Done')
    
    conn.close()

if __name__ == '__main__':
    main()