#!/usr/bin/python3
"""
Flask application module 
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User

app = Flask(__name__)

# API endpoints for User objects

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Retrieve all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a specific User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)

@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a specific User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new User object"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    data = request.json
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a specific User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
