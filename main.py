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

    all_readings = db.execute(
        """
        SELECT strftime ('%d %H',read_datetime) as read_datetime, round(avg(temperature),1) as temperature
        FROM temperatures where read_datetime >= datetime('now', '-1 day')
        GROUP BY strftime ('%d %H',read_datetime);
        """
    ).fetchall()

    minimum = db.execute(
        """
        SELECT read_datetime, round(min(temperature), 1) as temperature
        FROM temperatures where read_datetime >= datetime('now', '-1 day');
        """
    ).fetchone()

    maximum = db.execute(
        """
        SELECT read_datetime, round(max(temperature), 1) as temperature
        FROM temperatures where read_datetime >= datetime('now', '-1 day');
        """
    ).fetchone()

    average = db.execute(
        """
        SELECT read_datetime, round(avg(temperature), 1) as temperature
        FROM temperatures where read_datetime >= datetime('now', '-1 day');
        """
    ).fetchone()

    print(minimum['temperature'])
    print(maximum['temperature'])
    print(average['temperature'])

    labels = []
    values = []

    for reading in all_readings:
        labels.append(reading['read_datetime'][-2:])
        values.append(reading['temperature'])


    # labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    # values = [19, 19, 3, 5, 2, 3]

    return render_template(
        'index.html',
        minimum=minimum,
        maximum=maximum,
        average=average,
        labels=labels,
        values=values)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
