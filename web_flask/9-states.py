#!/usr/bin/python3
""" module containing 7 simple web applications with flask """
from flask import Flask, render_template, g
from models import storage
from markupsafe import escape

app = Flask(__name__)

@app.route('/states', strict_slashes=False)
def states():
    from models.state import State
    storage.reload()
    states = []
    x = storage.all(State)
    for item in x:
        states.append(x[item])
    return render_template("7-states_list.html", states=states)


@app.route('/states/<id>', strict_slashes=False)
def state(id):
    from models.state import State
    storage.reload()
    x = storage.all(State)
    for item in x:
        if x[item].id == id:
            state = x[item]
            return render_template("9-states.html", id=id, state=state)
    return 'Not found!'


@app.teardown_appcontext
def teardown_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
