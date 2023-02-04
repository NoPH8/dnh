from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app import db
from app.api.auth import api_key_required
from app.api.v1.validators import ValidationError, validate_ip_family
from app.constants import IP_FAMILY_VALUES, IP_FAMILY_IP_v4, IP_FAMILY_IP_v6
from app.models import IPRange, Record
from app.tools.network import (is_ip_address_in_network, is_ipv4_address,
                               is_ipv6_address)

api_v1 = Blueprint('v1', __name__, url_prefix='/v1')


@api_v1.route('/ip_list')
@api_key_required
def ip_list():
    ip_family = request.args.get('family', '').lower()

    try:
        validate_ip_family(ip_family)
    except ValidationError:
        error_message = f'Invalid family value. Allowed are {", ".join(IP_FAMILY_VALUES)}'
        return {'message': error_message}, HTTPStatus.BAD_REQUEST

    return jsonify(get_ip_list_response(ip_family))


def get_ip_list_response(ip_family: str) -> dict:  # noqa C901
    all_ip_addresses = set()
    address_filter = None

    custom_ranges_query = db.select(IPRange.ip_range).filter(IPRange.active)

    if ip_family == IP_FAMILY_IP_v4:
        address_filter = is_ipv4_address
        custom_ranges_query = custom_ranges_query.filter(IPRange.ip_range.contains('.'))
    elif ip_family == IP_FAMILY_IP_v6:
        address_filter = is_ipv6_address
        custom_ranges_query = custom_ranges_query.filter(IPRange.ip_range.contains(':'))

    custom_ranges = set(db.session.execute(custom_ranges_query).scalars())

    records = db.session.execute(
        db.select(Record.ip_addresses).filter(Record.updated_at.isnot(None) & Record.active)
    ).scalars()

    for record in records:
        ip_addresses = record.split('; ')
        if address_filter:
            ip_addresses = filter(address_filter, ip_addresses)

        for address in ip_addresses:
            unique = not any(
                is_ip_address_in_network(address, network)
                for network in custom_ranges
            )
            if unique:
                all_ip_addresses.add(address)

    all_ip_addresses.update(custom_ranges)
    last_record = db.session.execute(
        db.select(Record.updated_at).filter(Record.active).order_by(Record.updated_at.desc())
    ).first()

    return {
        'ip_addresses': sorted(list(all_ip_addresses)),
        'updated_at': last_record[0] if last_record else None,
    }
