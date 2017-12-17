import random

from factory import LazyFunction
from factory.mongoengine import MongoEngineFactory

from goodsongs.models import Rating


class RatingFactory(MongoEngineFactory):
    class Meta:
        model = Rating

    value = LazyFunction(lambda: random.choice(Rating.VALID_RATINGS))
