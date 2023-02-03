from flask import Blueprint, jsonify

from app import db
from app.api.auth import api_key_required
from app.models import IPRange, Record
from app.tools.network import is_ip_address_in_network

api_v1 = Blueprint('v1', __name__, url_prefix='/v1')


@api_v1.route('/ip_list')
@api_key_required
def ip_list():
    return jsonify(get_ip_list_response())


def get_ip_list_response() -> dict:
    all_ip_addresses = set()

    custom_ranges_query = db.select(IPRange.ip_range).filter(IPRange.active)

    records = db.session.execute(
        db.select(Record.ip_addresses).filter(Record.updated_at.isnot(None) & Record.active)
    ).scalars()

    for record in records:
        ip_addresses = record.split('; ')

        for address in ip_addresses:
            unique = not any(
                is_ip_address_in_network(address, network)
                for network in db.session.execute(custom_ranges_query).scalars()
            )
            if unique:
                all_ip_addresses.add(address)

    all_ip_addresses.update(set(db.session.execute(custom_ranges_query).scalars()))
    last_record = db.session.execute(
        db.select(Record.updated_at).filter(Record.active).order_by(Record.updated_at.desc())
    ).first()

    return {
        'ip_addresses': sorted(list(all_ip_addresses)),
        'updated_at': last_record[0] if last_record else None,
    }
