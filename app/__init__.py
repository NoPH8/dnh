from flask import Flask, render_template, url_for
from flask_admin import helpers as admin_helpers
from flask_security import SQLAlchemySessionUserDatastore, Security

from config import AppConfig
from .admin import UserModelView, admin
from .database import db
from .models import Role, User, UserRoles
from .utils import create_roles, create_tables


def create_app(config_class=AppConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # DB initialization
    db.init_app(app)

    # Flask security initialization
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security = Security(app, user_datastore)

    # Flask admin initialization
    admin.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # App hooks
    create_tables(app)
    create_roles(app)

    return app
