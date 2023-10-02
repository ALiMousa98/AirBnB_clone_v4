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
    returns number of each objects by type
    """
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for key in classes:
        count = storage.count(classes[key])
        classes[key] = count
    return jsonify(classes)
