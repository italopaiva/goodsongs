"""App models."""

from datetime import datetime

from bson.errors import InvalidId
from bson.objectid import ObjectId

from flask_mongoengine import MongoEngine

from goodsongs.errors import InvalidRecordError, NotFoundError

from mongoengine.errors import ValidationError
from mongoengine.queryset.visitor import Q


db = MongoEngine()


class Rating(db.EmbeddedDocument):
    """Represents a song rating."""

    VALID_RATINGS = tuple(range(1, 6))

    value = db.IntField(choices=VALID_RATINGS)


class Song(db.Document):
    """Model to describe a Song."""

    artist = db.StringField()
    title = db.StringField()
    difficulty = db.FloatField()
    level = db.IntField()
    released = db.DateTimeField()
    ratings = db.ListField(db.EmbeddedDocumentField(Rating))

    meta = {
        'collection': 'songs',
        'indexes': [
            '$title',
            '+level',
        ]
    }

    def add_rating(self, rating_value):
        """Add a new rating for the song."""
        rating = Rating(value=rating_value)
        self.ratings.append(rating)
        try:
            self.save()
        except ValidationError:
            raise InvalidRecordError('Ratings range from 1 to 5')

    def get_ratings_data(self):
        """Get the lowest, highest and average rating for the song."""
        query = """
        function (){
            return db[collection].aggregate([
                { "$project": {"ratings": 1} },
                { "$match": { "_id": ObjectId(options.songId) } },
                { "$unwind": "$ratings" },
                {
                    "$group": {
                        "_id": "$_id",
                        "average": { "$avg": "$ratings.value" },
                        "lowest": { "$min": "$ratings.value" },
                        "highest": { "$max": "$ratings.value" },
                    }
                }
            ]);
        }
        """
        options = {'songId': str(self.id)}
        result = self.__class__.objects.exec_js(query, **options)
        result = result['_batch']

        if result:
            ratings_data = result[0]
            average = ratings_data['average']
            lowest = ratings_data['lowest']
            highest = ratings_data['highest']
        else:
            average = lowest = highest = None

        return {
            'average': average,
            'lowest': lowest,
            'highest': highest,
        }

    @classmethod
    def get(cls, song_id):
        """Find a song by its Object ID."""
        try:
            song_object_id = ObjectId(song_id)
            return cls.objects.exclude('ratings').get(pk=song_object_id)
        except (cls.DoesNotExist, TypeError, InvalidId):
            raise NotFoundError('Song with ID %s not found' % song_id)

    @classmethod
    def find_by_title_or_artist(cls, message):
        """Return songs containing the given message in title or artists."""
        return cls.objects.exclude('ratings').filter(
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
