"""App models."""

from flask_mongoengine import MongoEngine


db = MongoEngine()


def seed_database(songs='', **_kwargs):
    """Seed the database with the given files."""
    pass
