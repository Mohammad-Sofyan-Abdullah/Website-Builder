import ipaddress
from urllib.parse import urlparse
from fastapi import HTTPException

_BLOCKED_HOSTS = {"localhost", "ip6-localhost", "ip6-loopback", "broadcasthost"}


def validate_safe_url(url: str) -> str:
    """Block SSRF-prone URLs: non-http(s), loopback, private, and link-local targets."""
    try:
        parsed = urlparse(url)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid URL")

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only http/https URLs are allowed")

    host = (parsed.hostname or "").lower()
    if not host:
        raise HTTPException(status_code=400, detail="URL must include a hostname")

    if host in _BLOCKED_HOSTS:
        raise HTTPException(status_code=400, detail="URL hostname not allowed")

    try:
        addr = ipaddress.ip_address(host)
        if any([
            addr.is_loopback,
            addr.is_private,
            addr.is_link_local,
            addr.is_reserved,
            addr.is_multicast,
        ]):
            raise HTTPException(status_code=400, detail="URL hostname not allowed")
    except ValueError:
        pass  # hostname (not a raw IP) — allowed

    return url
