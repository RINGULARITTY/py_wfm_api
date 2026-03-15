import re
import threading
import requests
import time
import logging
from json import JSONDecodeError
from typing import Any, Optional

API_BASE_URL = "https://api.warframe.market/v2"
API_VERSION = "0.21.2"
REQUEST_TIMEOUT = 10  # seconds

_api_version_checked: bool = False
_auth_token: Optional[str] = None
_rate_limit_delay: float = 0.35  # seconds between requests
_last_request_time: float = 0.0
_rate_limit_lock = threading.Lock()  # thread-safe rate limiting

# Slugs: lowercase alphanumeric + hyphens/underscores (e.g. "boltor-prime-set")
# IDs:   hex chars + hyphens (UUID-like)
_SLUG_RE = re.compile(r'^[a-z0-9_-]+$')
_ID_RE   = re.compile(r'^[a-zA-Z0-9_-]+$')


def set_auth_token(token: str) -> None:
    """Set the JWT Bearer token used for authenticated requests."""
    global _auth_token
    _auth_token = token


def clear_auth_token() -> None:
    """Remove the stored authentication token."""
    global _auth_token
    _auth_token = None


def validate_slug(value: str, name: str = "slug") -> str:
    """Raise ValueError if *value* is not a safe URL path segment."""
    if not value or not _SLUG_RE.match(value):
        raise ValueError(
            f"Invalid {name} '{value}': must only contain lowercase letters, "
            "digits, hyphens, or underscores."
        )
    return value


def validate_id(value: str, name: str = "id") -> str:
    """Raise ValueError if *value* is not a safe identifier (UUID-like)."""
    if not value or not _ID_RE.match(value):
        raise ValueError(
            f"Invalid {name} '{value}': must only contain alphanumeric characters and hyphens."
        )
    return value


def _rate_limit() -> None:
    global _last_request_time
    with _rate_limit_lock:
        elapsed = time.time() - _last_request_time
        if elapsed < _rate_limit_delay:
            time.sleep(_rate_limit_delay - elapsed)
        _last_request_time = time.time()


def _check_api_version(json_res: dict) -> None:
    global _api_version_checked
    if not _api_version_checked:
        server_version = json_res.get("apiVersion")
        if server_version and server_version != API_VERSION:
            logging.warning(
                f"API version mismatch — Server: {server_version}, Library: {API_VERSION}. "
                f"Some features may not work as expected."
            )
        _api_version_checked = True


def _make_request(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    json: Optional[Any] = None,
) -> Any:
    _rate_limit()

    url = f"{API_BASE_URL}/{endpoint}"
    headers: dict = {}
    if _auth_token:
        headers["Authorization"] = f"Bearer {_auth_token}"

    response = requests.request(
        method, url, params=params, json=json, headers=headers,
        timeout=REQUEST_TIMEOUT,
    )

    # 204 No Content — DELETE endpoints typically return this
    if response.status_code == 204 or not response.content:
        return None

    if response.status_code not in (200, 201):
        # Truncate response body to avoid leaking large/sensitive payloads
        preview = response.text[:200] if response.text else ""
        raise ValueError(
            f"HTTP {response.status_code} for {method} '{endpoint}': {preview}"
        )

    try:
        json_res = response.json()
    except JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON response from '{endpoint}'") from exc

    error = json_res.get("error")
    if error is not None:
        raise ValueError(f"Warframe Market API error: {error}")

    _check_api_version(json_res)
    return json_res.get("data")


# ─── Public helpers ───────────────────────────────────────────────────────────

def get_request_wfm(endpoint: str, params: Optional[dict] = None) -> Any:
    return _make_request("GET", endpoint, params=params)


def post_request_wfm(endpoint: str, json: Optional[Any] = None) -> Any:
    return _make_request("POST", endpoint, json=json)


def put_request_wfm(endpoint: str, json: Optional[Any] = None) -> Any:
    return _make_request("PUT", endpoint, json=json)


def patch_request_wfm(endpoint: str, json: Optional[Any] = None) -> Any:
    return _make_request("PATCH", endpoint, json=json)


def delete_request_wfm(endpoint: str) -> None:
    _make_request("DELETE", endpoint)
