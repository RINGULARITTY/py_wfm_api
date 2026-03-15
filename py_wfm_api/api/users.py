from typing import List
from py_wfm_api.api.core import get_request_wfm, put_request_wfm, validate_slug
from py_wfm_api.objects.categories import Status
from py_wfm_api.objects.user import User, UserPrivate

_VALID_STATUSES = {s.value for s in Status}


def get_profile(username: str) -> User:
    """Get a user's public profile by their in-game name."""
    return User(**get_request_wfm(f"profile/{validate_slug(username, 'username')}"))


def search_users(query: str) -> List[User]:
    """Search for users by name."""
    return [User(**u) for u in get_request_wfm("profile/search", params={"q": query})]


def get_my_profile() -> UserPrivate:
    """Get the authenticated user's full private profile. Requires auth token."""
    return UserPrivate(**get_request_wfm("profile/my"))


def update_my_profile(
    about: str | None = None,
    status: str | None = None,
) -> UserPrivate:
    """Update the authenticated user's profile. Requires auth token.

    Args:
        about:  HTML-formatted about text.
        status: New status value — one of: 'online', 'invisible', 'offline', 'ingame'.
    """
    if status is not None and status not in _VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {sorted(_VALID_STATUSES)}")

    payload = {k: v for k, v in {"about": about, "status": status}.items() if v is not None}
    return UserPrivate(**put_request_wfm("profile/my", json=payload))
