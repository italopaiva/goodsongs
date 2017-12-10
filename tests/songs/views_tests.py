from flask import url_for


def test_get_songs(client):
    url = url_for('songs.get_songs')
    res = client.get(url)
    assert res.status_code == 200
