


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate 
from flask_talisman import Talisman  # <-- Import Talisman
from config import Config

db = SQLAlchemy()
migrate = Migrate() 
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ==================================================================
    # TALISMAN CONFIGURATION
    # ==================================================================
    # This Content Security Policy will be sent with every response.
    # It explicitly allows 'unsafe-eval' for scripts, which fixes the debugger.
    csp = {
        'default-src': '\'self\'',
        'script-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            '\'unsafe-eval\'',  # <-- The required setting for the debugger
            'https://stackpath.bootstrapcdn.com' # Allow Bootstrap CSS
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://stackpath.bootstrapcdn.com' # Allow Bootstrap CSS
        ]
    }
    # Initialize Talisman with the specific CSP
    Talisman(app, content_security_policy=csp)
    # ==================================================================

    db.init_app(app)
    migrate.init_app(app, db) 
    login_manager.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # It's generally better to not run db.create_all() here
    # and rely solely on flask db upgrade, but we will leave it for now.
    with app.app_context():
        db.create_all()

    return app