import os
import sqlite3

from flask import Flask, render_template, g, request

app = Flask(__name__)
app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'data'))
print(app.config['DATABASE'])

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    last_reading = db.execute(
        """
        SELECT read_datetime, temperature
        FROM temperatures
        ORDER BY read_datetime DESC;
        """
    ).fetchone()

    return render_template('index.html', last_reading=last_reading)
