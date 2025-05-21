#!/usr/bin/env python3
"""Flask app with Babel, user locale, and mock user login.

This module sets up a Flask application with Babel for
internationalization, user-specific locale preferences, and a mock user login
system.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel

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
    """Determine the best locale for the request based on priority.

    Priority:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request header
    4. Default locale

    Returns:
        The best match language code from the supported languages.
    """
    # 1. Locale from URL parameters
    url_locale = request.args.get('locale')
    if url_locale and url_locale in app.config['LANGUAGES']:
        return url_locale

    # 2. Locale from user settings
    if g.user and g.user.get('locale') and \
            g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # 3. Locale from request header
    header_locale = request.accept_languages.best_match(
        app.config['LANGUAGES'])
    if header_locale:
        return header_locale

    # 4. Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', strict_slashes=False)
def index() -> str:
    """Return the index page.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
