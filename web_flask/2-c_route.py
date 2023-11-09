#!/usr/bin/python3
""" module containing three simple web applications with flask """
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<string:text>', strict_slashes=False)
def text(text):
    new_text = text.replace("_", " ")
    return f'C {escape(new_text)}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
