#!/usr/bin/python3
""" module containing six simple web applications with flask """
from flask import Flask, render_template
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
def python(text='is cool'):
    new_text = text.replace("_", " ")
    return f'Python {escape(new_text)}'


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return f'{escape(n)} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_templates(n):
    return render_template("5-number.html", n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
