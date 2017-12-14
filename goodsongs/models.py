"""App models."""

from flask_mongoengine import MongoEngine


db = MongoEngine()


class Song(db.Document):
    """Model to describe a Song."""

    artist = db.StringField()
    title = db.StringField()
    difficulty = db.FloatField()
    level = db.IntField()
    released = db.DateTimeField()

    meta = {'collection': 'songs'}


def seed_database(songs='', **_kwargs):
    """Seed the database with the given files."""
    pass
