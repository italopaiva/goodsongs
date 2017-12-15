"""Songs endpoints."""

from flask import Blueprint, jsonify, request

from goodsongs.models import Song
from goodsongs.pagination import get_pagination_params, paginate


songs = Blueprint('songs', __name__)


@songs.route('', methods=['GET'])
def get_songs():
    """
    Return a list of songs with some details on them.

    Accepts page and per_page parameters
    as a query strings to paginate the results.
    """
    page, per_page = get_pagination_params(request)
    all_songs = Song.objects
    paginated_songs = paginate(all_songs, page=page, per_page=per_page)

    return jsonify(paginated_songs)


@songs.route('/search', methods=['GET'])
def search_songs():
    """
    Search for songs with the given message.

    Accepts "message" as a query string to be the search parameter.

    The search is case insensitive and will search
    for song's and artist's names.
    """
    return jsonify({'data': [
        {
            "_id": {
                "$oid": "5a3327d2008b90001ce60239"
            },
            "artist": "The Yousicians",
            "difficulty": 14.6,
            "level": 13,
            "released": {
                "$date": 1477440000000
            },
            "title": "Special Name 1"
        },
        {
            "_id": {
                "$oid": "5a3327d2008b90001ce60239"
            },
            "artist": "The Yousicians",
            "difficulty": 14.6,
            "level": 13,
            "released": {
                "$date": 1477440000000
            },
            "title": "Special Name 2"
        },
    ]})
