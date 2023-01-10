import ipaddress
import logging
import re
from typing import Optional

import dns

logger = logging.getLogger(__name__)


# Via https://github.com/django/django/blob/main/django/core/validators.py
ul = "\u00a1-\uffff"  # Unicode letters range (must not be a raw string).

hostname_re = f"[a-z{ul}0-9](?:[a-z{ul}" + r"0-9-]{0,61}[a-z" + ul + r"0-9])?"

# Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
domain_re = r"(?:\.(?!-)[a-z" + ul + r"0-9-]{1,63}(?<!-))*"
tld_re = (
    r"\."  # dot
    r"(?!-)"  # can't start with a dash
    r"(?:[a-z" + ul + "-]{2,63}"  # domain label
                      r"|xn--[a-z0-9]{1,59})"  # or punycode label
                      r"(?<!-)"  # can't end with a dash
                      r"\.?"  # may have a trailing dot
)

host_re = f"({hostname_re}{domain_re}{tld_re})"


class DomainExtractor:
    regex = re.compile(
        r"^(http|https|ftp|ftps)://"  # scheme
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + host_re + ")"
        r"(?:[/?#]\S*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )

    def __call__(self, value) -> Optional[str]:
        match = re.search(self.regex, value)
        return match[2] if match else None


class DomainValidator:
    regex = re.compile(
        r"^{host_re}\Z".format(host_re=host_re),
        re.IGNORECASE,
    )

    def __call__(self, value) -> bool:
        return bool(re.search(self.regex, value))


def extract_domain(url_like_str: str) -> Optional[str]:
    extractor = DomainExtractor()

    return extractor(url_like_str)


def get_ip_addresses_str(record) -> str:
    try:
        resolved = dns.resolver.resolve(record.domain)
    except Exception as exc:
        logger.exception(f'Unknown error {exc}')
        return record.ip_addresses

    result = (
        sorted([elem.address for elem in resolved if validate_ip_address(elem.address)])
    )

    return '; '.join(result)


def is_ip_address_in_network(ip_address: str, ip_network: str) -> bool:
    try:
        return is_ipv4_in_network(ip_address, ip_network)
    except ValueError:  # IPv6
        return ipaddress.ip_address(ip_address) in ipaddress.ip_network(ip_network)


def is_ipv4_in_network(ip_address, ip_network) -> bool:
    ipaddr = int(''.join(['%02x' % int(x) for x in ip_address.split('.')]), 16)
    netstr, bits = ip_network.split('/')
    netaddr = int(''.join(['%02x' % int(x) for x in netstr.split('.')]), 16)
    mask = (0xffffffff << (32 - int(bits))) & 0xffffffff

    return (ipaddr & mask) == (netaddr & mask)


def validate_domain(domain_like_str: str) -> bool:
    validator = DomainValidator()

    return validator(domain_like_str)


def validate_ip_address(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def validate_ip_range(value: str) -> bool:
    try:
        ipaddress.ip_network(value)
        return True
    except ValueError:
        return False
