#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenities_per_place(place_id=None):
    """
        reviews route to handle http method for requested reviews by place
    """
    place = storage.get(Place, place_id)

    if request.method == 'GET':
        if place is None:
            abort(404, 'Not found')

        if STORAGE_TYPE == 'db':
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            amenities = [storage.get(Amenity, amenity_id).to_dict()
                         for amenity_id in place.amenitiy_id]
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """
        reviews route to handle http methods for given review by ID
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404, 'Not found')
    if amenity is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (amenity not in place.amenities or
                amenity.id not in place.amenity_ids):
            abort(404, 'Not found')
        if STORAGE_TYPE == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id, None)
        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if STORAGE_TYPE == 'db':
            if (amenity in place.amenities):
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenities.append(amenity)
        else:
            if (amenity.id in place.amenity_ids):
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenity_ids.append(amenity_id)

        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
