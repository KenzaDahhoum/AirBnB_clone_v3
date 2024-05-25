#!/usr/bin/python3
"""
Flask application module 
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User

app = Flask(__name__)

# API endpoints for Place objects

@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Retrieve all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])

@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
