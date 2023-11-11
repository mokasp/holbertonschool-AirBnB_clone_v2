#!/usr/bin/python3
""" module containing 7 simple web applications with flask """
from flask import Flask, render_template, g
from models import storage
from markupsafe import escape

app = Flask(__name__)
app.config['FLASK_DEBUG'] = False


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    from models.state import State
    storage.reload()
    x = storage.all(State)
    if id is None:
        states = []
        for item in x:
            states.append(x[item])
        return render_template("7-states_list.html", states=states)
    elif id is not None:
        for item in x:
            if x[item].id == id:
                state = x[item]
                return render_template("9-states.html", id=id, state=state)
        return render_template('9-states_not_found.html')


@app.teardown_appcontext
def teardown_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
