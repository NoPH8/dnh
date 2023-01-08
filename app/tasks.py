import datetime
import logging

import dns.resolver
import flask

from app import db
from app.models import Record
from app.tools.network import validate_ip_address

logger = logging.getLogger(__name__)


def update_domain_ip_task(app: flask.Flask):
    with app.app_context():
        for record in db.session.execute(db.select(Record)).scalars():
            try:
                resolved = dns.resolver.resolve(record.domain)
                result = (
                    sorted([elem.address for elem in resolved if validate_ip_address(elem.address)])
                )
                ip_addresses = '; '.join(result)
                if record.ip_addresses != ip_addresses:
                    record.ip_addresses = ip_addresses
                    record.updated_at = datetime.datetime.now()
                    db.session.add(record)
            except Exception as exc:
                logger.exception(f'Unknown error {exc}')

        db.session.commit()
