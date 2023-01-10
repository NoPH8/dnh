from flask import Blueprint, jsonify

from app import db
from app.models import IPRange, Record
from app.tools.network import is_ip_address_in_network

api_v1 = Blueprint('v1', __name__, url_prefix='/v1')


@api_v1.route('/ip_list')
def ip_list():
    return jsonify(get_ip_list_response())


def get_ip_list_response() -> dict:
    all_ip_addresses = set()

    custom_ranges = list(db.session.execute(db.select(IPRange.ip_range)).scalars())

    records = db.session.execute(
        db.select(Record.ip_addresses).filter(Record.updated_at.isnot(None))
    ).scalars()

    for record in records:
        ip_addresses = record.split('; ')

        for address in ip_addresses:
            unique = not any(
                is_ip_address_in_network(address, network)
                for network in custom_ranges
            )
            if unique:
                all_ip_addresses.add(address)

    all_ip_addresses.update(set(custom_ranges))
    last_record = db.session.execute(
        db.select(Record.updated_at).order_by(Record.updated_at.desc())
    ).first()

    return {
        'ip_addresses': sorted(list(all_ip_addresses)),
        'updated_at': last_record[0] if last_record else None,
    }
