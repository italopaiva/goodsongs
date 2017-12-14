# pylint: skip-file
from flask import url_for

import pytest

from .schemas import all_songs_schema

from ..factories.song_factory import SongFactory

from ..helpers import TestViewBaseClass
from ..helpers import matches_json


@pytest.fixture(scope='module')
def some_songs(request):
    """Create some songs and return them.

    The quantity of songs to be created is passed as an argument.
    """
    return [SongFactory.create() for _ in range(0, request.param)]


@pytest.mark.usefixtures('client_class')
class TestGetSongsView(TestViewBaseClass):
    """Test songs views."""

    url = 'songs.get_songs'
    schema = all_songs_schema

    @pytest.mark.options(default_per_page=10)
    @pytest.mark.parametrize('some_songs', [5], indirect=True)
    def test_get_all_songs(self, some_songs):
        amount_of_songs = len(some_songs)

        response = self.client.get(url_for(self.url))

        self.assert_response_ok(response)
        assert len(response.json['data']) == amount_of_songs

    @pytest.mark.options(default_per_page=2)
    @pytest.mark.parametrize('some_songs', [10], indirect=True)
    def test_get_paginated_songs_with_default_per_page(self, some_songs):
        amount_of_songs = len(some_songs)
        total_pages = amount_of_songs / 2
        current_page = 1

        response = self.client.get(url_for(self.url))

        assert len(response.json['data']) == 2
        self.assert_response_ok(response)
        self.assert_pagination_meta_ok(response, current_page, total_pages)

    @pytest.mark.parametrize('some_songs', [10], indirect=True)
    def test_get_paginated_songs_with_custom_per_page(self, some_songs):
        amount_of_songs = len(some_songs)
        current_page = 1
        per_page = 3
        total_pages = (amount_of_songs // per_page) + 1

        url = url_for(self.url) + '?per_page=%s' % per_page
        response = self.client.get(url)

        self.assert_response_ok(response)
        self.assert_pagination_meta_ok(response, current_page, total_pages)
        assert len(response.json['data']) == per_page

    def assert_response_ok(self, response):
        assert response.status_code == 200
        assert matches_json(response.json, self.schema)

    def assert_pagination_meta_ok(self, response, current_page, total_pages):
        assert response.json['meta']['current_page'] == current_page
        assert response.json['meta']['next_page'] == current_page + 1
        assert response.json['meta']['total_pages'] == total_pages
