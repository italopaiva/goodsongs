"""Songs endpoints."""

from flask import Blueprint, jsonify


songs = Blueprint('songs', __name__)


@songs.route('', methods=['GET'])
def get_songs():
    """
    Return a list of songs with some details on them.

    Accepts page and per_page parameters
    as a query strings to paginate the results.
    """
    return jsonify({
        'data': [
            {
                '_id': {
                    '$oid': '5a31d485bdb63d001da756d7'
                },
                'artist': 'The Yousicians',
                'difficulty': 14.6,
                'level': 13,
                'released': {
                    '$date': 1477440000000
                },
                'title': 'Lycanthropic Metamorphosis'
            }
        ],
        'meta': {
            'current_page': 1,
            'next_page': 2,
            'total_pages': 3
        }
    })
