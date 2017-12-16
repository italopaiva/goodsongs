"""Songs endpoints."""

from flask import Blueprint, request

from goodsongs.api_responses import ok, unprocessable_entity
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

    return ok(paginated_songs)


@songs.route('/search', methods=['GET'])
def search_songs():
    """
    Search for songs with the given message.

    Accepts "message" as a query string to be the search parameter.

    The search is case insensitive and will search
    for song's and artist's names.
    """
    message = request.args.get('message') or ''
    found_songs = Song.find_by_title_or_artist(message)

    return ok(found_songs)


@songs.route('/avg/difficulty', methods=['GET'])
def get_songs_difficulty_average():
    """
    Return the average difficulty for all songs.

    Accepts an optional parameter "level" as query
    string to select only songs from a specific level.
    """
    level = request.args.get('level') or None

    average = Song.difficulty_average(level=level)

    return ok({'average': average})


@songs.route('/rating', methods=['POST'])
def add_rating():
    """
    Add a rating to the given song.

    Arguments:
        song_id -- ID of the song to be rated
        rating -- The rating value to add to the song.
                  Ratings should be between 1 and 5.
    """
    data = request.get_json()
    rating = data['rating']
    song_id = data['song_id']

    song = Song.get(song_id)

    if not (rating >= 1 and rating <= 5):
        return unprocessable_entity()

    return ok()
