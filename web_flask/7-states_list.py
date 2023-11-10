#!/usr/bin/python3
""" module containing 7 simple web applications with flask """
from flask import Flask, render_template, g
from models import storage
from markupsafe import escape

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    from models.state import State
    storage.reload()
    states = []
    x = storage.all(State)
    for item in x:
        states.append(x[item])
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
