"""Test helpers module."""

from flask import url_for

from jsonschema import validate

from mongoengine.connection import _get_db

import pytest


def matches_json(data, schema):
    """Check if the given JSON response matches the given schema."""
    try:
        validate(data, schema)
    except Exception:
        return False
    else:
        return True


def clean_test_database():
    """Clear test database for test isolation purposes."""
    db = _get_db()
    db.client.drop_database(db.name)


@pytest.mark.usefixtures('client_class')
class TestViewBaseClass(object):
    """Base class for view tests.

    This class defines a teardown that clears the database after each test.
    """

    url = None
    schema = None

    def teardown_method(self, _method):
        clean_test_database()

    def get(self, params=None):
        """Perform a GET request to class URL attribute with given params."""
        url = self.build_url(params)
        self.response = self.client.get(url)

    def build_url(self, params):
        """Assemble URL with given query strings params."""
        url = url_for(self.url)
        if params:
            url += '?'
            for param, value in params.items():
                url += '%s=%s&' % (param, value)

        return url

    def response_data(self):
        """Return the response 'data' item."""
        return self.response.json['data']

    def assert_quantity_of_items(self, quantity):
        """Check if the returned data from response matches the quantity."""
        assert len(self.response.json['data']) == quantity

    def assert_response_ok(self):
        """Check if response has OK status and matches the given schema."""
        assert self.response.status_code == 200
        self.assert_matches_schema()

    def assert_matches_schema(self):
        """Check if the JSON response matches the given JSON schema."""
        if self.schema:
            assert matches_json(self.response.json, self.schema)

    def assert_pagination_meta_ok(self, current_page, total_pages):
        """Check if paginationo metadata is present on response."""
        response = self.response.json
        if 'meta' in response:
            metadata = response['meta']
            assert metadata['current_page'] == current_page
            assert metadata['total_pages'] == total_pages
            if 'next_page' in metadata:
                assert metadata['next_page'] == current_page + 1
            if 'previous_page' in metadata:
                assert metadata['previous_page'] == current_page - 1
