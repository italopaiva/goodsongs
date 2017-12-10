"""Songs endpoints."""

from flask import Blueprint, jsonify


songs = Blueprint('songs', __name__)


@songs.route('', methods=['GET'])
def get_songs():
    """
    Return a list of songs with some details on them.

    Accepts a page parameter as a query string to paginate the results.
    """
    return jsonify([{'id': 1, 'name': 'song name'}])
