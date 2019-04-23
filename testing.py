
import sqlite3
import datetime


conn = sqlite3.connect(':memory:',detect_types=sqlite3.PARSE_DECLTYPES)
conn.execute('CREATE TABLE t (id integer primary key, dob timestamp)')
conn.execute('INSERT into t(dob) values (?)', (datetime.datetime.now(),))
x = conn.execute('SELECT * from t').fetchone()
print(x[1])
