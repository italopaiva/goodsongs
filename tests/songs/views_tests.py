# pylint: skip-file
from random import choice, randint

import pytest

from .schemas import all_songs_schema
from .schemas import song_ratings_data_schema
from .schemas import songs_difficulty_schema

from ..factories.rating_factory import RatingFactory
from ..factories.song_factory import SongFactory

from ..helpers import TestViewBaseClass


@pytest.fixture(scope='module')
def some_songs(request):
    """Create some songs and return them.

    The quantity of songs to be created is passed as an argument.
    """
    return [SongFactory.create() for _ in range(0, request.param)]


class TestGetSongsView(TestViewBaseClass):
    """Test get_songs view."""

    url = 'songs.get_songs'
    schema = all_songs_schema

    @pytest.mark.options(default_per_page=10)
    @pytest.mark.parametrize('some_songs', [5], indirect=True)
    def test_get_all_songs(self, some_songs):
        amount_of_songs = len(some_songs)

        self.get()

        self.assert_response_ok()
        self.assert_quantity_of_items(amount_of_songs)

    @pytest.mark.options(default_per_page=2)
    @pytest.mark.parametrize('some_songs', [10], indirect=True)
    def test_get_paginated_songs_with_default_per_page(self, some_songs):
        amount_of_songs = len(some_songs)
        total_pages = amount_of_songs / 2
        current_page = 1

        self.get()

        self.assert_response_ok()
        self.assert_quantity_of_items(2)
        self.assert_pagination_meta_ok(current_page, total_pages)

    @pytest.mark.parametrize('some_songs', [10], indirect=True)
    def test_get_paginated_songs_with_custom_per_page(self, some_songs):
        amount_of_songs = len(some_songs)
        current_page = 1
        per_page = 3
        total_pages = (amount_of_songs // per_page) + 1

        self.get(params={'per_page': per_page})

        self.assert_response_ok()
        self.assert_pagination_meta_ok(current_page, total_pages)
        self.assert_quantity_of_items(per_page)

    def test_get_no_songs(self):
        self.get()

        self.assert_response_ok()
        self.assert_pagination_meta_ok(1, 0)
        self.assert_quantity_of_items(0)


class TestSearchSongsView(TestViewBaseClass):
    """Test search_songs view."""

    url = 'songs.search_songs'
    schema = all_songs_schema

    @pytest.fixture
    def names(self):
        return ['Name 1', 'Name 2', 'Name 3']

    @pytest.fixture
    def special_names(self):
        return ['Special Name 1', 'Special Name 2']

    @pytest.fixture
    def songs_with_regular_title(self, names):
        return [SongFactory.create(title=title) for title in names]

    @pytest.fixture
    def songs_with_special_title(self, special_names):
        return [SongFactory.create(title=title) for title in special_names]

    @pytest.fixture
    def songs_with_regular_artist(self, names):
        return [SongFactory.create(artist=name) for name in names]

    @pytest.fixture
    def songs_with_special_artist(self, special_names):
        return [SongFactory.create(artist=name) for name in special_names]

    @pytest.mark.usefixtures(
        'songs_with_regular_title',
        'songs_with_special_title',
    )
    def test_search_for_songs_title(self, special_names):
        attr = 'title'
        message = 'Special'

        self.get(params={'message': message})

        self.assert_response_ok()
        self.assert_quantity_of_items(len(special_names))
        self.assert_data_attr_contains(attr, message)

    @pytest.mark.usefixtures(
        'songs_with_regular_title',
        'songs_with_special_title',
    )
    def test_search_for_songs_title_case_insensitive(self, special_names):
        attr = 'title'
        message = 'special'

        self.get(params={'message': message})

        self.assert_response_ok()
        self.assert_quantity_of_items(len(special_names))
        self.assert_data_attr_contains(attr, message, case_insensitive=True)

    @pytest.mark.usefixtures(
        'songs_with_regular_artist',
        'songs_with_special_artist',
    )
    def test_search_for_songs_artist(self, special_names):
        attr = 'artist'
        message = 'Special'

        self.get(params={'message': message})

        self.assert_response_ok()
        self.assert_quantity_of_items(len(special_names))
        self.assert_data_attr_contains(attr, message)

    @pytest.mark.usefixtures(
        'songs_with_regular_artist',
        'songs_with_special_artist',
    )
    def test_search_for_songs_artist_case_insensitive(self, special_names):
        attr = 'artist'
        message = 'special'

        self.get(params={'message': message})

        self.assert_response_ok()
        self.assert_quantity_of_items(len(special_names))
        self.assert_data_attr_contains(attr, message, case_insensitive=True)

    @pytest.mark.usefixtures(
        'songs_with_regular_title',
        'songs_with_special_title',
    )
    def test_search_for_songs_without_message(self, names, special_names):
        self.get(params={})

        self.assert_response_ok()
        self.assert_quantity_of_items(len(special_names) + len(names))

    @pytest.mark.usefixtures(
        'songs_with_regular_title',
        'songs_with_special_artist',
    )
    @pytest.mark.parametrize('some_songs', [5], indirect=True)
    def test_search_for_songs_with_title_and_artist(
        self, names, special_names, some_songs
    ):
        message = 'Name'

        self.get(params={'message': message})

        self.assert_response_ok()
        self.assert_quantity_of_items(len(special_names) + len(names))


class TestGetSongsDifficultyAverageView(TestViewBaseClass):
    """Test get_songs_difficulty_average view."""

    url = 'songs.get_songs_difficulty_average'
    schema = songs_difficulty_schema

    @pytest.fixture
    def difficulties(self):
        return [10, 5.5, 6.7, 6.5, 8.8, 3]

    @pytest.fixture
    def level_two_difficulties(self):
        return [1, 2, 3, 4]

    @pytest.fixture
    def level_ten_difficulties(self):
        return [15, 20, 25, 30]

    @pytest.fixture
    def songs_with_difficulties(self, difficulties):
        return [
            SongFactory.create(difficulty=difficulty)
            for difficulty in difficulties
        ]

    @pytest.fixture
    def level_ten_songs(self, level_ten_difficulties):
        return [
            SongFactory.create(difficulty=difficulty, level=10)
            for difficulty in level_ten_difficulties
        ]

    @pytest.fixture
    def level_two_songs(self, level_two_difficulties):
        return [
            SongFactory.create(difficulty=difficulty, level=2)
            for difficulty in level_two_difficulties
        ]

    @pytest.mark.usefixtures('songs_with_difficulties')
    def test_get_songs_difficulty_avg(self, difficulties):
        expected_average = sum(difficulties) / float(len(difficulties))

        self.get()

        average = self.response_data()['average']

        self.assert_response_ok()
        assert average == expected_average

    @pytest.mark.usefixtures('level_ten_songs', 'level_two_songs')
    def test_get_songs_difficulty_avg_for_specific_level(
        self, level_ten_difficulties
    ):
        difficulties_sum = sum(level_ten_difficulties)
        difficulties_count = len(level_ten_difficulties)
        expected_average = difficulties_sum / float(difficulties_count)
        level = 10

        self.get(params={'level': level})

        average = self.response_data()['average']

        self.assert_response_ok()
        assert average == expected_average

    def test_get_songs_difficulty_avg_for_no_songs(self):
        expected_average = 0

        self.get()

        average = self.response_data()['average']

        self.assert_response_ok()
        assert average == expected_average


class TestAddRatingView(TestViewBaseClass):
    """Test add_rating view."""

    url = 'songs.add_rating'
    schema = None

    MIN_VALID_RATING = 1
    MAX_VALID_RATING = 5

    @pytest.fixture
    def song(self):
        return SongFactory.create()

    def test_add_min_valid_rating_to_song(self, song):
        rating = self.MIN_VALID_RATING
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_created()

    def test_add_max_valid_rating_to_song(self, song):
        rating = self.MAX_VALID_RATING
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_created()

    def test_add_random_valid_rating_to_song(self, song):
        rating = randint(self.MIN_VALID_RATING, self.MAX_VALID_RATING)
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_created()

    def test_add_nearest_min_invalid_rating_to_song(self, song):
        rating = self.MIN_VALID_RATING - 1
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_unprocessable_entity()

    def test_add_nearest_max_invalid_rating_to_song(self, song):
        rating = self.MAX_VALID_RATING + 1
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_unprocessable_entity()

    def test_add_random_invalid_negative_rating_to_song(self, song):
        rating = randint(-100, self.MIN_VALID_RATING - 1)
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_unprocessable_entity()

    def test_add_random_invalid_positive_rating_to_song(self, song):
        rating = randint(self.MAX_VALID_RATING + 1, 100)
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_unprocessable_entity()

    def test_add_rating_to_nonexistent_song(self):
        rating = 1
        nonexistent_song_id = 10
        data = {
            'song_id': nonexistent_song_id,
            'rating': rating,
        }

        self.post(data=data)

        self.assert_response_not_found()

    def test_add_new_rating_to_song(self, song):
        rating = 3
        data = {
            'song_id': str(song.pk),
            'rating': rating,
        }

        self.post(data=data)

        song.reload()

        self.assert_response_created()
        assert song.ratings[0]['value'] == rating


class TestGetSongRatingsDataView(TestViewBaseClass):
    """Test get_song_ratings_data view."""

    url = 'songs.get_song_ratings_data'
    schema = song_ratings_data_schema

    @pytest.fixture
    def random_integer(self):
        return randint(1, 100)

    @pytest.fixture
    def ratings_values(self, random_integer):
        return [choice(list(range(1, 6))) for _ in range(random_integer)]

    @pytest.fixture
    def ratings(self, ratings_values):
        return [RatingFactory.create(value=value) for value in ratings_values]

    @pytest.fixture
    def rated_song(self, ratings):
        return SongFactory.create(ratings=ratings)

    @pytest.fixture
    def unrated_song(self):
        return SongFactory.create(ratings=[])

    def test_get_rated_song_ratings_data(self, rated_song, ratings_values):
        self.url_params = {'song_id': str(rated_song.pk)}

        self.get()

        data = self.response_data()
        expected_average = sum(ratings_values) / float(len(ratings_values))

        self.assert_response_ok()
        assert data['average'] == expected_average
        assert data['lowest'] == min(ratings_values)
        assert data['highest'] == max(ratings_values)

    def test_get_unrated_song_ratings_data(self, unrated_song):
        self.url_params = {'song_id': str(unrated_song.pk)}

        self.get()

        data = self.response_data()

        self.assert_response_ok()
        assert data['average'] is None
        assert data['lowest'] is None
        assert data['highest'] is None

    def test_get_rating_data_of_nonexistent_song(self):
        nonexistent_song_id = 10
        self.url_params = {'song_id': nonexistent_song_id}

        self.get()

        self.assert_response_not_found()
