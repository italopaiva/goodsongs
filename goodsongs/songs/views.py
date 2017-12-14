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
