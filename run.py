import requests
import os
import sqlite3
import json
from datetime import datetime
from pytz import timezone

db_filename = 'data.db'
schema_filename = 'data_schema.sql'
files_db_filename = 'files.db'
files_schema_filename = 'files_schema.sql'

db_is_new = not os.path.exists(db_filename)
files_db_is_new = not os.path.exists(files_db_filename)

conn = sqlite3.connect(db_filename)
files_conn = sqlite3.connect(files_db_filename)

logs = ""

if db_is_new:
  with open(schema_filename, 'rt') as f:
    schema = f.read()
  conn.executescript(schema)
if files_db_is_new:
  with open(files_schema_filename, 'rt') as f:
    schema = f.read()
  files_conn.executescript(schema)

def write_date():
  with open('latest.date', 'w', encoding='utf-8') as file:
    date = datetime.now(timezone('Asia/Seoul'))
    file.write(str(date))
def numbers():
  url = "https://ltn.hitomi.la/index-korean.nozomi"
  res = requests.get(url)
  data = res.content
  return [int.from_bytes(data[i:i+4], 'big') for i in range(0, len(data), 4)]
def fetch(id):
  url = "https://ltn.hitomi.la/galleries/{0}.js".format(id)
  res = requests.get(url)
  data = res.content[18:].decode('utf-8')
  return json.loads(data)
def tags():
  url = "https://github.com/rmagur1203/hitomi-series/blob/master/tags.json?raw=true"
  res = requests.get(url)
  data = res.content.decode('utf-8')
  return list(map(lambda x: x[1],json.loads(data)))
def create_tag(tagfull, tagtype, tagname):
  cur = conn.cursor()
  cur.execute("""
  INSERT INTO tags (full, type, name)
  VALUES (?, ?, ?)
  """, (tagfull,
        tagtype,
        tagname)
  )
  return cur.lastrowid
def tag2oid(tag):
  if 'male' in tag and (tag['male'] == 1 or tag['male'] == '1'):
    tagtype = 'male:'
  elif 'female' in tag and (tag['female'] == 1 or tag['female'] == '1'):
    tagtype = 'female:'
  else:
    tagtype = ''
  full = tagtype + tag['tag']
  cur = conn.cursor()
  cur.execute("""
  SELECT oid FROM tags WHERE full=?
  """, (full,))
  rows = cur.fetchall()
  if len(rows) <= 0:
    tagtype = None
    if 'male' in tag and (tag['male'] == 1 or tag['male'] == '1'):
      tagtype = 'male'
    elif 'female' in tag and (tag['female'] == 1 or tag['female'] == '1'):
      tagtype = 'female'
    return create_tag(full, tagtype, tag['tag'])
  return rows[0][0]
def file2oid(file):
  cur = files_conn.cursor()
  cur.execute("""
  SELECT oid FROM files WHERE hash=?
  """, (file["hash"],))
  res = cur.fetchall()
  if len(res) > 0:
    return res[0][0]
  else:
    cur.execute("""
    INSERT INTO files (hash, hasavif, haswebp, width, height, name)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (file["hash"],
          file["hasavif"],
          file["haswebp"],
          file["width"],
          file["height"],
          file["name"])
    )
    return cur.lastrowid

nums = numbers()
for i in range(len(nums)):
  num = nums[i]

  cur = conn.cursor()
  cur.execute("""
  SELECT COUNT(1) FROM galleries WHERE id=?
  """, (num,))
  res = cur.fetchall()
  if res[0][0] > 0:
    continue

  data = fetch(num)
  tags = list(map(str, map(tag2oid, data['tags'])))
  files = list(map(str, map(file2oid, data['files'])))
  conn.execute("""
  INSERT INTO galleries (id, type, title, language, language_localname, japanese_title, date, tag_ids, file_ids)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  """, (data["id"],
        data["type"],
        data["title"],
        data["language"],
        data["language_localname"],
        data["japanese_title"],
        data["date"],
        ','.join(tags),
        ','.join(files))
  )
  if i % 100 == 0:
    conn.commit()
    files_conn.commit()
  write_date()
  logs += data["id"] + "\n"
  print(data["id"])
conn.commit()
files_conn.commit()
if logs != "":
  with open('latest.log', 'w', encoding='utf-8') as file:
    file.write(logs)
