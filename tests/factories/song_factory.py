import datetime

from factory import Sequence
from factory.mongoengine import MongoEngineFactory

from goodsongs.models import Song


class SongFactory(MongoEngineFactory):
    class Meta:
        model = Song

    artist = Sequence(lambda n: 'Artist %d' % n)
    title = Sequence(lambda n: 'Title %d' % n)
    difficulty = Sequence(lambda n: float(n))
    level = Sequence(lambda n: n)
    released = Sequence(
        lambda n: datetime.datetime.now() + datetime.timedelta(days=n)
    )
    ratings = []
