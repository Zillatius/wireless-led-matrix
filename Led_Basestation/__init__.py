import sys, time, struct, threading, click, os, sqlite3
from . import hwInterface as hw
from flask import Flask, jsonify, render_template, current_app, g
from flask.cli import with_appcontext


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'measurements.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #runs before processing first request
    @app.before_first_request
    def getNewReading():
        temp, hum = hw.setCell(286)
        if temp > -1:
            with app.app_context():
                db = get_db()
                db.execute(
                    'INSERT INTO measurements (temperature, humidity) VALUES (?,?)',
                    (temp,hum)
                )
                db.commit()
            threading.Timer(300, getNewReading).start()
        else:
            threading.Timer(1, getNewReading).start()

        print("got t:{} h:{}".format(temp,hum))
        

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/setCell/<int:num>')
    def setCell(num):
        x = num if num >= 0 else (255 if num > 255 else 0)
        temp, hum = hw.setCell(x)
        msg = {'temp':temp,
                'hum':hum}
        return jsonify(msg)
    @app.route('/getData/<string:dateStart>&<string:dateEnd>')
    def getTempData(dateStart, dateEnd):
        #db interface
        date=[]
        temp=[]
        hum=[]
        db = get_db()
        db.row_factory = dict_factory
        data = db.execute(
            'SELECT * FROM measurements WHERE measurement_date BETWEEN ? AND ?',
            (dateStart,dateEnd)
        ).fetchall()
        for r in data:
            date.append(r['measurement_date']*1000)
            temp.append(r['temperature'])
            hum.append(r['humidity'])
        
        return jsonify({'date':date,'temp':temp,'hum':hum})


    init_app(app)

    return app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('baza zrifreszowana')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


