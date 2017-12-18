# Goodsongs
Goodsongs is a Flask API that manages a MongoDB songs collection. It has the following endpoints:

- GET /songs
  - Return a list of songs with some details on them.
  - Accepts page and per_page parameters as a query strings to paginate the results.

- GET /songs/avg/difficulty
  - Return the average difficulty for all songs.
  - Accepts an optional parameter "level" as query string to select only songs from a specific level.

- GET /songs/search
  - Search for songs with the given message.
  - Accepts "message" as a query string to be the search parameter.
  - Accepts page and per_page parameters as a query strings to paginate the results.
  - The search is case insensitive and will search for song's and artist's names.

- POST /songs/rating
  - Add a rating to the given song.
  - Takes in parameter a "song_id" and a "rating".
  - Ratings should be between 1 and 5.

- GET /songs/avg/rating/<song_id>
  - Return the average, the lowest and the highest rating of the given song.

## Running the application

There are two ways to run the application: the easiest and hardest.

### Running using Docker

The easiest way to run the application is using Docker and Docker Compose.

You can find instructions to install Docker [here](https://docs.docker.com/engine/installation/) and Docker Compose [here](https://docs.docker.com/compose/install/).

With Docker and Docker Compose installed, just run `docker-compose up -d` to start the services and you are done!
The API will be running on http://localhost:5000.

Using Docker, the API will be configured with all requirements needed and a MongoDB instance will be available too.

### Running manually

The hardest way is to set up all the environment by yourself.

Goodsongs was built with Flask, so you will need **Python 3** and pip in order to run it locally.
Goodsongs also uses MongoDB as database engine, so you will need to install it locally.
You can find instructions to install MongoDB on your machine [here](https://docs.mongodb.com/manual/installation/).


With MongoDB installed, let's proceed with setting up the Flask API:

**_OBS_**: You may want to create a [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to isolate the dependencies of Goodsongs before installing it.

1. Clone the repository and navigate to it.

`$ git clone https://github.com/italopaiva/goodsongs.git && cd goodsongs/`

2. Install the requirements.

`$ pip install -r requirements.txt`

3. Run the API

    **_OBS_**: By default, Goodsongs will try to connect with MongoDB on localhost:27017 (MongoDB's default), but you can change it on `config/development.py`.

`$ python run.py`


## Seeding the database

Goodsongs has `songs.json` file that contains some songs to seed the database.

To seed the database with `songs.json`, just run:

- If using Docker:
    `$ docker exec -it api flask seeddb --songs songs.json`

- If running locally:
    `$ flask seeddb --songs songs.json`

## Running tests

NotifiCar is shipped with _tox_, so just run `tox` to run the test suite:

- If using Docker:
    `$ docker exec -it api tox`

- If running locally:
    `$ tox`

The tests relies on _pytest_, so you can run it too:

`$ pytest --cov=.`

## Performance analysis

A simple test was made to check out Goodsongs performance and it is described bellow:

- Environment:
    - Host machine with a Intel Core i5 processor and 4GB RAM;
    - Flask API and MongoDB instance running on Docker containers;
    - Using Google Chrome as client for requests;
    - Metrics colected with docker [stats](https://docs.docker.com/engine/reference/commandline/stats/).

- Scenario 1: With 1M songs and no ratings
    - Endpoint GET /songs:
        - Paginating with per_page=1000
            - API
                - Memory Usage: 50MiB-60MiB / 3.767GiB
            - Database
                - Memory Usage: ~316MiB / 3.767GiB
            - Request time: ~500ms
        - Paginating with per_page=5000
            - API
                - Memory Usage: 60MiB-65MiB / 3.767GiB
            - Database
                - Memory Usage: ~316MiB / 3.767GiB
            - Request time: ~3s
        - Paginating with per_page=10000
            - API
                - Memory Usage: 60MiB-80MiB / 3.767GiB
            - Database
                - Memory Usage: ~316MiB / 3.767GiB
            - Request time: ~6s
        - Paginating with per_page=100000
            - API
                - Memory Usage: ~400MiB / 3.767GiB
            - Database
                - Memory Usage: ~350MiB / 3.767GiB
            - Request time: ~1.8min
    - Endpoint GET /songs/search:
        - Behaves closely to GET /songs
    - Endpoint GET /songs/avg/difficulty:
        - API
            - Memory Usage: ~50MiB / 3.767GiB
        - Database
            - Memory Usage: ~350MiB / 3.767GiB
        - Request time: ~900ms
    - Endpoint GET /songs/avg/rating/<song_id>:
        - Song with 100k ratings
        - API
            - Memory Usage: ~60MiB / 3.767GiB
        - Database
            - Memory Usage: ~350MiB / 3.767GiB
        - Request time: ~150ms