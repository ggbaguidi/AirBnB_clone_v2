#!/usr/bin/python3
"""
Write a script that starts a Flask web application:

    Your web application must be listening on 0.0.0.0, port 5000
    Routes:
        /: display “Hello HBNB!”
        /hbnb: display “HBNB”
        /c/<text>: display “C ”, followed by the value of the text variable
        (replace underscore _ symbols with a space )
        /python/<text>: display “Python ”, followed by the value of the text
        variable (replace underscore _ symbols with a space )
            The default value of text is “is cool”
    You must use the option strict_slashes=False in your route definition
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """display “Hello HBNB!”"""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """display “HBNB”"""
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c_route(text: str):
    """display “C ” followed by the value of the text variable"""
    return "C " + text.replace("_", " ")

@app.route("/python", strict_slashes=False, defaults={"text": "is cool"})
@app.route("/python/<text>", strict_slashes=False)
def python_route(text: str):
    """display “Python ”, followed by the value of the text"""
    return "Python " + text.replace("_", " ")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
