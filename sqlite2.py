import sqlite3

conn=sqlite3.connect('practice_counts.sqlite')
cur=conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''
CREATE TABLE Counts(
      org TEXT,
    count INTEGER
)
''')
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'
xfile = open(fname)

for item in xfile:
    if not item.startswith("From "):
        continue
    words = item.rstrip().split()[1]
    word = words.split('@')[1]

    cur.execute('SELECT count FROM Counts WHERE org=?', (word,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts(org, count) VALUES (?, 1)', (word,))
    else:
        cur.execute('UPDATE Counts SET count = count+1 WHERE org = ?', (word,))
    conn.commit()

sqlstr = "SELECT * FROM Counts ORDER BY count DESC"

for row in cur.execute(sqlstr):
    print("org:", row[0],"count:", row[1])
