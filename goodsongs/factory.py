from flask import Flask


def create_app(config_filename):
    app = Flask('goodsongs')

    app.config.from_object('config.base')
    app.config.from_pyfile(config_filename)

    register_blueprints(app)

    return app


def register_blueprints(app):
    from goodsongs.songs.views import songs

    app.register_blueprint(songs, url_prefix='/songs')
