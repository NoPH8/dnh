import ipaddress
import re
from typing import Optional

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


def validate_domain(domain_like_str: str) -> bool:
    validator = DomainValidator()

    return validator(domain_like_str)


def validate_ip_address(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
