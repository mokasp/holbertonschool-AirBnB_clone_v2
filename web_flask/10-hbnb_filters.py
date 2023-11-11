#!/usr/bin/python3
""" module containing 7 simple web applications with flask """
from flask import Flask, render_template, g
from models import storage


app = Flask(__name__)
app.debug = False


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    from models.state import State
    from models.amenity import Amenity
    storage.reload()
    states = []
    amenities = []
    x = storage.all(State)
    y = storage.all(Amenity)
    for state in x:
        states.append(x[state])
    for amenity in y:
        amenities.append(y[amenity])
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(e=None):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
