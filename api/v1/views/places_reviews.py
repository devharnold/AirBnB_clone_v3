#!/usr/bin/python3

"""Start a Flask app"""
from flask import Blueprint, make_response, abort, request, jsonify
from models import Review, User
from api.v1.views import app_views

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_places(place_id):
    """Retrieves the list of all Review objects
    If the place_id is not linked to any Place object, raise a 404
    """
    place  = Review.query.get(place_id)
    if place is None:
        abort(404)

    reviews = Review.query.filter(place_id=place_id).all()
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list)

@app_views.route('/reviews/<reviews_id>', methods=['GET'])
def get_reviewobj(review_id):
    """
    Retrieves a review object
    If the review_id is not linked to any Review object, raise a 404 error
    """
    review = Review.query.get(review_id)
    if review_id is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    is not linked to any Review object, raise a 404 
    Returns an empty dictionary with the status code 200
    """
    review = Review.query.get(review_id)
    if review_id is None:
        abort(404)
    review.delete()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    If the place_id is not linked to any Place object, raise a 404 error
    If the HTTP body request is not valid JSON, raise a 400 e
    If the dictionary does not contain the key user_id, raise a 400 
    """
    place = next((p for p in place if p['id'] == place_id), None)
    if place is None:
        abort(404)
    
    if not request.is_json:
        abort(404, description='Not a JSON')

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    user = User.query.get(data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data:
        abort(400, description='Missing text')

    new_review = Review(
        user_id = data['user_id'],
        place_id = place_id,
        text=data['text']
    )
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 
    Update the Review object with all key-value pairs of the dictionary
    """
    review = Review.query.get(review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()

    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key in ignored_keys:
        data.pop(key, None)

    for key, value in data.items():
        setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200