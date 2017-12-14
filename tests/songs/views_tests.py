from flask import url_for

from ..helpers import matches_json


songs_schema = {}


def test_get_songs(client):
    url = url_for('songs.get_songs')
    response = client.get(url)
    assert response.status_code == 200
    assert matches_json(response.json, songs_schema)
