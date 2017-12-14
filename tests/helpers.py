"""Test helpers module."""

from mongoengine.connection import _get_db


def clean_test_database():
    """Clear test database for test isolation purposes."""
    db = _get_db()
    db.client.drop_database(db.name)


class TestViewBaseClass(object):
    """Base class for view tests.

    This class defines a teardown that clears the database after each test.
    """

    def teardown_method(self, _method):
        clean_test_database()
