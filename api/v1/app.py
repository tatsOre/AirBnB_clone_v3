#!/usr/bin/python3
""" app.py
Module that starts a Flask API
"""
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    """Close the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'), threaded=True)
