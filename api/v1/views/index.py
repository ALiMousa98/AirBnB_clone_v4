#!/usr/bin/python3
"""JSON file status """

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status", methods=["GET"])
def status():
    '''
    Returns a JSON response for RESTful API health.
    '''
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Returns the number of instances of each object
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
    