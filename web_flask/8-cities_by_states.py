#!/usr/bin/python3
""" module containing 7 simple web applications with flask """
from flask import Flask, render_template, g
from models import storage
from markupsafe import escape

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    from models.state import State
    storage.reload()
    states = []
    x = storage.all(State)
    for item in x:
        states.append(x[item])
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
