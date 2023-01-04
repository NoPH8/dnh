import datetime

from flask_security import user_authenticated


def connect_update_last_login_signal(app, db):
    @user_authenticated.connect_via(app)
    def update_last_login(app, user, *args, **kwargs):
        user.last_login_at = datetime.datetime.now()
        db.session.commit()
