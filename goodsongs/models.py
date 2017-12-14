"""App models."""

from datetime import datetime

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
