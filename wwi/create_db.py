import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('words.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS verses (
    id INTEGER PRIMARY KEY,
    book TEXT,
    chapter INTEGER,
    verse INTEGER,
    strongs INTEGER,
    transliteration TEXT,
    root TEXT,
    hebrew TEXT,
    english TEXT,
    morphology TEXT
)
''')

# Insert data into the table
cursor.execute('''
INSERT INTO data (book, chapter, verse, strongs, hebrew, english, morphology)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', ('1_samuel', 1, 1, 'H1234', 'בְּרֵאשִׁית', 'In the beginning', 'Noun'))

# Commit the changes and close the connection
conn.commit()
conn.close()