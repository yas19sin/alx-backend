#!/usr/bin/env python3
"""Flask app with Babel configuration and locale selector.

This module sets up a Flask application with Babel for
internationalization support and selects the best language match.
"""
from flask import Flask, render_template, request
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


@babel.localeselector
def get_locale() -> str:
    """Determine the best match for the client's preferred language.

    Returns:
        The best match language code from the supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Return the index page.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
