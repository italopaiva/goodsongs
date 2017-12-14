"""Testing configuration values."""
from os import environ

DEGUG = True

# Database config
#
# There are issues with mongomock with flask_mongoengine pagination.
# Therefore mongomock was not used for tests yet.
#
# MONGODB_HOST = 'mongomock://localhost'
#
# Travis-CI run Mongo on "127.0.0.1" host.
#
DATABASE_NAME = 'goodsongs_test'
MONGODB_DB = DATABASE_NAME
MONGODB_PORT = 27017
MONGODB_HOST = 'mongo' if 'RUNNING_FROM_DOCKER' in environ else '127.0.0.1'
