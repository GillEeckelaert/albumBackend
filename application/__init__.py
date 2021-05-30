from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from .routes.testRoutes import testRoutesBlueprint
        from .routes.userRoutes import userRoutesBlueprint
        from .routes.docRoutes import docRoutesBlueprint
        from .routes.authRoutes import authRoutesBlueprint

        # Register Blueprints
        app.register_blueprint(testRoutesBlueprint)
        app.register_blueprint(userRoutesBlueprint)
        app.register_blueprint(docRoutesBlueprint)
        app.register_blueprint(authRoutesBlueprint)

        db.create_all()

        return app