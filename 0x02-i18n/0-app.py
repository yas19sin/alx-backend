#!/usr/bin/env python3
"""Basic Flask app.

This module sets up a basic Flask application with a single route
that renders an HTML template.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Return the index page.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
