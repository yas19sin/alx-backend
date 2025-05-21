#!/usr/bin/env python3
"""Flask app with Babel, user locale, timezone, and current time display.

This module sets up a Flask application with Babel for
internationalization, user-specific locale and timezone preferences,
and displays the current time formatted according to the user's locale.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

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
        try:
            return users.get(int(user_id))
        except ValueError:
            return None
    return None


@app.before_request
def before_request() -> None:
    """Set the user in flask.g before each request.

    Retrieves the user based on the 'login_as' URL parameter and
    stores it in flask.g.user for access in other parts of the app.
    """
    user = get_user()
    g.user = user
    current_tz = pytz.timezone(get_timezone())
    g.current_time = format_datetime(datetime.now(current_tz))


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


@babel.timezoneselector
def get_timezone() -> str:
    """Determine the best timezone for the request based on priority.

    Priority:
    1. Timezone from URL parameters
    2. Timezone from user settings
    3. Default to UTC

    Returns:
        A valid timezone string.
    """
    # 1. Find timezone parameter in URL parameters
    tz_param = request.args.get('timezone')
    if tz_param:
        try:
            pytz.timezone(tz_param)
            return tz_param
        except UnknownTimeZoneError:
            pass

    # 2. Find time zone from user settings
    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass

    # 3. Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def index() -> str:
    """Return the index page.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
