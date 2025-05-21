#!/usr/bin/env python3
"""Basic Flask app with Babel configuration.

This module sets up a Flask application with Babel for
internationalization support.
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Configuration class for the Flask app.

    Attributes:
        LANGUAGES (list): List of available languages
        BABEL_DEFAULT_LOCALE (str): Default locale
        BABEL_DEFAULT_TIMEZONE (str): Default timezone
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Return the index page.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
