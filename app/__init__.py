from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, url_for
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemySessionUserDatastore

from app.tools.utils import create_roles, create_tables
from config import AppConfig

from .admin import app_admin
from .dashboard import dashboard, turbo
from .database import db
from .models import Role, User
from .signals import connect_update_last_login_signal
from .tools.json import JSONProvider


def create_app(config_class=AppConfig, *args, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json_provider_class = JSONProvider

    # DB initialization
    db.init_app(app)

    # Flask security initialization
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security = Security(app, user_datastore)

    # Flask admin initialization
    app_admin.init_app(app)

    # Scheduler initialization
    app.scheduler = BackgroundScheduler()
    app.scheduler.start()

    # Dashboard initialization
    turbo.init_app(app)
    dashboard.init_app(app)

    @app.security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=app_admin.base_template,
            admin_view=app_admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    from app.management import manage_bp
    app.register_blueprint(manage_bp)
    from app.scheduler import scheduler_bp
    app.register_blueprint(scheduler_bp)
    from app.api.views import api_bp
    app.register_blueprint(api_bp)

    # App hooks
    create_tables(app)
    create_roles(app)
    connect_update_last_login_signal(app, db)

    return app
