import sqlite3

write = input("enter text:")
if len(write) < 1:
    write = 'mbox.txt'

handle = open(write)

conn = sqlite3.connect('mboxdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''
CREATE TABLE Counts(
    org TEXT,
    count INTEGER)
''')

for lines in handle:
    if not lines.startswith("From "):
        continue
    line = lines.rstrip().split()[1]
    word = line.split('@')[1]

    cur.execute('SELECT count FROM Counts WHERE org = ?', (word,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts(org, count) VALUES (?, 1)', (word,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (word,))
    conn.commit()

sqlstr = "SELECT * FROM Counts ORDER BY count DESC LIMIT 10"

for item in cur.execute(sqlstr):
    print(item)
