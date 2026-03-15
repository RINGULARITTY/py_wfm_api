from py_wfm_api.api.core import set_auth_token, clear_auth_token, post_request_wfm
from py_wfm_api.objects.user import UserPrivate


def signin(email: str, password: str) -> UserPrivate:
    """Authenticate with Warframe Market and store the JWT token.

    The token is automatically injected into all subsequent API requests.
    Returns the authenticated user's private profile.
    """
    data = post_request_wfm("auth/signin", json={"email": email, "password": password})
    token = (
        data.get("accessToken")
        or data.get("token")
        or data.get("jwt")
    )
    if not token:
        raise ValueError("Authentication failed: no token received in response.")
    set_auth_token(token)
    return UserPrivate(**data.get("user", {})) if data.get("user") else data


def signout() -> None:
    """Sign out and clear the stored authentication token."""
    try:
        post_request_wfm("auth/signout")
    finally:
        clear_auth_token()


def set_token(token: str) -> None:
    """Manually set a JWT token (e.g. extracted from a browser session).

    Use this if you already have a valid token and do not want to call signin().
    """
    set_auth_token(token)


def logout() -> None:
    """Alias for signout()."""
    signout()
