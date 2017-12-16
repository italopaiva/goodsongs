import json

from os.path import dirname, join


def load_json_schema(schema_file_name):
    """Load json schema from JSON file."""
    with open(schema_file_name) as schema_file:
        return json.loads(schema_file.read())


current_dir = dirname(__file__)

songs_json_schema_file = join(current_dir, 'songs.json')
songs_difficulty_json_schema_file = join(current_dir, 'songs_difficulty.json')

all_songs_schema = load_json_schema(songs_json_schema_file)
songs_difficulty_schema = load_json_schema(songs_difficulty_json_schema_file)
