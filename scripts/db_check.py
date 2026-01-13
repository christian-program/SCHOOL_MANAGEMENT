import sqlite3

conn=sqlite3.connect('db.sqlite3')
cur=conn.cursor()
cur.execute('PRAGMA foreign_keys=ON')
try:
    cur.execute("SELECT id, promotion FROM portal_post")
    rows=cur.fetchall()
    print('total rows in portal_post:', len(rows))
    bad=[]
    for r in rows:
        pid=r[0]
        prom=r[1]
        if prom is None:
            # NULL is acceptable for nullable FK
            continue
        if isinstance(prom, str):
            if prom.strip()=='' or not prom.strip().isdigit():
                bad.append((pid,prom))
        else:
            # non-str value (number) is fine
            pass
    print('bad rows count:', len(bad))
    for b in bad:
        print(b)
except Exception as e:
    print('ERROR', e)
finally:
    conn.close()
