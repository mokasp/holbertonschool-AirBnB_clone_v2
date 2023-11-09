#!/usr/bin/python3
""" module containing four simple web applications with flask """
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
def c(text):
    new_text = text.replace("_", " ")
    return f'C {escape(new_text)}'


@app.route('/python', strict_slashes=False)
@app.route('/python/<string:text>', strict_slashes=False)
def python(text='is fun'):
    new_text = text.replace("_", " ")
    return f'Python {escape(new_text)}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
