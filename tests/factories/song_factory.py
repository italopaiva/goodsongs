import datetime
import random

from factory import LazyFunction, Sequence
from factory.mongoengine import MongoEngineFactory

from goodsongs.models import Song


class SongFactory(MongoEngineFactory):
    class Meta:
        model = Song

    artist = Sequence(lambda n: 'Good musician %d' % n)
    title = Sequence(lambda n: 'Good song %d' % n)
    difficulty = LazyFunction(lambda: round(random.uniform(1.0, 20.0), 2))
    level = LazyFunction(lambda: random.randint(1, 20))
    released = datetime.datetime.now()
    ratings = []
