"""Basic SSRF protection: only http(s) URLs, block private IPs."""
import ipaddress
import socket
from urllib.parse import urlparse


def is_safe_url(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https") or not p.hostname:
            return False
        if p.hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
            return False
        # Resolve and reject private ranges
        try:
            infos = socket.getaddrinfo(p.hostname, None)
        except socket.gaierror:
            return False
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False
        return True
    except Exception:
        return False