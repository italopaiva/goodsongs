"""Development configuration values."""
from os import environ

DEGUG = True

DATABASE_NAME = 'goodsongs'

# Database config
MONGODB_DB = DATABASE_NAME
MONGODB_HOST = 'mongo' if 'RUNNING_FROM_DOCKER' in environ else 'localhost'
MONGODB_PORT = 27017
