import flask

from app import db
from app.models import Record


def update_domain_ip_task(app: flask.Flask):
    with app.app_context():
        for record in db.session.execute(db.select(Record)).scalars():
            if record.update_ip_addresses():
                db.session.add(record)

        db.session.commit()
