"""App models."""

from datetime import datetime

from bson.errors import InvalidId
from bson.objectid import ObjectId

from flask_mongoengine import MongoEngine

from goodsongs.errors import NotFoundError

from mongoengine.queryset.visitor import Q


db = MongoEngine()


class Song(db.Document):
    """Model to describe a Song."""

    artist = db.StringField()
    title = db.StringField()
    difficulty = db.FloatField()
    level = db.IntField()
    released = db.DateTimeField()

    meta = {'collection': 'songs'}

    ratings = [{'value': 3}]

    @classmethod
    def get(cls, song_id):
        """Find a song by its Object ID."""
        try:
            song_object_id = ObjectId(song_id)
            return cls.objects.get(pk=song_object_id)
        except (cls.DoesNotExist, TypeError, InvalidId):
            raise NotFoundError('Song with ID %s not found' % song_id)

    @classmethod
    def find_by_title_or_artist(cls, message):
        """Return songs containing the given message in title or artists."""
        return cls.objects(
            Q(title__icontains=message) | Q(artist__icontains=message)
        )

    @classmethod
    def difficulty_average(cls, level=None):
        """Return songs difficulty average.

        Accepts a level parameter to narrow the calculation for songs in level.
        """
        level_songs = Song.objects
        if level:
            level_songs = level_songs.filter(level=level)
        average = level_songs.average('difficulty')

        return average

    @classmethod
    def load_songs_from_file(cls, songs_file):
        """Load songs from a JSON like file."""
        import json

        songs = []
        with open(songs_file, 'r') as song_file:
            for line in song_file:
                song = json.loads(line)
                song_obj = cls(
                    artist=song['artist'],
                    title=song['title'],
                    difficulty=song['difficulty'],
                    level=song['level'],
                    released=datetime.strptime(song['released'], '%Y-%m-%d'),
                )
                songs.append(song_obj)
        cls.objects.insert(songs)


def seed_database(songs='', **_kwargs):
    """Seed the database with the given files."""
    Song.load_songs_from_file(songs)
