import json, os, sqlite3

db_filename = 'data.db'
files_db_filename = 'files.db'

db_is_new = not os.path.exists(db_filename)
files_db_is_new = not os.path.exists(files_db_filename)

conn = sqlite3.connect(db_filename)
files_conn = sqlite3.connect(files_db_filename)

if (os.path.exists(db_filename)):
  cur = conn.cursor()
  cur.execute("""SELECT * FROM galleries""")
  r = [dict((cur.description[i][0], value) \
    for i, value in enumerate(row)) for row in cur.fetchall()]
  with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(r, ensure_ascii=False))
  cur.execute("""SELECT * FROM tags""")
  r = [dict((cur.description[i][0], value) \
    for i, value in enumerate(row)) for row in cur.fetchall()]
  with open('tags.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(r, ensure_ascii=False))

if (os.path.exists(files_db_filename)):
  cur = files_conn.cursor()
  cur.execute("""SELECT * FROM files""")
  r = [dict((cur.description[i][0], value) \
    for i, value in enumerate(row)) for row in cur.fetchall()]
  with open('files.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(r, ensure_ascii=False))
