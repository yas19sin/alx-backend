#!/usr/bin/env python3
"""Flask app with Babel, locale selector, and mock user login.

This module sets up a Flask application with Babel for
internationalization, locale selection, and a mock user login system.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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


def get_user() -> dict:
    """Get user dictionary by ID from login_as parameter.

    Returns:
        A user dictionary if the ID is valid and found, otherwise None.
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """Set the user in flask.g before each request.

    Retrieves the user based on the 'login_as' URL parameter and
    stores it in flask.g.user for access in other parts of the app.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Determine the locale for the request.

    Returns:
        The locale to use for the request, based on URL parameter,
        or the best match from the client's accepted languages.
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Return the index page.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
