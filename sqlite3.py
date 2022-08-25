import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('sql_project.sqlite')
cur = conn.cursor()
cur.executescript ('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE);
CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE);
CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE);
CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER);
''')

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

fname = input("Input file name")
if len(fname) < 1:
    fname = 'Library.xml'

tree = ET.parse(fname)
find = tree.findall('dict/dict/dict')
print ('count of dict', len(find))

for item in find:
    if (lookup(item,'Track ID')is None):
        continue
    name = lookup(item, 'Name')
    artist = lookup(item, 'Artist')
    album = lookup(item, 'Album')
    count = lookup(item, 'Play Count')
    rating = lookup(item, 'Rating')
    length = lookup(item, 'Total Time')
    genre = lookup(item, 'Genre')


    if name is None or artist is None or album is None or genre is None: continue

    cur.execute('INSERT OR IGNORE INTO Artist(name) VALUES(?)', (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist, ))
    artist_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Album(title, artist_id) VALUES(?,?)', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Genre(name) VALUES(?)', (genre,))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cur.fetchone()[0]
    cur.execute('INSERT OR REPLACE INTO TRACK(title, album_id, genre_id, rating, len, count) VALUES (?,?,?,?,?,?)', (album, album_id, genre_id, rating, length, count))
    conn.commit()

sqlstr = "SELECT Track.title, Artist.name, Album.title, Genre.name FROM Track JOIN Artist JOIN Album JOIN Genre ON Artist.id = Album.artist_id AND Track.album_id = Album.id AND Track.Genre_id = Genre.id ORDER BY Artist.name LIMIT 3 "

for row in cur.execute(sqlstr):
    print(row)
