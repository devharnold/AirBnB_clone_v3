#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Route that displays 'Hello HBNB!' """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Route that displays 'HBNB' """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ Route that displays 'C' fllowed by value of <text> """
    formatted_text = text.replace('_', ' ')
    return 'C {}'.format(formatted_text)


@app.route("/python", strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """ Route that displays 'Python' fllowed by value of <text> """
    formatted_text = text.replace('_', ' ')
    return 'Python {}'.format(formatted_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
