import time, requests, pymysql.cursors

def search(conn, table, imdbID):
    c = conn.cursor()
    c.execute("SELECT * FROM " + table)
    for row in c:
        if row[0] == imdbID:
            return False
    return True

def delete(imdbID, table='temp'):
    conn = pymysql.connect(host='localhost', port=8889, user='imdb', password='movie', db='imdb')
    c = conn.cursor()
    c.execute("DELETE FROM " + table + " WHERE imdbID='" + imdbID + "'")
    conn.commit()
    conn.close()

def main(conn=pymysql.connect(host='localhost', port=8889, user='imdb', password='movie', db='imdb')):
    c = conn.cursor()
    c.execute("SELECT * FROM temp")
    for row in c:
        if not search(conn, 'imdb', row[0]):
            delete(row[0])
        else:
            r = requests.get('http://localhost:81/imdb/api.php', params={"i":row[0]})
            print(r.url)
            delete(row[0])
            print('----------')
        time.sleep(1.5)
    conn.close()

main()