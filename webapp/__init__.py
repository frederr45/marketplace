import logging

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.market.views import blueprint as market_blueprint
from webapp.images.views import blueprint as img_blueprint
from webapp.message.views import blueprint as message_blueprint


def create_app():
    app = Flask(__name__, static_folder='templates/images')
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'market.index'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(market_blueprint)
    app.register_blueprint(img_blueprint)
    app.register_blueprint(message_blueprint)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        handlers=[logging.FileHandler('logging.log',
                                                      'w', 'utf-8')])

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app
