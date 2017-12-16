"""App factory functions."""

from flask import Flask


def create_app(config_filename):
    """Create an instance of the app with given configuration file."""
    app = Flask('goodsongs')

    app.config.from_object('config.base')
    app.config.from_pyfile(config_filename)

    config_database(app)
    register_blueprints(app)
    register_cli(app)
    register_errors_handlers(app)

    return app


def register_blueprints(app):
    """Resgister app blueprints."""
    from goodsongs.songs.views import songs

    app.register_blueprint(songs, url_prefix='/songs')


def config_database(app):
    """Configure app database."""
    from goodsongs.models import db

    db.init_app(app)


def register_cli(app):
    """Register custom CLI commands."""
    from goodsongs.models import seed_database
    import click

    @app.cli.command('seeddb')
    @click.option('--songs')
    def seed_database_command(**kwargs):
        """Initiate the database with custom data."""
        seed_database(**kwargs)
        print('Database seeded.')


def register_errors_handlers(app):
    """Register application general errors handlers."""
    from goodsongs.errors import NotFoundError
    from goodsongs.api_responses import not_found

    @app.errorhandler(NotFoundError)
    def not_found_error_handler(error):
        """Error handler for when NotFoundError be raised."""
        return not_found(message=str(error))
