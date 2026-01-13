import sqlite3

conn=sqlite3.connect('db.sqlite3')
cur=conn.cursor()
cur.execute('PRAGMA foreign_keys=ON')
try:
    # Count and clear empty or non-numeric promotion values in portal_post
    cur.execute("SELECT COUNT(*) FROM portal_post WHERE promotion IS NOT NULL AND (trim(promotion) = '' OR promotion NOT GLOB '[0-9]*')")
    p_before = cur.fetchone()[0]
    cur.execute("UPDATE portal_post SET promotion = NULL WHERE promotion IS NOT NULL AND (trim(promotion) = '' OR promotion NOT GLOB '[0-9]*')")

    # Count and clear in portal_studentresult
    cur.execute("SELECT COUNT(*) FROM portal_studentresult WHERE promotion IS NOT NULL AND (trim(promotion) = '' OR promotion NOT GLOB '[0-9]*')")
    s_before = cur.fetchone()[0]
    cur.execute("UPDATE portal_studentresult SET promotion = NULL WHERE promotion IS NOT NULL AND (trim(promotion) = '' OR promotion NOT GLOB '[0-9]*')")

    conn.commit()
    print(f"portal_post cleaned: {p_before}, portal_studentresult cleaned: {s_before}")
except Exception as e:
    print('ERROR', e)
finally:
    conn.close()
